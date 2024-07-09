import win32event
import win32api
import winerror

mutex_name = "Global\\MyPythonScript"

mutex = win32event.CreateMutex(None, False, mutex_name)
last_error = win32api.GetLastError()

if last_error == winerror.ERROR_ALREADY_EXISTS:
    print("別のインスタンスが既に実行中です")
else:
    # スクリプトの主要な処理をここに記述
    print("スクリプトが実行されています")
    
    # 処理が終わったらミューテックスを解放
user_input = input("press enter to exit\n")
win32api.CloseHandle(mutex)
    
