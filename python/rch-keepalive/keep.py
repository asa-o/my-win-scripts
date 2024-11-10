import sys

sys.dont_write_bytecode = True

import pyautogui
import time
import random
import time
import numpy as np
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import settings

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

# 算出に失敗した場合のデフォルト値
LEFT_BASE_POINT_DEFAULT = (50, 780)
RIGHT_BASE_POINT_DEFAULT = (666, 830)

# 各ch 基準点からの座標
LEFT_NEWS = (102, 28)
RIGHT_NEWS = (98, 26)
LEFT_WEATHER = (102, 113)
RIGHT_WEATHER = (98, 116)

TAB_COUNT_FROM = 7
TAB_COUNT_TRIAL = 8

# REBOOT_HOUR = (0, 12)
REBOOT_HOUR = (0,)

# REFRESH_INTERVAL = 7200  # 一時的に更新処理なしにしてみる 510
REFRESH_INTERVAL = 510

SCREENSHOT_DIR = "screenshots"

# スクリーンショット範囲の指定 (左上のx座標, 左上のy座標, 幅, 高さ)
REGION_LEFT = (10, 230, 590, 340)
REGION_RIGHT = (625, 220, 680, 390)

TIMESTAMP_FILE = "lastRefresh.lockfile"


def find_image(image_path, region, confidence=0.8):
    # 画像の位置を探す
    try:
        location = pyautogui.locateOnScreen(
            image_path, region=region, confidence=confidence
        )
        if location:
            print(location)
            return (location.left, location.top)
        else:
            print(f"Image {image_path} not found on screen.")
    except:
        print(f"Image {image_path} not found on screen.")

    return (-1, -1)


def mail_send(subject, body):
    msg = MIMEMultipart()
    msg["From"] = settings.from_email
    msg["To"] = settings.to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.from_email, settings.to_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


def acquire_lock_and_read_timestamp():
    if not os.path.exists(TIMESTAMP_FILE):
        open(TIMESTAMP_FILE, "w").close()
        print(f"ファイル {TIMESTAMP_FILE} が存在しなかったため、新規作成しました。")

    file = open(TIMESTAMP_FILE, "r+")

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
    pyautogui.press("f5")
    time.sleep(1.5)
    pyautogui.press("pageup")
    time.sleep(0.5)


def select_category():
    for i in range(TAB_COUNT_FROM):
        pyautogui.press("tab")
        time.sleep(0.01)

    for i in range(TAB_COUNT_TRIAL):
        pyautogui.press("down")
        pyautogui.press("tab")
        time.sleep(0.01)

    pyautogui.press("pageup")


def rand_duration():
    return random.randint(10, 100) / 10


def reboot():
    pyautogui.click(LEFT_CLOSE)
    time.sleep(2.5)
    pyautogui.click(LEFT_BOOT)
    time.sleep(0.3)
    pyautogui.click(RIGHT_CLOSE)
    time.sleep(2.5)
    pyautogui.click(RIGHT_BOOT)
    time.sleep(0.3)


# 待機中はランダムにマウスを動かす
def rand_wait_task():
    pyautogui.moveTo(2, 4, duration=rand_duration())
    pyautogui.moveTo(10, 23, duration=rand_duration())
    pyautogui.moveTo(236, 81, duration=rand_duration())
    pyautogui.click(236, 10)

    loopCount = random.randint(1, 10)
    for i in range(loopCount):
        pyautogui.moveTo(
            random.randint(1, 200), random.randint(700, 1000), duration=rand_duration()
        )
        pyautogui.moveTo(
            random.randint(600, 800),
            random.randint(700, 1000),
            duration=rand_duration(),
        )
        pyautogui.moveTo(
            random.randint(600, 800), random.randint(1, 300), duration=rand_duration()
        )


def refresh_and_select_category():
    left_base_point = find_image(
        "./logo/nnn_logo.png", (0, 450, 600, 600), confidence=0.9
    )
    if left_base_point[0] == -1:
        left_base_point = LEFT_BASE_POINT_DEFAULT

    right_base_point = find_image(
        "./logo/nnn_logo.png", (600, 450, 700, 600), confidence=0.9
    )
    if right_base_point[0] == -1:
        right_base_point = RIGHT_BASE_POINT_DEFAULT

    # left weather change
    pyautogui.click(
        LEFT_WEATHER[0] + left_base_point[0], LEFT_WEATHER[1] + left_base_point[1]
    )

    refresh()
    select_category()
    time.sleep(0.2)

    # right weather change
    pyautogui.click(
        RIGHT_WEATHER[0] + right_base_point[0], RIGHT_WEATHER[1] + right_base_point[1]
    )

    refresh()
    select_category()


