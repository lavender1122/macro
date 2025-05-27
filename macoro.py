### macro.py
import traceback

from pynput import keyboard
import pyautogui
import time
from numpy import array
import pytesseract
from PIL import Image

# ------------------- 설정 -------------------
target_img = "target.png"
target_img2 = "500.png"
autobtn_img = "autobtn.png"
plusbtn_img = "plusbtn.png"
confirm_button_img = "confirm_button.png"
threshold = 0.7


def color_match(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))


def click_target_img_by_image():
    location = pyautogui.locateCenterOnScreen(target_img, confidence=threshold)
    if location:
        pyautogui.click(location)
        print(f"좌석 선택 완료 버튼 클릭: {location}")
        return True  # ✅ 이 줄이 꼭 있어야 함!
    else:
        print("버튼 이미지를 찾지 못했습니다.")


def click_confirm_button_by_image():
    location = pyautogui.locateCenterOnScreen(confirm_button_img, confidence=threshold)
    if location:
        pyautogui.click(location)
        print(f"다음단계 완료 버튼 클릭: {location}")
    else:
        print("버튼 이미지를 찾지 못했습니다.")

# ------------------- 단축키 리스너 -------------------

def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l:
            print("option 눌림 → 매크로 실행")
            click_target_img_by_image()

        elif key == keyboard.Key.alt_l:
            print("alt 눌림 → 매크로 실행")
            click_confirm_button_by_image()

        else:
            print("→ plusbtn.png 인식 실패로 중단")

    except Exception as e:
        print("오류 발생:", e)
        traceback.print_exc()


print("⌨️ option 키를 누르면 매크로가 실행됩니다. 종료하려면 Ctrl+C.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
