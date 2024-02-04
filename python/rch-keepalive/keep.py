import pyautogui
import time
import random

# 実行時は Weatherである前提

def refresh():
    time.sleep(0.5)
    pyautogui.press('f5')

# left news change
pyautogui.click(75, 715)

refresh()
time.sleep(0.2)

# right news change
pyautogui.click(715, 750)

refresh()

# いくらかの待機
wait_time = random.randint(60, 70)
time.sleep(wait_time)

# left weather change
pyautogui.click(70, 870)

refresh()
time.sleep(0.2)

# right weather change
pyautogui.click(700, 905)

refresh()
