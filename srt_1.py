import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime, timedelta
import logging
import threading
import queue

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# 전역 변수
stop_flag = False
reservation_thread = None
message_queue = queue.Queue()
attempt_count = 0
MAX_ATTEMPTS = 100  # 최대 시도 횟수

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_srt(driver, username, password):
    try:
        driver.get('https://etk.srail.kr/cmc/01/selectLoginForm.do')
        time.sleep(2)
        
        # 휴대폰 번호 로그인
        driver.find_element(By.ID, 'srchDvCd3').click()
        time.sleep(1)
        
        driver.find_element(By.ID, 'srchDvNm03').send_keys(username)
        driver.find_element(By.ID, 'hmpgPwdCphd03').send_keys(password)
        
        login_btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[4]/div/div[2]/input')
        login_btn.click()
        time.sleep(2)
        
        message_queue.put(("info", "로그인 성공"))
        return True
    except Exception as e:
        message_queue.put(("error", f"로그인 실패: {str(e)}"))
        return False


def make_reservation(driver, departure, arrival, date, time_str):
    try:
        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        time.sleep(2)
        
        # 출발역 설정
        departure_input = driver.find_element(By.ID, 'dptRsStnCdNm')
        departure_input.clear()
        departure_input.send_keys(departure)
        
        # 도착역 설정
        arrival_input = driver.find_element(By.ID, 'arvRsStnCdNm')
        arrival_input.clear()
        arrival_input.send_keys(arrival)
        
        # 시간 선택
        time_select = driver.find_element(By.ID, 'dptTm')
        for option in time_select.find_elements(By.TAG_NAME, 'option'):
            if time_str in option.text:
                option.click()
                break
        
        # 조회하기 버튼 클릭
        search_button = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
        search_button.click()
        time.sleep(2)
        
        # 예약 가능한 열차 찾기 및 예약 시도
        try:
            # 첫 번째 열차의 예약 버튼 XPATH
            reservation_button = driver.find_element(
                By.XPATH, 
                '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[1]/td[6]/a'
            )
            
            button_text = reservation_button.text
            
            if button_text == "예약하기":
                # 예약 버튼 클릭
                reservation_button.click()
                time.sleep(1)
                
                # 열차 정보 가져오기
                tr_element = reservation_button.find_element(By.XPATH, "./ancestor::tr")
                departure_time = tr_element.find_element(By.XPATH, ".//td[@class='time']").text
                
                success_message = f"예약 성공!\n출발역: {departure}\n도착역: {arrival}\n출발 시간: {departure_time}"
                message_queue.put(("success", success_message))
                global stop_flag
                stop_flag = True  # 예약 성공 시 중지
                return True
            else:
                message_queue.put(("info", f"현재 예약 가능한 좌석이 없습니다. (상태: {button_text})"))
                return False
            
        except Exception as e:
            message_queue.put(("error", f"예약하기 버튼 클릭 중 오류 발생: {str(e)}"))
            return False
            
    except Exception as e:
        message_queue.put(("error", f"예약 시도 중 오류 발생: {str(e)}"))
        return False

def reservation_process(departure, arrival, date, time_str):
    global stop_flag, attempt_count
    driver = setup_driver()
    try:
        username = st.secrets["srt"]["username"]
        password = st.secrets["srt"]["password"]
        
        if login_srt(driver, username, password):
            attempt_count = 0
            
            while not stop_flag and attempt_count < MAX_ATTEMPTS:
                attempt_count += 1
                message_queue.put(("info", f"예약 시도 #{attempt_count}"))
                
                if make_reservation(driver, departure, arrival, date, time_str):
                    break
                    
                time.sleep(2)
                driver.refresh()
    except Exception as e:
        message_queue.put(("error", f"예약 프로세스 중 오류 발생: {str(e)}"))
    finally:
        driver.quit()

def main():
    st.set_page_config(page_title="SRT 예약 시스템", layout="wide")
    
    st.title("🚄 SRT 자동 예약 시스템")
    
    if 'reservation_active' not in st.session_state:
        st.session_state.reservation_active = False
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("예약 정보")
        departure = st.selectbox("출발역", 
            ["동탄", "평택지제", "천안아산", "오송", "대전", "김천(구미)", "동대구", "신경주", "울산", "부산"],
            index=0)  # 동탄을 기본값으로 설정
        arrival = st.selectbox("도착역",
            ["수서", "동탄", "평택지제", "천안아산", "오송", "대전", "김천(구미)", "동대구", "신경주", "울산", "부산"],
            index=10)  # 부산을 기본값으로 설정
        
        date = st.date_input("날짜", min_value=datetime.now().date())
        time_str = st.time_input("시간", datetime.now().time()).strftime("%H:00")
        
    with col2:
        st.subheader("예약 상태")
        
        # 시도 횟수 표시 영역
        attempt_container = st.container()
        st.write("예약 시도 현황")
        progress_bar = st.progress(0)
        attempt_text = st.empty()
        
        if not st.session_state.reservation_active:
            if st.button("예약 시작", type="primary"):
                st.session_state.reservation_active = True
                global stop_flag, reservation_thread, attempt_count
                stop_flag = False
                attempt_count = 0
                formatted_date = date.strftime("%Y%m%d")
                
                reservation_thread = threading.Thread(
                    target=reservation_process,
                    args=(departure, arrival, formatted_date, time_str)
                )
                reservation_thread.start()
        
        # 중지 버튼은 항상 표시
        if st.button("예약 중지", type="secondary", key="stop_button"):
            stop_flag = True
            st.session_state.reservation_active = False
            st.warning("예약이 중지되었습니다.")
        
        # 상태 메시지 표시 영역
        status_container = st.container()
        
        # 실시간 업데이트
        if st.session_state.reservation_active:
            while True:
                # 진행률 업데이트
                progress = min(attempt_count / MAX_ATTEMPTS, 1.0)
                progress_bar.progress(progress)
                attempt_text.write(f"현재 {attempt_count}번째 시도 중... (최대 {MAX_ATTEMPTS}회)")
                
                # 메시지 큐 처리
                try:
                    msg_type, message = message_queue.get_nowait()
                    with status_container:
                        if msg_type == "error":
                            st.error(message)
                        elif msg_type == "success":
                            st.success(message)
                            st.session_state.reservation_active = False
                            break
                        else:
                            st.info(message)
                except queue.Empty:
                    pass
                
                if stop_flag or not st.session_state.reservation_active:
                    break
                
                time.sleep(0.1)

if __name__ == "__main__":
    main()