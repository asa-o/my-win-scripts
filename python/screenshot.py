import pyautogui

def take_screenshot_and_save(file_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

file_path = "screenshot.png"
take_screenshot_and_save(file_path)
