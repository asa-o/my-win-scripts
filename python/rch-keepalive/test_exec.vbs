Set ws = CreateObject( "Wscript.Shell" )
ws.CurrentDirectory = "C:\scripts"

ws.run "py ""keep.py"" 0", vbhide
