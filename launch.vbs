Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\MES PROJETS WEB\Projet Python\Graden IA"
WshShell.Run "python graden.py", 1, True
