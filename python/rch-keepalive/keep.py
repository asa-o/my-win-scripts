import pyautogui
import time
import random

# 実行時は Weatherである前提

# left news change
pyautogui.click(75, 715)

time.sleep(1)

# right news change
pyautogui.click(715, 750)

# いくらかの待機
wait_time = random.randint(60, 70)
time.sleep(wait_time)

# left weather change
pyautogui.click(70, 870)

time.sleep(1)

# right weather change
pyautogui.click(700, 905)
