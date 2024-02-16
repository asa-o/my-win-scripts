import pyautogui
import time
import random

# 実行時は Weatherである前提

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

def refresh():
    time.sleep(0.5)
    pyautogui.press('f5')

pyautogui.moveTo(2, 4, duration=0.5)
pyautogui.moveTo(10, 23, duration=0.5)
pyautogui.moveTo(236, 81, duration=0.5)
pyautogui.click(236, 10)

wait_time = random.randint(1, 4)
time.sleep(wait_time)

pyautogui.moveTo(LEFT_NEWS, duration=1)

# left news change
pyautogui.click(LEFT_NEWS)

refresh()

pyautogui.moveTo(RIGHT_NEWS, duration=1)

# right news change
pyautogui.click(RIGHT_NEWS)

refresh()

# いくらかの待機
wait_time = random.randint(60, 70)
time.sleep(wait_time)

# left weather change
pyautogui.click(LEFT_WEATHER)

refresh()
time.sleep(0.2)

# right weather change
pyautogui.click(RIGHT_WEATHER)

refresh()
