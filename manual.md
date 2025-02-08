# SRT 열차 예매 시스템 구축 매뉴얼

## 1. 개발 환경 설정

### 1.1 필수 라이브러리 설치
```bash
pip install streamlit
pip install selenium
pip install webdriver_manager
```

### 1.2 프로젝트 구조
```
srt_reservation/
├── main.py         # 메인 애플리케이션 코드
├── .streamlit/     # Streamlit 설정 디렉토리
│   └── secrets.toml # 비밀 설정 파일
└── requirements.txt # 프로젝트 의존성 파일
```

### 1.3 secrets.toml 설정
```toml
[srt]
username = "your_phone_number"  # SRT 로그인용 휴대폰 번호
password = "your_password"      # SRT 로그인 비밀번호
```

## 2. 기본 구조 구현

### 2.1 필요한 라이브러리 임포트
```python
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime, timedelta
import logging
import threading
import queue
```

### 2.2 기본 설정
```python
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
```

## 3. 핵심 기능 구현

### 3.1 웹드라이버 설정
```python
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver
```

### 3.2 로그인 기능
로그인 함수는 SRT 웹사이트에 자동으로 로그인하는 기능을 구현합니다:
```python
def login_srt(driver, username, password):
    try:
        driver.get('https://etk.srail.kr/cmc/01/selectLoginForm.do')
        time.sleep(2)
        
        # 휴대폰 번호 로그인
        driver.find_element(By.ID, 'srchDvCd3').click()
        time.sleep(1)
        
        driver.find_element(By.ID, 'srchDvNm03').send_keys(username)
        driver.find_element(By.ID, 'hmpgPwdCphd03').send_keys(password)
        
        login_btn = driver.find_element(
            By.XPATH, 
            '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[4]/div/div[2]/input'
        )
        login_btn.click()
        time.sleep(2)
        
        return True
    except Exception as e:
        logging.error(f"로그인 실패: {str(e)}")
        return False
```

### 3.3 예약 기능
열차 예약을 시도하는 핵심 함수입니다:
```python
def make_reservation(driver, departure, arrival, date, time_str):
    try:
        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        time.sleep(2)
        
        # 출발역, 도착역 설정
        driver.find_element(By.ID, 'dptRsStnCdNm').clear()
        driver.find_element(By.ID, 'dptRsStnCdNm').send_keys(departure)
        time.sleep(1)
        
        driver.find_element(By.ID, 'arvRsStnCdNm').clear()
        driver.find_element(By.ID, 'arvRsStnCdNm').send_keys(arrival)
        time.sleep(1)
        
        # 날짜 설정
        formatted_date = date.strftime("%Y%m%d")
        driver.execute_script(
            f"document.getElementById('dptDt').value = '{formatted_date}'"
        )
        
        # 시간 설정
        time_hour = time_str.split(":")[0]
        time_element = driver.find_element(By.ID, 'dptTm')
        select = Select(time_element)
        select.select_by_value(time_hour + "0000")
        time.sleep(1)
        
        # 조회하기 버튼 클릭
        search_button = driver.find_element(
            By.XPATH, 
            '//*[@id="search_top_tag"]/input'
        )
        search_button.click()
        time.sleep(2)
        
        # 예약 가능한 열차 찾기 및 예약
        rows = driver.find_elements(
            By.XPATH, 
            '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr'
        )
        
        for i, row in enumerate(rows, 1):
            try:
                reservation_button = driver.find_element(
                    By.XPATH, 
                    f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a'
                )
                
                if "예약" in reservation_button.text.strip():
                    reservation_button.click()
                    return True
                    
            except NoSuchElementException:
                continue
                
        return False
        
    except Exception as e:
        logging.error(f"예약 시도 중 오류 발생: {str(e)}")
        return False
```

## 4. Streamlit UI 구현

### 4.1 메인 UI 구성
```python
def main():
    st.set_page_config(page_title="SRT 예약 시스템", layout="wide")
    
    st.title("🚄 SRT 자동 예약 시스템")
    
    if 'reservation_active' not in st.session_state:
        st.session_state.reservation_active = False
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("예약 정보")
        departure = st.selectbox("출발역", 
            ["동탄", "평택지제", "천안아산", "오송", "대전", 
             "김천(구미)", "동대구", "신경주", "울산", "부산"],
            index=0)
        arrival = st.selectbox("도착역",
            ["수서", "동탄", "평택지제", "천안아산", "오송", "대전", 
             "김천(구미)", "동대구", "신경주", "울산", "부산"],
            index=10)
        
        # 날짜 선택
        min_date = datetime.now().date()
        date = st.date_input("날짜", value=min_date, min_value=min_date)
        
        # 시간 선택 (30분 단위)
        hours = list(range(0, 24))
        minutes = [0, 30]
        time_options = [f"{h:02d}:{m:02d}" for h in hours for m in minutes]
        selected_time = st.selectbox("시간", time_options, 
                                   index=time_options.index(datetime.now().strftime("%H:00")))
```

### 4.2 예약 상태 표시 UI
```python
    with col2:
        st.subheader("예약 상태")
        
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
                
                reservation_thread = threading.Thread(
                    target=reservation_process,
                    args=(departure, arrival, date, selected_time)
                )
                reservation_thread.start()
```

## 5. 실행 및 테스트

### 5.1 애플리케이션 실행
```bash
streamlit run main.py
```

### 5.2 주의사항
1. Chrome 브라우저가 설치되어 있어야 합니다.
2. secrets.toml 파일에 로그인 정보가 올바르게 설정되어 있어야 합니다.
3. 네트워크 상태가 안정적이어야 합니다.
4. 자동 예약 시스템은 실제 SRT 웹사이트의 변경에 따라 수정이 필요할 수 있습니다.

### 5.3 문제 해결
- 셀레니움 오류 발생 시 Chrome 브라우저와 ChromeDriver 버전이 일치하는지 확인
- 로그인 실패 시 secrets.toml 파일의 계정 정보 확인
- 예약 버튼 클릭 실패 시 XPath 정확성 확인

## 6. 유지보수 및 개선사항

### 6.1 코드 유지보수
- SRT 웹사이트 구조 변경 시 XPath 및 선택자 업데이트 필요
- 예외 처리 로직 보완
- 로깅 기능 강화

### 6.2 개선 가능한 기능
- 다중 열차 동시 예약
- 예약 성공 시 알림 기능 (이메일, SMS 등)
- 예약 이력 관리
- 자동 로그인 세션 유지
- 예약 가능 좌석 필터링 기능
