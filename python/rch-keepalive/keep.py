import pyautogui
import time
import random
import sys
import time

from datetime import datetime

# 実行時は Weatherである前提

LEFT_CLOSE = (595, 32)
LEFT_BOOT = (558, 1030)
RIGHT_CLOSE = (1304, 32)
RIGHT_BOOT = (508, 1030)

# type 1-2
LEFT_NEWS = (75, 760)
RIGHT_NEWS = (715, 750)
LEFT_WEATHER = (70, 850)
RIGHT_WEATHER = (700, 840)

# type 2-3
# LEFT_NEWS = (60, 850)
# RIGHT_NEWS = (715, 840)
# LEFT_WEATHER = (60, 930)
# RIGHT_WEATHER = (700, 920)

TAB_COUNT_CHROME = 12
TAB_COUNT_VIVALDI = 9

REBOOT_HOUR = (0, 12)

def refresh():
    time.sleep(0.7)
    pyautogui.press('f5')
    time.sleep(1.5)
    pyautogui.press('pageup')
    time.sleep(0.5)

def selectCategory(tabCount):
    for i in range(tabCount):
        pyautogui.press('tab')
        time.sleep(0.01)
    pyautogui.press('down')

def randDuration():
    return random.randint(10, 100) / 10

def reboot():
    pyautogui.click(LEFT_CLOSE)
    time.sleep(2)
    pyautogui.click(LEFT_BOOT)
    time.sleep(0.1)
    pyautogui.click(RIGHT_CLOSE)
    time.sleep(2)
    pyautogui.click(RIGHT_BOOT)
    time.sleep(0.1)

# 待機中はランダムにマウスを動かす
def randWaitTask():
    pyautogui.moveTo(2, 4, duration=randDuration())
    pyautogui.moveTo(10, 23, duration=randDuration())
    pyautogui.moveTo(236, 81, duration=randDuration())
    pyautogui.click(236, 10)

    loopCount = random.randint(1, 10)
    for i in range(loopCount):
        pyautogui.moveTo(random.randint(1, 200), random.randint(700, 1000), duration=randDuration())
        pyautogui.moveTo(random.randint(600, 800), random.randint(700, 1000), duration=randDuration())
        pyautogui.moveTo(random.randint(600, 800), random.randint(1, 300), duration=randDuration())

args = sys.argv
isAllowWait = True
isReboot = False

# なんらかの引数があるならテスト起動で待機なし
if (2 <= len(args)):
    isAllowWait = False
    # 引数が1なら再起動テスト
    if( args[1] == '1' ):
        isReboot = True
else:
    # 0時と12時に再起動
    current_time = datetime.now()
    if current_time.hour in REBOOT_HOUR:
        isReboot = True

if (isAllowWait):
    randWaitTask()

if(isReboot):
    reboot()

pyautogui.moveTo(LEFT_NEWS, duration=1)

# left news change
pyautogui.click(LEFT_NEWS)

refresh()
selectCategory(TAB_COUNT_CHROME)

pyautogui.moveTo(RIGHT_NEWS, duration=1)

# right news change
pyautogui.click(RIGHT_NEWS)

refresh()
selectCategory(TAB_COUNT_VIVALDI)

# いくらかの待機
wait_time = random.randint(60, 70)
if (isAllowWait):
    time.sleep(wait_time)
else:
    time.sleep(5)

# left weather change
pyautogui.click(LEFT_WEATHER)

refresh()
selectCategory(TAB_COUNT_CHROME)
time.sleep(0.2)

# right weather change
pyautogui.click(RIGHT_WEATHER)

refresh()
selectCategory(TAB_COUNT_VIVALDI)
