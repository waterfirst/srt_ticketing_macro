안녕하세요! Python과 Streamlit을 사용하여 **SRT 예매 자동화 웹 애플리케이션**을 만드는 방법에 대한 단계별 가이드를 제공해드리겠습니다. 이 가이드는 웹 애플리케이션의 인터페이스 구축, 사용자 입력 처리, 그리고 자동화 로직(예: Selenium)을 통합하는 방법을 다룹니다. 

**주의사항:** 웹사이트의 자동화 도구 사용은 해당 사이트의 이용 약관을 위반할 수 있으며, 이는 법적인 문제를 초래할 수 있습니다. SRT의 이용 약관을 반드시 확인하고, 합법적인 범위 내에서 도구를 사용하시기 바랍니다. 불법적인 자동화는 법적 책임을 질 수 있습니다.

그럼에도 불구하고, Streamlit과 Selenium을 사용한 웹 애플리케이션 개발 방법을 기술적인 측면에서 설명드리겠습니다.

---

## **목차**

1. [프로젝트 환경 설정](#1-프로젝트-환경-설정)
2. [Streamlit 기본 애플리케이션 만들기](#2-streamlit-기본-애플리케이션-만들기)
3. [Selenium을 사용한 웹 자동화 설정](#3-selenium을-사용한-웹-자동화-설정)
4. [Streamlit과 Selenium 통합하기](#4-streamlit과-selenium-통합하기)
5. [비밀 정보 관리](#5-비밀-정보-관리)
6. [애플리케이션 실행 및 테스트](#6-애플리케이션-실행-및-테스트)
7. [추가 고려 사항 및 디버깅 팁](#7-추가-고려-사항-및-디버깅-팁)
8. [마무리](#8-마무리)

---

## **1. 프로젝트 환경 설정**

### 1.1. Python 설치 확인

먼저, 시스템에 Python이 설치되어 있는지 확인하세요. 터미널(또는 명령 프롬프트)에서 다음 명령어를 실행합니다.

```bash
python --version
```

Python이 설치되어 있지 않다면 [Python 공식 웹사이트](https://www.python.org/downloads/)에서 설치하세요. Python 3.7 이상을 권장합니다.

### 1.2. 가상환경 설정

프로젝트마다 의존성을 관리하기 위해 가상환경을 사용하는 것이 좋습니다.

```bash
# 프로젝트 디렉토리 생성 및 이동
mkdir srt_reservation_app
cd srt_reservation_app

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 1.3. 필수 라이브러리 설치

필요한 라이브러리를 설치합니다.

```bash
pip install streamlit selenium webdriver-manager python-dotenv
```

---

## **2. Streamlit 기본 애플리케이션 만들기**

Streamlit은 간단하게 대화형 웹 애플리케이션을 만들 수 있는 프레임워크입니다. 아래의 간단한 예제를 통해 기본적인 설정을 확인해보겠습니다.

### 2.1. 기본 Streamlit 앱 작성

`app.py` 파일을 생성하고 다음 내용을 입력합니다.

```python
import streamlit as st

def main():
    st.title("SRT 예매 자동화 애플리케이션")
    st.write("여기에 예매 자동화 기능을 추가하세요.")

if __name__ == "__main__":
        main()
```

### 2.2. 애플리케이션 실행

터미널에서 다음 명령어를 실행하여 Streamlit 애플리케이션을 시작합니다.

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며, 간단한 애플리케이션이 표시됩니다.

---

## **3. Selenium을 사용한 웹 자동화 설정**

Selenium은 웹 브라우저를 자동으로 제어할 수 있는 도구입니다. 이를 통해 특정 작업을 자동화할 수 있습니다.

### 3.1. ChromeDriver 다운로드 및 설정

웹 자동화를 위해서는 ChromeDriver가 필요합니다. `webdriver-manager` 라이브러리를 사용하면 ChromeDriver의 설치와 관리를 자동으로 할 수 있습니다.

### 3.2. 기본 Selenium 스크립트 작성

다음은 Selenium을 사용하여 SRT 예매 페이지에 접속하는 기본 스크립트입니다.

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def access_srt_reservation():
    driver = setup_driver()
    try:
        driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do")
        print(driver.title)  # 페이지 제목 출력
    finally:
        driver.quit()

if __name__ == "__main__":
    access_srt_reservation()
```

이 스크립트는 SRT 예매 페이지에 접속하여 페이지 제목을 출력한 후 브라우저를 종료합니다.

### **주의사항:**
- **SRT 이용 약관 준수:** 자동으로 웹사이트에 접속하거나 상호작용하는 것은 SRT의 이용 약관을 위반할 수 있습니다. 사전에 약관을 확인하세요.
- **브라우저 옵션:** `--headless` 옵션을 제거하면 실제 브라우저 창이 열리므로 디버깅 시 유용합니다.

---

## **4. Streamlit과 Selenium 통합하기**

이제 Streamlit 인터페이스를 통해 사용자의 입력을 받고, 이를 기반으로 Selenium을 사용하여 예매 자동화를 구현할 수 있습니다.

### 4.1. 사용자 입력 폼 만들기

`app.py`를 다음과 같이 수정합니다.

```python
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import threading
import queue
from datetime import datetime
from dotenv import load_dotenv
import os

# 메시지 큐 설정
message_queue = queue.Queue()

# .env 파일 로드
load_dotenv()

# 환경 변수에서 ID와 비밀번호 불러오기
SRT_ID = os.getenv('SRT_ID')
SRT_PASSWORD = os.getenv('SRT_PASSWORD')

# 전역 변수 설정
stop_flag = False

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_srt(driver, username, password):
    try:
        driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do")
        wait = WebDriverWait(driver, 10)
        
        # 로그인 버튼 클릭 (셀렉터는 실제 사이트에 맞게 수정 필요)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gnb_menu"]/ul/li[1]/a')))
        login_button.click()
        
        # 아이디 입력
        user_id_input = wait.until(EC.presence_of_element_located((By.ID, 'txtUserId')))
        user_id_input.clear()
        user_id_input.send_keys(username)
        
        # 비밀번호 입력
        password_input = driver.find_element(By.ID, 'txtUserPwd')
        password_input.clear()
        password_input.send_keys(password)
        
        # 로그인 제출
        login_submit = driver.find_element(By.ID, 'btnLogin')
        login_submit.click()
        
        # 로그인 성공 확인 (예: 로그아웃 버튼 존재 확인)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="top"]/div[2]/div/a[1]')))
        message_queue.put(("info", "로그인 성공"))
    except TimeoutException:
        message_queue.put(("error", "로그인 실패: 요소를 찾을 수 없습니다."))
    except Exception as e:
        message_queue.put(("error", f"로그인 중 오류 발생: {e}"))

def make_reservation(driver, departure, arrival, date, time_str):
    global stop_flag
    attempts = 0
    max_attempts = 100
    
    while attempts < max_attempts and not stop_flag:
        attempts += 1
        try:
            message_queue.put(("info", f"예약 시도 {attempts}회: 출발역={departure}, 도착역={arrival}, 날짜={date}, 시간={time_str}"))
            driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
            wait = WebDriverWait(driver, 10)
            
            # 출발역 입력
            departure_input = wait.until(EC.presence_of_element_located((By.ID, 'dptRsStnCdNm')))
            departure_input.clear()
            departure_input.send_keys(departure)
            time.sleep(1)  # 자동 완성 로드 대기
            departure_input.send_keys(Keys.RETURN)  # 첫 번째 자동 완성 선택
            
            # 도착역 입력
            arrival_input = wait.until(EC.presence_of_element_located((By.ID, 'arvRsStnCdNm')))
            arrival_input.clear()
            arrival_input.send_keys(arrival)
            time.sleep(1)  # 자동 완성 로드 대기
            arrival_input.send_keys(Keys.RETURN)  # 첫 번째 자동 완성 선택
            
            # 날짜 설정
            formatted_date = date.strftime("%Y%m%d")
            date_input = driver.find_element(By.ID, 'dptDt')
            date_input.clear()
            date_input.send_keys(formatted_date)
            
            # 시간 설정
            time_element = Select(driver.find_element(By.ID, 'dptTm'))
            time_hour = int(time_str.split(":")[0])
            time_minute = int(time_str.split(":")[1])
            time_formatted = f"{time_hour:02d}{time_minute:02d}00"  # 예: "090000" for 09:00
            time_element.select_by_value(time_formatted)
            
            # 조회하기 버튼 클릭
            search_button = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
            search_button.click()
            
            # 열차 목록 로드 대기
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr')))
            
            # 현재 시각 기준으로 2시간 이내의 출발 시간 계산
            target_datetime = datetime.combine(date, datetime.strptime(time_str, "%H:%M").time())
            target_datetime_plus_2h = target_datetime.replace(hour=(target_datetime.hour + 2) % 24, minute=target_datetime.minute)
            target_time_total = target_datetime_plus_2h.hour * 60 + target_datetime_plus_2h.minute
            
            # 열차 목록 가져오기
            rows = driver.find_elements(By.XPATH, '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr')
            reservation_made = False
            
            for row in rows:
                try:
                    # 출발 시간 가져오기
                    departure_time_text = row.find_element(By.XPATH, './td[3]').text.strip()  # 출발 시간 셀
                    departure_time = datetime.strptime(departure_time_text, "%H:%M")
                    departure_time_total = departure_time.hour * 60 + departure_time.minute
                    
                    # 2시간 이내인지 확인
                    if departure_time_total > target_time_total:
                        continue  # 2시간 후의 열차는 건너뜀
                    
                    # "예약하기" 버튼 찾기
                    reserve_button = row.find_element(By.XPATH, './td[7]/a')
                    if "예약" in reserve_button.text:
                        reserve_button.click()
                        message_queue.put(("info", f"예약 버튼 클릭: 출발 시간 {departure_time_text}"))
                        
                        # 예약 페이지 로드 대기
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="reservation-form"]/fieldset/div[2]/input')))
                        
                        # 예약 완료 확인 (예: 예약 완료 메시지 또는 특정 요소 확인)
                        try:
                            success_element = driver.find_element(By.XPATH, '//*[contains(text(), "예약 완료")]')
                            if success_element:
                                success_message = f"예약 성공!\n출발역: {departure}\n도착역: {arrival}\n출발 시간: {departure_time_text}"
                                message_queue.put(("success", success_message))
                                stop_flag = True
                                return True
                        except NoSuchElementException:
                            message_queue.put(("error", "예약 완료 확인 요소를 찾을 수 없습니다."))
                            return False
                except NoSuchElementException:
                    continue
                except Exception as e:
                    message_queue.put(("error", f"예약 시도 중 오류 발생: {e}"))
                    continue
            
            # 예약 가능한 좌석이 없는 경우
            message_queue.put(("info", f"예약 시도 {attempts}회: 예약 가능한 좌석이 없습니다. 재시도 중..."))
            time.sleep(10)  # 10초 대기 후 재시도
        
        # 최대 시도 횟수에 도달했을 때
        message_queue.put(("error", "예약 시도 100회 실패."))
        return False

def reservation_loop(username, password, departure, arrival, date, time_str):
    driver = setup_driver()
    login_srt(driver, username, password)
    
    success = False
    try:
        success = make_reservation(driver, departure, arrival, date, time_str)
    finally:
        driver.quit()
    
    if success:
        message_queue.put(("success", "예약 성공!"))
    else:
        message_queue.put(("error", "예약 실패. 로그를 확인하세요."))

def main():
    st.title("SRT 예매 자동화 애플리케이션")

    with st.form("reservation_form"):
        username = st.text_input("SRT 사용자명", value=SRT_ID)
        password = st.text_input("비밀번호", type="password", value=SRT_PASSWORD)
        departure = st.text_input("출발역", value="서울")
        arrival = st.text_input("도착역", value="광주")
        date = st.date_input("날짜", value=datetime.now())
        time_str = st.text_input("시간 (HH:MM)", value="09:00")
        submit = st.form_submit_button("예약 시작")
    
    if submit:
        if not username or not password:
            st.error("사용자명과 비밀번호를 입력해주세요.")
        else:
            thread = threading.Thread(target=reservation_loop, args=(
                username, password, departure, arrival, date, time_str))
            thread.start()
    
    # 메시지 큐에서 메시지 읽기
    while not message_queue.empty():
        msg_type, msg_content = message_queue.get_nowait()
        if msg_type == "success":
            st.success(msg_content)
        elif msg_type == "info":
            st.info(msg_content)
        elif msg_type == "error":
            st.error(msg_content)

if __name__ == "__main__":
    main()
```

### 4.2. 코드 설명

1. **라이브러리 임포트:**
   - `streamlit`을 사용하여 웹 인터페이스를 구축합니다.
   - `selenium`과 `webdriver-manager`를 사용하여 브라우저 자동화를 수행합니다.
   - `threading`과 `queue`를 사용하여 백그라운드에서 예약 프로세스를 실행하고, 실시간으로 메시지를 UI에 전달합니다.
   - `dotenv`를 사용하여 `.env` 파일에서 환경 변수를 로드합니다.

2. **메시지 큐 설정:**
   - 스레드 간에 메시지를 전달하기 위해 `queue.Queue`를 사용합니다. 이를 통해 예약 진행 상태를 사용자에게 실시간으로 알릴 수 있습니다.

3. **ChromeDriver 설정:**
   - `webdriver_manager`를 사용하여 ChromeDriver를 자동으로 설치하고 설정합니다.
   - `--headless` 옵션을 사용하여 브라우저 창 없이 자동화 작업을 수행합니다. 디버깅 시 이 옵션을 제거하면 실제 브라우저 창을 볼 수 있습니다.

4. **로그인 함수 (`login_srt`):**
   - SRT 예매 사이트에 로그인하는 함수입니다.
   - 로그인 성공 여부를 메시지 큐에 전달하여 UI에 표시합니다.

5. **예약 함수 (`make_reservation`):**
   - 사용자가 입력한 정보를 바탕으로 예약을 시도합니다.
   - 각 시도마다 메시지를 큐에 전달하여 UI에 진행 상황을 표시합니다.
   - 최대 100회까지 시도하며, 예약이 성공하면 루프를 종료합니다.

6. **예약 루프 (`reservation_loop`):**
   - Selenium 드라이버를 설정하고, 로그인 및 예약 함수를 호출합니다.
   - 예약 성공 여부에 따라 메시지 큐에 결과를 전달합니다.

7. **Streamlit 메인 함수 (`main`):**
   - 사용자로부터 예약 정보를 입력받는 폼을 생성합니다.
   - 예약 시작 버튼을 누르면 백그라운드 스레드에서 예약 루프를 실행합니다.
   - 메시지 큐에 전달된 메시지를 실시간으로 UI에 표시합니다.

---

## **5. 비밀 정보 관리**

### 5.1. `.env` 파일 생성

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음과 같이 SRT 사용자명과 비밀번호를 저장합니다.

```
SRT_ID=your_srt_username
SRT_PASSWORD=your_srt_password
```

**주의:** `.env` 파일은 절대 버전 관리 시스템(Git 등)에 포함시키지 마세요. `.gitignore` 파일에 `.env`를 추가하여 무단 포함을 방지합니다.

### 5.2. `.gitignore` 설정

프로젝트 루트 디렉토리에 `.gitignore` 파일을 생성하고 다음 내용을 추가합니다.

```
.env
```

---

## **6. 애플리케이션 실행 및 테스트**

### 6.1. Streamlit 애플리케이션 실행

터미널에서 다음 명령어를 실행하여 애플리케이션을 시작합니다.

```bash
streamlit run app.py
```

### 6.2. 애플리케이션 사용

1. 브라우저에서 열리는 Streamlit 애플리케이션 페이지에 접속합니다.
2. 사용자명, 비밀번호, 출발역, 도착역, 날짜, 시간을 입력합니다.
3. "예약 시작" 버튼을 클릭하여 예약 프로세스를 시작합니다.
4. 예약 진행 상황과 결과가 실시간으로 UI에 표시됩니다.

**디버깅 Tip:**
- 예약이 제대로 진행되지 않을 경우, `--headless` 옵션을 제거하여 실제 브라우저 창을 확인합니다.
- `reservation.log` 파일을 통해 상세한 로그를 확인할 수 있습니다.

---

## **7. 추가 고려 사항 및 디버깅 팁**

### 7.1. ChromeDriver와 Chrome 브라우저 버전 호환성

- `webdriver_manager`를 사용하면 대부분의 버전 호환 문제를 자동으로 해결할 수 있습니다. 하지만 문제가 발생할 경우 Chrome 브라우저와 ChromeDriver의 버전을 다시 확인하세요.

### 7.2. 헤드리스 모드 디버깅

- `chrome_options.add_argument("--headless")` 옵션을 주석 처리하거나 제거하여 브라우저 창을 실제로 열어보세요. 이를 통해 자동화 스크립트의 동작을 시각적으로 확인할 수 있습니다.

```python
chrome_options.add_argument("--headless")  # 주석 처리 또는 제거
```

### 7.3. 요소 셀렉터 검증

- SRT 웹사이트의 HTML 구조가 변경될 수 있으므로, 각 요소의 ID와 XPath가 현재 사이트와 일치하는지 브라우저의 개발자 도구(F12)를 사용하여 확인하세요.
- 예를 들어, 로그인 버튼의 XPath가 `//*[@id="gnb_menu"]/ul/li[1]/a`인지 확인하고, 필요 시 수정하세요.

### 7.4. 로그 파일 확인

- `reservation.log` 파일을 열어 예약 시도 과정에서 발생한 상세한 로그를 확인하세요. 이를 통해 어떤 단계에서 문제가 발생했는지 파악할 수 있습니다.

### 7.5. Python 및 라이브러리 업데이트

- 최신 버전의 Python, Selenium, `webdriver-manager`, 그리고 Streamlit을 사용하는지 확인하세요. 필요 시 업데이트합니다.

```bash
pip install --upgrade selenium webdriver-manager streamlit python-dotenv
```

### 7.6. 예약 성공 확인 로직 검증

- 실제 SRT 예약 완료 페이지에서 예약 성공을 확인하는 요소(XPath 등)를 정확히 파악하고, 스크립트를 업데이트하세요. 예를 들어, "예약 완료" 메시지가 다른 형식으로 표시될 수 있습니다.

---

## **8. 마무리**

Python과 Streamlit을 사용하여 SRT 예매 자동화 웹 애플리케이션을 구축하는 과정은 사용자 인터페이스 구축, 웹 자동화 로직 통합, 그리고 보안과 윤리적 고려 사항을 포함합니다. 아래는 마무리 단계입니다.

1. **테스트 환경 설정:**
   - 실제 예매를 시도하기 전에 테스트 계정이나 시간이 조정된 열차를 사용하여 충분히 테스트하세요.
   
2. **보안 유지:**
   - 사용자 비밀번호와 같은 민감한 정보는 `.env` 파일에 안전하게 저장하고, 코드에서 직접 노출되지 않도록 합니다.
   
3. **법적 준수:**
   - SRT의 이용 약관을 준수하고, 자동화 스크립트를 사용함으로써 발생할 수 있는 법적 문제를 피하세요.

4. **애플리케이션 배포:**
   - 로컬 환경에서 개발을 완료한 후, Streamlit Sharing, Heroku, AWS 등 클라우드 플랫폼을 사용하여 애플리케이션을 배포할 수 있습니다.

---

**최종 주의사항:** 이번 가이드는 기술적인 측면에서 Python과 Streamlit, Selenium을 사용하는 방법을 설명합니다. SRT 예매 자동화는 해당 서비스의 이용 약관을 위반할 수 있으므로, 반드시 사전에 약관을 확인하고 규정을 준수하면서 개발하시기 바랍니다. 불법적인 자동화 도구 사용은 법적 책임을 질 수 있습니다.

안전하고 책임감 있게 기술을 활용하시기 바랍니다. 추가적인 질문이나 도움이 필요하시다면 언제든지 문의해주세요!

감사합니다.
