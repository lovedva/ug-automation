

Write-Host "# 压力容器计算脚本，主程序目录" $PSScriptRoot
# 计算 "1.筒体端部计算"
    ##用户输入
$Di_管内径=180; $D2_加工内径=$Di_管内径+3; $db_螺栓M=20 
    ##计算  
$Db_主螺栓中心圆直径=190 #$D2_加工内径+1.5*$db_螺栓M
$D0_筒体外部端径= $Db_主螺栓中心圆直径+1.8*$db_螺栓M
    ##显示控制
Write-Host "筒体端部计算------"
Write-Host "用户输入：Di_管内径="$Di_管内径，"db_螺栓M="$db_螺栓M
Write-Host "计算结果："
Write-Host "Db_主螺栓中心圆直径≥"$Db_主螺栓中心圆直径
Write-Host "D0_筒体外部端径≥"$D0_筒体外部端径"mm"

cd $PSScriptRoot
ii "./src/整体法兰结构.png"
ii "./src/筒体端部结构.png"

#  Pause

# Windows Forms 控制，GUI显示相关
# 引入依赖包
# Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing
# $PSForms = New-Object System.Windows.Forms.Form
# $imageList1 = New-Object System.Windows.Forms.ImageList
# $imageList1.Images.Add([system.drawing.image]::FromFile("src/整体法兰结构.png"));
# $imageList1.Images.Add([system.drawing.image]::FromFile("src/筒体端部结构.png"));
# $Images = [system.drawing.image]::FromFile("src/筒体端部结构.png")
# $PSForms.BackgroundImage = $imageList1.Images[0]
# $PSForms.BackgroundImageLayout = "Zoom" # https://docs.microsoft.com/en-us/dotnet/api/system.windows.forms.imagelayout?view=windowsdesktop-6.0#system-windows-forms-imagelayout-zoom
# $PSForms.Width = 420
# $PSForms.Height = 360
# $PSForms.ShowDialog()


#Reference
# PShellGUI https://blog.csdn.net/melodytu/article/details/49977419
# Imagelist https://docs.microsoft.com/en-us/dotnet/api/system.windows.forms.imagelist?view=windowsdesktop-6.0