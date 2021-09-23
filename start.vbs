set ws = createobject("wscript.shell")
ws.currentdirectory = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
ws.run "pythonw.exe main.py"