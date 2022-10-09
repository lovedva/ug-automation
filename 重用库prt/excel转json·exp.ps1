# 导出数据为 json 格式文本,用作数据库。导出EXP表达式文件(临时)，用作UG参数建模
# 用任务管理器杀掉excel进程
#-----------------------------------------------
# 设置文件名，文件与当前ps1脚本放在相同目录
$xlsName= "容器用重型B型鞍式支座.xlsm"
# 设置输出路径
$outputpathjson= $PSScriptRoot+"\json_output\"+$xlsName+".json"
$outputpathexp= $PSScriptRoot+"\json_output\"+"UG表达式文件（临时），用记事本看我"+".exp"
# 设置数据库名/位置 
$tbName="C2"
write-host "tbName "$tbName
# 设置表头行数起点和终点数组，0号为起点，1号为终点
$tbHead="B5","U5"
# 设置字段类型起点和终点，0号为起点，1号为终点
# $fieldClass="B3","P3"

# ※设置表内数据起点和终点※※※※※※※※※※※※※※※※※※※修改这里
$tbContent="B6","U15"
# ※设置exp表达式文件输出行id※※※
$id=9

# $xlFixedFormat = "Microsoft.Office.Interop.Excel.xlFixedFormatType" -as [type] #设置excel文件类型
$ExcelObj = New-Object -comobject Excel.Application
$ExcelObj.visible = $false 
$path = "$PSScriptRoot\$xlsName" #待打开文件
$workbook = $ExcelObj.workbooks.open($path) #获取工作簿对象
$ws=$workbook.WorkSheets.item("筋板x1") #获取工作表对象，也可以通过item("Sheet1")
# $workbook.activate()#激活工作簿
# $ws.activate()#激活工作表
# $workbook.save()#保存工作簿
# $workbook.saveas("C:\Users\Administrator\desktop\save.xlsx")#另存工作簿
# $workbook.close()#关闭工作簿
# $objExcel.Quit()#退出Excel程序

# 输出json文件
$jsondb = "[`n"

#遍历第一列中所有行（格子）:Range（左上角第一格，左下角最后一格），
foreach ($elemnt in $ws.Range($tbContent[0],$ws.Cells($ws.Range($tbContent[1]).Row,$ws.Range($tbContent[0]).Column))){
    $jsondb = $jsondb +"{ "
    #遍历行中每一格：Range（每行第一格，最后一格）
    foreach ($item in $ws.Range($ws.Cells($elemnt.Row,$elemnt.Column) , $ws.Cells($elemnt.Row,$ws.Range($tbContent[1]).Column))){
        # Write-Host $elemnt.Value2
        # Write-Output $item.Value2.GetType().Name
        if ($item.Value2.GetType().Name -eq "String"){ #判断获取表格的值（用作key）是否为字符串，如果是就加引号，否就不加
            # Write-Output $ws.Cells.Item($ws.Range($tbHead[0],$tbHead[1]).Row,$item.Column).Value2
            # ※※※ 最后一列在这里,保证最后一列一定是字符串
            if ($item.Column -eq $ws.Range($tbHead[1]).Column) {#判断是不是最后一列格子的元素，如果是，就不加最后的逗号
                $jsondb =$jsondb + ("`""+$ws.Cells.Item($ws.Range($tbHead[0],$tbHead[1]).Row,$item.Column).Value2+"`": `""+$item.value2+"`"")
            }else {
                $jsondb =$jsondb + ("`""+$ws.Cells.Item($ws.Range($tbHead[0],$tbHead[1]).Row,$item.Column).Value2+"`": `""+$item.value2+"`" , ")
            }
        }else {
            $jsondb =$jsondb + ("`""+$ws.Cells.Item($ws.Range($tbHead[0],$tbHead[1]).Row,$item.Column).Value2+"`":"+$item.value2+" , ")
            # Write-Host $ws.Range($tbHead[1]).Column "---" $item.Column "---"  $item.Value2
        }
    } #遍历行结束
    $jsondb = $jsondb +" },`n"
}    #遍历第一列结束

$jsondb = $jsondb+"]"
$jsondb = $jsondb -replace ',\n]', ("`n"+']') #去掉最后一行的逗号

Write-Output $jsondb

# 保存json文件
if ((Test-Path $outputpathjson) -eq "False"){
    New-Item $outputpathjson -Force
    $jsondb | Out-File -FilePath $outputpathjson -Force -Encoding utf8

}else {
    $jsondb | Out-File -FilePath $outputpathjson -Force -Encoding utf8
}


# 输出ug表达式的exp文件，对应prt参数化建模文件，版本ugnx2007或以上，临时凑合用下
$expdb="//  Version 2, "+$(Get-Date)+"  ※注意自动生成的exp的顺序是打乱的`n"
$jsonobj = Get-Content -Raw $outputpathjson | ConvertFrom-Json #解析json数据库
# Write-Host $jsonobj.psobject.properties.name
$keylist= ($jsonobj[$id]|Get-Member -MemberType NoteProperty | Select -ExpandProperty Name )
Write-Host $keylist[0], $keylist[1],$keylist.Count
for ($i = 0; $i -lt $keylist.Count; $i++) {# 拼接字符串，做exp文件输出准备
    if ($jsonobj[$id].($keylist[$i]) -eq "None") { #如果键值对的Value是None，就在前面加上表达式文件专用注释符号“//”
        $expdb=$expdb+"//[MilliMeter]"+$keylist[$i]+"="+$jsonobj[$id].($keylist[$i])+"`n"
    }elseif ($jsonobj[$id].($keylist[$i]).GetType().Name -eq "String") {# 如果键值对的Value是字符串，就加在两边加上引号，单位改成String
        $expdb=$expdb+"(String) "+$keylist[$i]+"=`""+$jsonobj[$id].($keylist[$i])+"`"`n"
    }else {#剩下参与建模的表达式，单位是MilliMeter
        $expdb=$expdb+"[MilliMeter]"+$keylist[$i]+"="+$jsonobj[$id].($keylist[$i])+"`n"
        # Write-Host $keylist[$i],$jsonobj[$id].($keylist[$i]), $jsonobj[$id].($keylist[$i]).GetType().Name     
    }
}

Write-Host $expdb


# 保存exp文件
if ((Test-Path $outputpathexp) -eq "False"){
    New-Item $outputpathexp -Force
    $expdb | Out-File -FilePath $outputpathexp -Force -Encoding utf8

}else {
    $expdb | Out-File -FilePath $outputpathexp -Force -Encoding utf8
}


$ExcelObj.Quit()
$workbook.Close($false)
$ws=$null
$workbook=$null
$ExcelObj=$null
[GC]::Collect()



# foreach ($item in $ws.range($tbContent[0],$tbContent[1])){
#     #  write-host $item.Value2,$item.Value2.GetType()
#     



# References
# https://blog.csdn.net/weixin_46846685/article/details/109131585
# https://blog.csdn.net/u010288731/article/details/83120205
# http://woshub.com/read-write-excel-files-powershell/
# 读写json https://www.jianshu.com/p/0affea9e0420
# 自定义对象键值对操作，https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-pscustomobject?view=powershell-7.2