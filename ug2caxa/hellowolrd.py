#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# ugdxf调整格式处理，仅限UG转出的dxf使用,其他风格dxf需要调整匹配规则
# 变量处理 
filename="0.dxf"; outputfile="output.dxf"

# 引入包
import ezdxf, os

def main(fn,fnout):
    print ("按文件名获取文件对象，如报错检查文件名,当前文件名为：",fn)
    doc = ezdxf.readfile(fn,"utf-8") #按文件名获取文件实例，需要R2007或以后版本
    print ('打印文件实例和内存地址',doc)
    print ("打印当前dxfversion：",doc.dxfversion)
    print ("打印当前版本对应的autocad release版本:",doc.acad_release)
    print ("打印文件当前编码：",doc.encoding) #需要R2007以上版本
    print ("打印当前output_encoding",doc.output_encoding) #https://ezdxf.readthedocs.io/en/stable/dxfinternals/fileencoding.html#dxf-file-encoding
    msp = doc.modelspace()  #获取modelspace实例
    print ("打印modelspace实例和内存地址",msp)
    psp = doc.layout("model")  #按Layout键值获取paperspace实例，Caxa中显示“模型”键值为model，不存在键值的例如Layout3会报错，caxa转出的dxf未测试
    print ("打印paperspace实例和内存地址",psp)
    # print (doc.tables.layers.entries.keys().__contains__("中心线层"))
    
    # 创建图层以CAXA图层形势
    print ("打印当前文件包含的标注风格",doc.tables.dimstyles.entries)
    print ("打印当前文件包含的图层名称",doc.tables.layers.entries.keys())
    print("以CAXA为基准创建相同名称图层，如报错说明已经存在同名图层")
    doc.layers.add(name="粗实线层", lineweight=35,color=7, linetype="BYLAYER" )  # color:0 BYBLOCK， 256BYLAYER，257	BYOBJECT
    doc.layers.add(name="中心线层", lineweight=18,color=1, linetype="BYLAYER") #lineweight: -1 LINEWEIGHT_BYLAYER
    doc.layers.add(name="尺寸线层", lineweight=18,color=3, linetype="BYLAYER" ) #lineweight: -1 LINEWEIGHT_BYLAYER
    doc.layers.add(name="细实线层", lineweight=18,color=7, linetype="BYLAYER") #粗实线默认0.35mm，细实线默认0.18mm #粗实线默认0.35mm，细实线默认0.18mm
    doc.layers.add(name="虚线层", lineweight=18,color=6, linetype="BYLAYER" )
    doc.layers.add(name="剖面线层", lineweight=18,color=4, linetype="BYLAYER" )
    doc.layers.add(name="修改图层", lineweight=80,color=1, linetype="Continuous" ) # ※这里放置需要修改的内容
    doc.layers.add(name="螺纹线线层", lineweight=18,color=7, linetype="Continuous")
    doc.layers.add(name="文字图层", lineweight=18,color=3, linetype="Continuous")
    # Query规则查找对象，处理对象。   https://ezdxf.readthedocs.io/en/stable/tutorials/getting_data.html#entity-queries
    # 删除不可见线
    print("删除不可见线，dxf属性 ('invisible', 1)")
    invisible=msp.query('*[invisible==1]')
    for e in invisible:
        msp.delete_entity(e)
    
    print ("删除UG的表格框，以block块标签TabularNote.*正则匹配")
    ugtables=msp.query('INSERT[name?"TabularNote.*"]')
    for e in ugtables:
        msp.delete_entity(e)

    print ("查找所有轮廓线，设置图层为粗实线层，以下所有查找规则以线条颜色，线型和线条粗细为基准")
    borderlines = msp.query('*[color==7]') #查找轮廓线对象
    # printlog=open("log.txt","w")
    for e in borderlines:
        # print (e.dxfattribs().items(),file=printlog) #获取所有可以使用的dxf属性attribute
        e.set_dxf_attrib("layer","粗实线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
    # printlog.close()    

    print ("查找所有尺寸线，设置图层为尺寸线层")
    dimensions = msp.query('DIMENSION[color==3 & lineweight==13]') #在绿色中查找尺寸对象
    for e in dimensions:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        # print (e.get_dxf_attrib("color")) #打印颜色索引，绿色3
        # print(e.dxf.text, "尺寸结束")
        # print(e.dxf.text.replace(" <>","<>"))
        e.dxf.text=e.dxf.text.replace(" <>","<>") #修改尺寸文字，去掉尺寸前空格
        e.dxf.text=e.dxf.text.replace("直径","c%") # 把“直径”字符改成caxa中φ代号"c%"
        e.set_dxf_attrib("layer","尺寸线层")  #设置尺寸对象图层为尺寸线层
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
        # e.set_dxf_attrib("dimstyle","标准")

    print ("查找失效尺寸线，匹配规则为绿色Block,设置图层为修改图层")
    inserts = msp.query('INSERT[color==3]') #※使用正则表达式查找文字文字注释引用快对象※
    if len(inserts):
        for e in inserts:
            # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
            # print (e.dxftype())
            for blocklayoutents in e.block():
                # print ("当前Block下实体为",blocklayoutents.dxftype())
                blocklayoutents.set_dxf_attrib("layer","修改图层")  
                blocklayoutents.set_dxf_attrib("linetype","BYLAYER")  
                blocklayoutents.set_dxf_attrib("color",256)  
                blocklayoutents.set_dxf_attrib("lineweight",-1)
            
            e.set_dxf_attrib("layer","修改图层")  
            e.set_dxf_attrib("linetype","BYLAYER")  
            e.set_dxf_attrib("color",256)  
            e.set_dxf_attrib("lineweight",-1)

    print ("查找失效尺寸线，匹配规则为绿色MTEXT,设置图层为修改图层") #UG中的文字设置成绿色以外
    invaliddims= msp.query('MTEXT[color==3]') 
    for e in invaliddims:
        e.set_dxf_attrib("layer","修改图层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)

    print ("查找所有中心线，设置图层为中心线层")
    centerlines = msp.query('LINE ARC CIRCLE SPLINE[color==1 & linetype=="CENTER"]')#查找线条对象以红色，线型CENTER
    # centerlines = msp.query('*[color==1 & linetype=="CENTER"]')#查找线条对象以红色，线型CENTER
    for e in centerlines:
        #  print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        e.set_dxf_attrib("layer","中心线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
    
    print ("查找所有螺纹线，设置图层为螺纹线层")
    threadlinesARC = msp.query('ARC [lineweight==13]').query('*[color==30]')#查找螺纹线对象
    for e in threadlinesARC:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        # print (e.dxftype())
        print ("起始角度",e.dxf.start_angle)
        print ("终止角度",e.dxf.end_angle)
        startangle=260.0 #参考caxa图形
        e.set_dxf_attrib("start_angle",startangle)  
        e.set_dxf_attrib("end_angle",startangle+290.0)  #start+290
        e.set_dxf_attrib("layer","螺纹线线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
    threadlines = msp.query('LINE [lineweight==13]').query('*[color==30]')#查找螺纹线对象
    for e in threadlines:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        # print (e.dxftype())
        # print ("起始角度",e.dxf.start_angle)
        # print ("终止角度",e.dxf.end_angle)
        # startangle=260.0 #参考caxa图形
        # e.set_dxf_attrib("start_angle",startangle)  
        # e.set_dxf_attrib("end_angle",startangle+290.0)  #start+290
        e.set_dxf_attrib("layer","螺纹线线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
    
    print ("查找所有虚线，设置图层为虚线层")
    dashes = msp.query('*[color==183 & lineweight==18]') #查找虚线线对象
    for e in dashes:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        e.set_dxf_attrib("layer","虚线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)

    print ("查找所有除修改层以外宋体文字对象，设置图层为文字图层,字符串高度为3.5")
    # text = msp.query('*[style=="宋体" & (!layer=="修改图层")]') #查找文字对象
    text = msp.query('MTEXT[(!layer=="修改图层")]') #查找文字对象
    for e in text:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        # print (e.text)
        # print (e.dxftype())
        e.text=e.text.replace("SECTION","") #修改尺寸文字，去掉所有空格
        e.set_dxf_attrib("layer","文字图层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
        e.set_dxf_attrib('char_height',3.5)

    print ("查找所有注释文字对象，设置图层为修改层,并且改成红色")
    inserts = msp.query('INSERT[name?"LABLE.*"]') #※使用正则表达式查找文字文字注释引用快对象※
    if len(inserts):
        for e in inserts:
            # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
            # print (e.dxftype())
            for blocklayoutents in e.block():
                # print ("当前Block下实体为",blocklayoutents.dxftype())
                blocklayoutents.set_dxf_attrib("layer","修改图层")  
                blocklayoutents.set_dxf_attrib("linetype","BYLAYER")  
                blocklayoutents.set_dxf_attrib("color",256)  
                blocklayoutents.set_dxf_attrib("lineweight",-1)

            e.set_dxf_attrib("layer","修改图层")  
            e.set_dxf_attrib("linetype","BYLAYER")  
            e.set_dxf_attrib("color",256)  
            e.set_dxf_attrib("lineweight",-1)

    print ("查找所有剖面线对象，设置图层为剖面线层")
    hatches = msp.query('INSERT HATCH[color==4]') #查找剖面线对象
    for e in hatches:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        e.set_dxf_attrib("layer","剖面线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)
     
    print ("查找所有折断线样条曲线对象，设置图层为细实线层")
    breaklines = msp.query('SPLINE[color==6]') #查找折断线对象
    for e in breaklines:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        # print (e.dxftype())
        e.set_dxf_attrib("layer","细实线层")  
        e.set_dxf_attrib("linetype","BYLAYER")  
        e.set_dxf_attrib("color",256)  
        e.set_dxf_attrib("lineweight",-1)

    # fg = msp.query('*[dimstyle=="标准"]')
    # for e in fg:
    #     print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute    

    print ("尺寸线型替换完毕")

    #删除不需要的对象
    # delent = msp.query('*[layer=="1" | layer=="170" | layer=="173" | layer=="10"|layer=="Defpoints"]') #删除不需要的线条
    # for e in delent:
    #     msp.delete_entity(e)
    for e in list(doc.tables.layers.entries.keys()): # 迭代变异报错使用list固定迭代列表https://blog.csdn.net/uncle_ll/article/details/120992227
        if e not in ('粗实线层','中心线层','尺寸线层','细实线层','虚线层', '剖面线层','修改图层','螺纹线线层','文字图层'):
            print (e)
            doc.layers.remove(e) #删除元素会导致被遍历的列表变化，所以报错
            querystr="*[layer==\"%s\"]" %(e)
            print (querystr)
            delent1= msp.query(querystr)
            for i in delent1:
                msp.delete_entity(i)
            
    print ("其余不需要实体删除完毕")

    # doc.layers.remove("0")
    # doc.layers.remove("1")
    # doc.layers.remove("170")
    # doc.layers.remove("171")
    # doc.layers.remove("173")
    # # doc.layers.remove("10")
    # # doc.layers.remove("2")
    # doc.layers.remove("Defpoints")
    print ("CAXA默认以外图层删除完毕")
    print ("打印当前文件包含的图层名称",doc.tables.layers.entries.keys()) 
    print("保存文件，如报错检查文件是否被别的软件打开被占用")
    doc.saveas('./output/'+fnout,"utf-8") 
    print ("保存完毕")
    print ("-----------------------------------------------------------")
    print("※检查样条曲线！！！！！！！！！！！！！！！！！！！！！！")
    print ("※重新添加剖切线，箭头等特殊符号，重新标注螺栓中心圆尺寸，重新标注单箭头尺寸，※检查样条曲线※，检查整个图形，删除多余的线条")
    



if __name__ == "__main__":  # 用作主程序时执行
    print ('This is main of module')
    main(filename,outputfile)
    print ("打开"+outputfile)
    os.startfile(r'.\output\%s' %(outputfile)) 
    
    
    
    

    
    
    
#---------------测试用\备用代码-------------------------------------------

    # # helper function  打印所有线条
    # def print_entity(e):
    #     print("LINE on layer: %s\n" % e.dxf.layer)
    #     print("start point: %s\n" % e.dxf.start)
    #     print("end point: %s\n" % e.dxf.end)

    # # iterate over all entities in modelspace
    # for e in msp:
    #     if e.dxftype() == "LINE":
    #         print_entity(e)

    # # entity query for all LINE entities in modelspace
    # for e in msp.query("LINE"):
    #     print_entity(e)
# chicun = msp.query('DIMENSION[color==3]')
#     for e in chicun:
#         # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
#         # print (e.get_dxf_attrib("color")) #打印颜色索引，绿色3
#         e.set_dxf_attrib("layer","尺寸线层")

# Reference: 
# https://ezdxf.readthedocs.io/en/stable/tutorials/layers.html
# https://ezdxf.readthedocs.io/en/stable/dxfentities/dxfgfx.html#common-graphical-dxf-attributes  图层颜色，线型，粗细，缺省设置
# https://ezdxf.readthedocs.io/en/stable/query.html#entity-query-string  Query查找实体方法 
# https://ezdxf.readthedocs.io/en/stable/query.html
# https://ezdxf.readthedocs.io/en/stable/dxfentities/hatch.html 所有dxf对象