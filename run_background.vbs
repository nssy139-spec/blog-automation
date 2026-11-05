Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = scriptDir
' 0: 창 숨김(완전 백그라운드), False: 비동기 실행
WshShell.Run "cmd /c start_server.bat", 0, False
Set WshShell = Nothing
Set fso = Nothing
