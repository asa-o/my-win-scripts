Set ws = CreateObject( "Wscript.Shell" )
ws.CurrentDirectory = "C:\scripts"

ws.run "py ""screenshot.py""", vbhide
