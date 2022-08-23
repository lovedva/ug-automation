#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# 批量转dxf

import hellowolrd,os

if __name__=="__main__":
    for files in os.listdir(os.getcwd()):
        if files.find(".dxf")!=-1:
            print("当前dxf文件：",files)
            print("用helloword调整线型")
            hellowolrd.main(files,files)
            print("dxfall执行结束--------------------------------")