def keep_alive(isAllowWait, isReboot):
    if isAllowWait:
        rand_wait_task()

    if isReboot:
        reboot()

    left_base_point = find_image(
        "./logo/nnn_logo.png", (0, 450, 600, 600), confidence=0.9
    )
    if left_base_point[0] == -1:
        left_base_point = LEFT_BASE_POINT_DEFAULT

    pyautogui.moveTo(
        x=LEFT_NEWS[0] + left_base_point[0],
        y=LEFT_NEWS[1] + left_base_point[1],
        duration=1,
    )

    # left news change
    pyautogui.click(
        x=LEFT_NEWS[0] + left_base_point[0], y=LEFT_NEWS[1] + left_base_point[1]
    )

    refresh()
    select_category()

    right_base_point = find_image(
        "./logo/nnn_logo.png", (600, 450, 700, 600), confidence=0.9
    )
    if right_base_point[0] == -1:
        right_base_point = RIGHT_BASE_POINT_DEFAULT

    pyautogui.moveTo(
        x=RIGHT_NEWS[0] + right_base_point[0],
        y=RIGHT_NEWS[1] + right_base_point[1],
        duration=1,
    )

    # right news change
    pyautogui.click(
        x=RIGHT_NEWS[0] + right_base_point[0], y=RIGHT_NEWS[1] + right_base_point[1]
    )

    refresh()
    select_category()

    # いくらかの待機
    wait_time = random.randint(60, 70)
    if isAllowWait:
        time.sleep(wait_time)
    else:
        time.sleep(5)

    left_base_point = find_image(
        "./logo/nnn_logo.png", (0, 450, 600, 600), confidence=0.9
    )
    if left_base_point[0] == -1:
        left_base_point = LEFT_BASE_POINT_DEFAULT

    right_base_point = find_image(
        "./logo/nnn_logo.png", (600, 450, 700, 600), confidence=0.9
    )
    if right_base_point[0] == -1:
        right_base_point = RIGHT_BASE_POINT_DEFAULT

    # left weather change
    pyautogui.click(
        LEFT_WEATHER[0] + left_base_point[0], LEFT_WEATHER[1] + left_base_point[1]
    )

    refresh()
    select_category()
    time.sleep(0.2)

    # right weather change
    pyautogui.click(
        RIGHT_WEATHER[0] + right_base_point[0], RIGHT_WEATHER[1] + right_base_point[1]
    )

    refresh()
    select_category()


def is_90_minute_interval(time):
    reference_time = datetime(time.year, time.month, time.day, 0, 0, 0)
    time_difference = time - reference_time
    minutes_passed = time_difference.total_seconds() / 60
    return minutes_passed % 90 < 2


def main():
    try:
        file, last_execution = acquire_lock_and_read_timestamp()
        args = sys.argv
        is_keep_alive = False
        is_allow_wait = True
        is_reboot = False

        # ディレクトリの確認と作成
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)

        current_time = datetime.now()

        # なんらかの引数があるならテスト起動で待機なし
        if 2 <= len(args):
            is_keep_alive = True
            is_allow_wait = False
            # 引数が1なら再起動テスト
            if args[1] == "1":
                is_reboot = True
            elif args[1] == "find_image":
                print("left logo find_image")
                find_image("./logo/nnn_logo.png", (0, 450, 600, 600), confidence=0.9)
                print("right logo find_image")
                find_image("./logo/nnn_logo.png", (600, 450, 700, 600), confidence=0.9)
                return
        else:  # 1分ごとの通常起動
            # 90分ごとにkeepalive処理
            if is_90_minute_interval(current_time):
                is_keep_alive = True

                # 定期的な再起動はしばらく保留
                # 0時には再起動
                # if current_time.hour in REBOOT_HOUR:
                #     is_reboot = True

        if is_keep_alive:
            keep_alive(is_allow_wait, is_reboot)
            write_timestamp(file)
        else:
            if last_execution is None:
                print(
                    "初回実行または前回の実行時刻が見つかりません。処理を実行します。"
                )
                refresh_and_select_category()
                write_timestamp(file)
            else:
                time_diff = current_time - last_execution
                if time_diff >= timedelta(seconds=REFRESH_INTERVAL):
                    print(
                        f"前回の実行から{time_diff.total_seconds() / 60:.2f}分経過しました。処理を実行します。"
                    )
                    refresh_and_select_category()
                    write_timestamp(file)

                else:
                    # スクリーンショットの比較
                    left_changed = screen_diff(REGION_LEFT, "left")
                    right_changed = screen_diff(REGION_RIGHT, "right")

                    if left_changed == False or right_changed == False:
                        # 画面が変わっていなかったらエラーなどの可能性があるので 待機なしで再起動
                        mail_send(
                            settings.error_subject,
                            settings.error_screen_not_changed_body,
                        )
                        print("no changed")
                        keep_alive(False, True)
                        write_timestamp(file)

                    print(
                        f"前回の実行からまだ{time_diff.total_seconds() / 60:.2f}分しか経過していません。"
                    )
    except Exception as e:
        mail_send(
            settings.error_subject,
            settings.error_script_execution_body,
        )

    finally:
        if "file" in locals():
            release_lock(file)


if __name__ == "__main__":
    main()
