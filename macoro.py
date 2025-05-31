import traceback
import time
from datetime import datetime, timedelta,timezone
import urllib.request

import pyautogui
from pynput import keyboard

# ------------------- 설정 -------------------
URL = 'https://www.ticketlink.co.kr/home' # 서버시간url
THRESHOLD = 0.7 #유사도
# 좌석도 선택 이미지
IMG_TARGET = "target2.png"
# 다음단계 이미지(구단마다 다음단계 색상다르니 결졔전 꼭 확인하세요)
IMG_CONFIRM = "confirm_button.png"

# ------------------- 이미지 클릭 함수 -------------------
def click_image(image_path, description):
    try:
        print(f"→ {description} 탐색 시작")
        location = pyautogui.locateCenterOnScreen(image_path, confidence=THRESHOLD)
        if location:
            pyautogui.click(location)
            print(f"✅ {description} 클릭 완료: {location}")
            return True
        else:
            print(f"❌ {description} 이미지 찾지 못함.")
            return False
    except Exception as e:
        print(f"❗ 예외 발생 ({description}): {e}")
        return False

def click_target_img():
    return click_image(IMG_TARGET, "좌석 선택 버튼")

def click_confirm_button():
    return click_image(IMG_CONFIRM, "다음 버튼")

# ------------------- 서버 시간 확인 -------------------
# 1. 서버에서 시간 얻고, 밀리초 보정까지
def get_precise_kst_from_server():
    try:
        # 요청 전 시간 (UTC)
        start_perf = time.perf_counter()

        # 서버 요청
        req = urllib.request.Request(URL, method="HEAD")
        response = urllib.request.urlopen(req)
        date_str = response.headers['Date']  # 예: 'Sat, 31 May 2025 06:10:00 GMT'

        # 요청...
        end_perf = time.perf_counter()

        # 서버시간 → UTC 파싱
        server_utc = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)

        # 평균 지연 보정
        rtt = end_perf - start_perf
        delay = timedelta(seconds=rtt / 2)
        corrected_utc = server_utc + delay

        # KST = UTC + 9시간
        KST = timezone(timedelta(hours=9))
        kst_time = corrected_utc.astimezone(KST)
        return kst_time

    except Exception as e:
        print(f"서버 시간 가져오기 실패: {e}")
        return None

def wait_until_kst(target_kst):
    print(f"목표 시간 (KST): {target_kst}")

    while True:
        current_kst = get_precise_kst_from_server()
        if not current_kst:
            print("❌ 서버 시간 가져오기 실패")

        delta = (target_kst - current_kst).total_seconds()

        if delta <= 0:
            break

        print(f"\r⏳ 남은 시간: {delta:.3f}초", end="", flush=True)
        time.sleep(0.001)

    print("\n✅ 목표 시각(ms 포함)에 도달 → 엔터 누름")
    pyautogui.press('enter')

# ------------------- 단축키 리스너 -------------------
def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l:
            print("⌨️ Ctrl → 매크로 실행")
            click_target_img()

        elif key == keyboard.Key.alt_l:
            print("⌨️ Alt → 다음버튼 클릭 실행")
            click_confirm_button()
    except Exception as e:
        print("키 입력 처리 중 오류:", e)
        traceback.print_exc()

# ------------------- 실행 -------------------
if __name__ == "__main__":
    print("⌨️ Ctrl → 좌석 선택 / Alt → 확인 버튼🛑 종료: Ctrl+C")
    target_year = 2025 #년도
    target_mon = 6     #월
    target_day = 1     #일
    target_hour = 12   #시간
    target_min = 3     #분
    target_second = 00 #초
    target_ms = 000    #ms

    # 목표 시간에 도달하면 자동으로 엔터키 누릅니다.
    target_kst = datetime(target_year, target_mon, target_day, target_hour, target_min, target_second,target_ms, tzinfo=timezone(timedelta(hours=9)))
    wait_until_kst(target_kst)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()