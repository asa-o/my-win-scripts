import requests
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright


def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("エラー: config.json が見つかりません。")
        return None
    except json.JSONDecodeError:
        print("エラー: config.json の形式が正しくありません。")
        return None


def check_website(url, keyword, launch_args):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=launch_args)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            content = page.content()
            browser.close()
            return keyword in content
    except Exception as e:
        print(f"エラー: サイト取得に失敗しました - {e}")
        return None


def send_notification(webhook_url, payload):
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("通知を送信しました。")
    except requests.exceptions.RequestException as e:
        print(f"エラー: 通知の送信に失敗しました - {e}")


def main():
    config = load_config()
    if not config:
        return

    target_url = config.get("target_url")
    search_keyword = config.get("search_keyword")
    webhook_url = config.get("webhook_url")
    hit_payload = config.get("hit_payload")
    not_hit_payload = config.get("not_hit_payload")
    min_interval = config.get("min_interval_seconds", 60)
    max_interval = config.get("max_interval_seconds", 120)

    # ウィンドウ設定
    width = config.get("window_width", 1280)
    height = config.get("window_height", 720)
    x = config.get("window_x", 0)
    y = config.get("window_y", 0)
    launch_args = [f"--window-size={width},{height}", f"--window-position={x},{y}"]

    if not all([target_url, search_keyword, webhook_url, hit_payload, not_hit_payload]):
        print("エラー: 設定ファイルに必要な項目が不足しています。")
        return

    last_status_was_hit = None

    print("監視を開始します...")

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {target_url} をチェックしています...")

        is_hit = check_website(target_url, search_keyword, launch_args)

        if is_hit is None:
            pass
        elif is_hit:
            print(f"-> キーワード '{search_keyword}' が見つかりました。")
            if last_status_was_hit != True:
                send_notification(webhook_url, hit_payload)
                last_status_was_hit = True
            else:
                print("-> 状態に変化がないため、通知はスキップします。")
        else:
            print(f"-> キーワード '{search_keyword}' は見つかりませんでした。")
            if last_status_was_hit != False:
                send_notification(webhook_url, not_hit_payload)
                last_status_was_hit = False
            else:
                print("-> 状態に変化がないため、通知はスキップします。")

        wait_time = random.randint(min_interval, max_interval)
        print(f"次のチェックまで {wait_time} 秒待機します.\n")
        for remaining in range(wait_time, 0, -1):
            if remaining % 10 == 0 or remaining <= 5:
                print(f"残り {remaining} 秒...")
            time.sleep(1)


if __name__ == "__main__":
    main()
