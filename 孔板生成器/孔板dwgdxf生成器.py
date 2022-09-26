#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# 变量处理 
filename="1.dxf"; outputfile="ug用孔板参数.dxf"

# 引入包
import ezdxf, os

doc = ezdxf.new('R2007')  # create a new DXF R2007 drawing, 

msp = doc.modelspace()  # add new entities to the modelspace
msp.add_line((0, 0), (500, 0))  # add a LINE entity
doc.saveas('./output/line.dxf',"utf-8")
os.startfile('.\output\line.dxf') 













# Reference:
# 参考Hello World