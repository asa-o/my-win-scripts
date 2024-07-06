import pyautogui
import numpy as np
import cv2
import time
from datetime import datetime
import os

SAVE_DIR = "screenshots"

# スクリーンショット範囲の指定 (左上のx座標, 左上のy座標, 幅, 高さ)
REGION_LEFT = (10, 230, 590, 340)
REGION_RIGHT = (625, 220, 680, 390)

def save_screenshot(screenshot, filename):
    cv2.imwrite(filename, screenshot)

def screen_diff(region, name, threshold=1000):
    # 前回のスクリーンショットの読み込み
    prev_screenshot_path = os.path.join(SAVE_DIR, f"prev_{name}.png")
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
        save_screenshot(current_screenshot, os.path.join(SAVE_DIR, filename))
        print(f"{name} No change detected, current screen saved as", filename)
        return False

    return True

def main():

    # ディレクトリの確認と作成
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # スクリーンショットの比較
    left_changed = screen_diff(REGION_LEFT, "left")
    right_changed = screen_diff(REGION_RIGHT, "right")

    if left_changed == False or right_changed == False:
        print("no changed")

if __name__ == "__main__":
    main()
