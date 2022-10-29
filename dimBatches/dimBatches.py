#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# ug转dxf局部放大图尺寸数值倍率批处理，先把需要修改的尺寸全部放进"尺寸数值批处理"层
# 变量处理 
filename="b.dxf"; outputfile="output_尺寸批处理.dxf"

# 引入包
import ezdxf, re

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

    print ("查找“尺寸批处理”层所有尺寸线，按照倍率修改该层的尺寸数值，此处报错检查是否有该图层")
    dimensions = msp.query('DIMENSION[layer=="尺寸批处理"]') #在绿色中查找尺寸对象
    for e in dimensions:
        # print (e.dxfattribs().items()) #获取所有可以使用的dxf属性attribute
        # print (e.get_dxf_attrib("color")) #打印颜色索引，绿色3
        # print(e.dxf.text, "尺寸结束")
        # print(e.dxf.text.replace(" <>","<>"))
        # e.dxf.text=e.dxf.text.replace(" <>","<>") #修改尺寸文字，去掉尺寸前空格
        if (round(e.get_measurement()/3,3)).is_integer():
            replaceTEXT=int(round(e.get_measurement()/3,3))
        else:
            replaceTEXT=round(e.get_measurement()/5,3)

        print ("打印实际尺寸",e.get_measurement())
        if "<>"in e.dxf.text:
            e.dxf.text=e.dxf.text.replace("<>",str(replaceTEXT))
        else: 
            e.dxf.text=replaceTEXT
        print ("打印修改后显示尺寸",replaceTEXT)
        # https://ezdxf.readthedocs.io/en/stable/tables/dimstyle_table_entry.html#ezdxf.entities.DimStyle

        if re.findall("[\u4e00-\u9fa5]",e.dxf.text):
            print ("包含中文的尺寸文字为:",e.dxf.text)
            dimstloverride=e.override()
            # dimstloverride.set_text_align(halign="above2") #,valign= "None"

    print("保存文件，如报错检查文件是否被别的软件打开被占用")
    doc.saveas(fnout,"utf-8") 


if __name__ == "__main__":  # 用作主程序时执行
    print ('This is main of module')
    main(filename,outputfile)