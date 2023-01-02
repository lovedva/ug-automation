#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# dxf批量修改图框属性，页码等
# 引入包
import ezdxf, os,re
# 变量处理 
logFileDir=os.getcwd()+r"\editFrameAttitudes_py.log"
filename=os.getcwd()+r"\1.dxf"; outputfile="editFrame_output.dxf"


def main(fn,fnout):
    print_log = open(logFileDir,'w')
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
    
    # 查找所有insert（Block引用）
    print ("查找所有insert（Block引用）")
    inserts = msp.query('INSERT[name?".*FRAME.*"]')  #[name?".*FRAME.*"]
    if len(inserts):
        print ("查找insert包含结果：")
        for e in inserts:
            print ("当前包含属性：",e.dxfattribs().items(),file = print_log) #获取所有可以使用的dxf属性attribute
            print ("当前对象类型：",e.dxftype(),file = print_log)
            for attrib in e.attribs:
                    if  re.search(".*页.*",attrib.dxf.tag):  # identify attribute by tag
                        attrib.dxf.text=255
                        print (attrib.dxf.text)
            for blocklayoutents in e.block(): 
                print ("当前Block下实体为",blocklayoutents.dxftype(),file = print_log)
                 # change attribute content
                # if blocklayoutents.dxftype()=="MTEXT":
                #     print (blocklayoutents.dxf.text)
                # blocklayoutents.set_dxf_attrib("layer","修改图层")  
                # blocklayoutents.set_dxf_attrib("linetype","BYLAYER")  
                # blocklayoutents.set_dxf_attrib("color",256)  
                # blocklayoutents.set_dxf_attrib("lineweight",-1)
            
            # e.set_dxf_attrib("layer","修改图层")  
            # e.set_dxf_attrib("linetype","BYLAYER")  
            # e.set_dxf_attrib("color",256)  
            # e.set_dxf_attrib("lineweight",-1)


    print_log.close()
    doc.saveas('./output/'+fnout,"utf-8") 


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