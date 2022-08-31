# 导出数据为 json 格式文本,用作数据库
# 设置文件名，文件与当前ps1脚本放在相同目录
$xlsName= "容器用重型B型鞍式支座.xlsm"
# 设置输出路径
$outputpath= $PSScriptRoot+"\json_output\"+$xlsName+".txt"
# 设置数据库名/位置
$tbName="C2"
write-host "tbName"$tbName
# 设置表头行数起点和终点，0号为起点，1号为终点
$tbHead="B5","P5"
# 设置表内数据起点和终点
$tbContent="B6","P16"

# $xlFixedFormat = "Microsoft.Office.Interop.Excel.xlFixedFormatType" -as [type] #设置excel文件类型
$ExcelObj = New-Object -comobject Excel.Application
$ExcelObj.visible = $false 
$path = "$PSScriptRoot\$xlsName" #待打开文件
$workbook = $ExcelObj.workbooks.open($path) #获取工作簿对象
$ws=$workbook.WorkSheets.item("筋板x1")#获取工作表对象，也可以通过item("Sheet1")
# $workbook.activate()#激活工作簿
# $ws.activate()#激活工作表
# $workbook.save()#保存工作簿
# $workbook.saveas("C:\Users\Administrator\desktop\save.xlsx")#另存工作簿
# $workbook.close()#关闭工作簿
# $objExcel.Quit()#退出Excel程序



#遍历列
$jsondb = "`n"
foreach ($elemnt in $ws.Range($tbContent[0],$ws.Cells($ws.Range($tbContent[1]).Row,$ws.Range($tbContent[0]).Column))){
    $jsondb = $jsondb +"{ "
#遍历行
    foreach ($item in $ws.Range($ws.Cells($elemnt.Row,$elemnt.Column) , $ws.Cells($elemnt.Row,$ws.Range($tbContent[1]).Column))){
        # Write-Host $elemnt.Value2
        $jsondb =$jsondb + ("`""+$ws.Cells.Item($ws.Range($tbHead[0],$tbHead[1]).Row,$item.Column).Value2+"`":"+$item.value2+" , ")
    } #遍历行结束
    $jsondb = $jsondb +" },`n"
}    #遍历列结束

Write-Output $jsondb

Write-Output (Test-Path $outputpath)

New-Item $outputpath -Force
$jsondb | Out-File -FilePath $outputpath -Force -Encoding utf8



# foreach ($item in $ws.range($tbContent[0],$tbContent[1])){
#     #  write-host $item.Value2,$item.Value2.GetType()
#     



# References
# https://blog.csdn.net/weixin_46846685/article/details/109131585
# https://blog.csdn.net/u010288731/article/details/83120205
# http://woshub.com/read-write-excel-files-powershell/