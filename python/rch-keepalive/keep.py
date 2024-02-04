import pyautogui
import time
import random

# 実行時は Weatherである前提

def refresh():
    time.sleep(0.5)
    pyautogui.press('f5')

pyautogui.moveTo(2, 4, duration=0.5)
pyautogui.moveTo(10, 23, duration=0.5)
pyautogui.moveTo(236, 81, duration=0.5)
pyautogui.click(236, 10)

wait_time = random.randint(1, 4)
time.sleep(wait_time)

pyautogui.moveTo(75, 715, duration=1)

# left news change
pyautogui.click(75, 715)

refresh()

pyautogui.moveTo(715, 750, duration=1)

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
