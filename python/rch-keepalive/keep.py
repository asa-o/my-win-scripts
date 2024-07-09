import pyautogui
import time
import random
import sys
import time
import numpy as np
import cv2

from datetime import datetime
from datetime import timedelta

import os
import portalocker
import sys

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

SCREENSHOT_DIR = "screenshots"

# スクリーンショット範囲の指定 (左上のx座標, 左上のy座標, 幅, 高さ)
REGION_LEFT = (10, 230, 590, 340)
REGION_RIGHT = (625, 220, 680, 390)

TIMESTAMP_FILE = "lastRefresh.lockfile"


def acquire_lock_and_read_timestamp():
    if not os.path.exists(TIMESTAMP_FILE):
        open(TIMESTAMP_FILE, 'w').close()
        print(f"ファイル {TIMESTAMP_FILE} が存在しなかったため、新規作成しました。")

    file = open(TIMESTAMP_FILE, 'r+')

    try:
        portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    except portalocker.exceptions.LockException:
        file.close()
        print("別のインスタンスが実行中です。終了します。")
        exit(1)

    # タイムスタンプを読み取る
    file.seek(0)
    timestamp_str = file.read().strip()

    if timestamp_str:
        return file, datetime.fromisoformat(timestamp_str)
    else:
        return file, None

def release_lock(file):
    portalocker.unlock(file)
    file.close()
    
def write_timestamp(file):
    current_time = datetime.now().isoformat()
    file.seek(0)
    file.truncate()
    file.write(current_time)
    file.flush()
    os.fsync(file.fileno())

def save_screenshot(screenshot, filename):
    cv2.imwrite(filename, screenshot)

def screen_diff(region, name, threshold=1000):
    # 前回のスクリーンショットの読み込み
    prev_screenshot_path = os.path.join(SCREENSHOT_DIR, f"prev_{name}.png")
    if os.path.exists(prev_screenshot_path):
        prev_screenshot = cv2.imread(prev_screenshot_path)
    else:
        prev_screenshot = None

    current_screenshot = pyautogui.screenshot(region=region)
    current_screenshot = cv2.cvtColor(np.array(current_screenshot), cv2.COLOR_RGB2BGR)
    
    # 現在のスクリーンショットを次回用に保存
    save_screenshot(current_screenshot, prev_screenshot_path)

    if prev_screenshot is None:
        return True, current_screenshot

    diff = cv2.absdiff(prev_screenshot, current_screenshot)
    non_zero_count = np.count_nonzero(diff)

    if non_zero_count <= threshold:
        filename = datetime.now().strftime(f"{name}_%Y%m%d_%H%M%S.png")
        save_screenshot(current_screenshot, os.path.join(SCREENSHOT_DIR, filename))
        print(f"{name} No change detected, current screen saved as", filename)
        return False

    return True

def refresh():
    time.sleep(0.7)
    pyautogui.press('f5')
    time.sleep(1.5)
    pyautogui.press('pageup')
    time.sleep(0.5)

def select_category(tabCount):
    for i in range(tabCount):
        pyautogui.press('tab')
        time.sleep(0.01)
    pyautogui.press('down')

    pyautogui.press('tab')
    time.sleep(0.01)
    pyautogui.press('down')

    pyautogui.press('tab')
    pyautogui.press('pageup')

def rand_duration():
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
def rand_wait_task():
    pyautogui.moveTo(2, 4, duration=rand_duration())
    pyautogui.moveTo(10, 23, duration=rand_duration())
    pyautogui.moveTo(236, 81, duration=rand_duration())
    pyautogui.click(236, 10)

    loopCount = random.randint(1, 10)
    for i in range(loopCount):
        pyautogui.moveTo(random.randint(1, 200), random.randint(700, 1000), duration=rand_duration())
        pyautogui.moveTo(random.randint(600, 800), random.randint(700, 1000), duration=rand_duration())
        pyautogui.moveTo(random.randint(600, 800), random.randint(1, 300), duration=rand_duration())

def refresh_and_select_category():
    # left weather change
    pyautogui.click(LEFT_WEATHER)

    refresh()
    select_category(TAB_COUNT_CHROME)
    time.sleep(0.2)

    # right weather change
    pyautogui.click(RIGHT_WEATHER)

    refresh()
    select_category(TAB_COUNT_VIVALDI)

def keep_alive(isAllowWait, isReboot):
    if (isAllowWait):
        rand_wait_task()

    if(isReboot):
        reboot()

    pyautogui.moveTo(LEFT_NEWS, duration=1)

    # left news change
    pyautogui.click(LEFT_NEWS)

    refresh()
    select_category(TAB_COUNT_CHROME)

    pyautogui.moveTo(RIGHT_NEWS, duration=1)

    # right news change
    pyautogui.click(RIGHT_NEWS)

    refresh()
    select_category(TAB_COUNT_VIVALDI)

    # いくらかの待機
    wait_time = random.randint(60, 70)
    if (isAllowWait):
        time.sleep(wait_time)
    else:
        time.sleep(5)

    # left weather change
    pyautogui.click(LEFT_WEATHER)

    refresh()
    select_category(TAB_COUNT_CHROME)
    time.sleep(0.2)

    # right weather change
    pyautogui.click(RIGHT_WEATHER)

    refresh()
    select_category(TAB_COUNT_VIVALDI)

def is_90_minute_interval(time):
    reference_time = datetime(time.year, time.month, time.day, 0, 0, 0)
    time_difference = time - reference_time
    minutes_passed = time_difference.total_seconds() / 60
    return minutes_passed % 90 < 2

def main():
    try:
        file, last_execution = acquire_lock_and_read_timestamp()
        args = sys.argv
        isKeepAlive = False
        isAllowWait = True
        isReboot = False

        # ディレクトリの確認と作成
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)

        current_time = datetime.now()

        # なんらかの引数があるならテスト起動で待機なし
        if (2 <= len(args)):
            isKeepAlive = True
            isAllowWait = False
            # 引数が1なら再起動テスト
            if( args[1] == '1' ):
                isReboot = True
        else:   # 1分ごとの通常起動
            # 90分ごとにkeepalive処理
            if is_90_minute_interval(current_time):
                isKeepAlive = True
                # 0時と12時には再起動
                if current_time.hour in REBOOT_HOUR:
                    isReboot = True

        if isKeepAlive:
            keep_alive(isAllowWait, isReboot)
        else:
            if last_execution is None:
                print("初回実行または前回の実行時刻が見つかりません。処理を実行します。")
                refresh_and_select_category()
                write_timestamp(file)
            else:
                time_diff = current_time - last_execution
                if time_diff >= timedelta(seconds=510):
                    print(f"前回の実行から{time_diff.total_seconds() / 60:.2f}分経過しました。処理を実行します。")
                    refresh_and_select_category()
                    write_timestamp(file)

                else:
                    # スクリーンショットの比較
                    left_changed = screen_diff(REGION_LEFT, "left")
                    right_changed = screen_diff(REGION_RIGHT, "right")

                    if left_changed == False or right_changed == False:
                        # 画面が変わっていなかったらエラーなどの可能性があるので 待機なしで再起動
                        print("no changed")
                        keep_alive(False, True)

                    print(f"前回の実行からまだ{time_diff.total_seconds() / 60:.2f}分しか経過していません。")

    finally:
        if 'file' in locals():
            release_lock(file)

if __name__ == "__main__":
    main()
