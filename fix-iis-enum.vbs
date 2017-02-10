'IIS 短文件名枚举漏洞修复，适用于Windows2003+IIS6环境。
'具体步骤如下:
'   一: 执行命令"fsutil behavior set disable8dot3 1", 随后重启系统;
'   二: 把该脚本放在网站根目录下并执行, 等待提示"执行完毕", 随后确认漏洞是否修复成功.

Function FixPath(sPath)      
    Set oFso = CreateObject("Scripting.FileSystemObject")    
    Set oFolder = oFso.GetFolder(sPath)    
    Set oSubFolders = oFolder.SubFolders
		
    Set oFiles = oFolder.Files    
    For Each oFile In oFiles    
		sTmp = oFile.path & ".x"
		sFile = oFile.path
		oFso.MoveFile sFile, sTmp
		oFso.MoveFile sTmp, sFile
    Next    
        
    For Each oSubFolder In oSubFolders 
		sTmp = oSubFolder & ".x"
		sFolder = oSubFolder.path
		oFso.MoveFolder sFolder, sTmp
		oFso.MoveFolder sTmp, sFolder
        FixPath(oSubFolder.Path) 
    Next    
        
    Set oFolder = Nothing    
    Set oSubFolders = Nothing    
    Set oFso = Nothing    
End Function    

path = Createobject("Scripting.FileSystemObject").GetFolder(".").Path
msg = VBcrlf
msg = "此工具针对IIS短文件名枚举漏洞进行修复，具有一定风险性，请在使用前做好备份!" 
msg = msg & VBcrlf & VBcrlf & VBcrlf & VBcrlf
msg = msg & "请确认网站路径: "
webdir = InputBox(msg, "警告", path)
If webdir=vbEmpty Then
	wscript.quit
End If
If webdir=path Then
	FixPath(webdir)
	MsgBox "执行完毕!"
Else
	MsgBox "路径不匹配!"
End If
