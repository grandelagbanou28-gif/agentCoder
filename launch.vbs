Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\MES PROJETS WEB\Projet Python\Graden IA"
WshShell.Run "pythonw graden_app.py", 0, False
