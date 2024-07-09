Set ws = CreateObject( "Wscript.Shell" )
ws.CurrentDirectory = "C:\scripts"

ws.run "py ""proc_test.py""", 1, True
WScript.Sleep 10000
