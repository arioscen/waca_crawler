import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
from datetime import datetime

url = 'https://admin.waca.ec/login'

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_TW.UTF-8')
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)


def login():
    driver.get(url)
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
    except FileNotFoundError:
        pass

    try:
        driver.find_element_by_css_selector("#SysLoginForm_email").send_keys("<email>")
        driver.find_element_by_css_selector("#SysLoginForm_password").send_keys("<passwd>")
        try:
            try:
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'icon-signup'))
                )
            except TimeoutException:
                login()
            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
            return 1
        except UnexpectedAlertPresentException:
            login()
    except NoSuchElementException:
        return 1


def export_order():
    driver.find_element_by_css_selector('.icon-signup').click()
    # 確認連結至訂單管理
    try:
            WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name="date_type"]'))
            )
    except TimeoutException:
            pass
    # 設定搜尋條件
    driver.find_element_by_css_selector('option[value="created_at"]').click()
    thetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    driver.find_element_by_css_selector('#reservationtime').send_keys("2016-08-01 00:00 - {}".format(thetime))
    # 點擊搜尋按鈕
    driver.find_element_by_css_selector(".btn_other.btn-block.btn_order_search.active").click()
    # 避免左側欄位卡住點擊
    # driver.find_element_by_css_selector("#js_fast_filter").click()
    delete_fast_filter = 'document.getElementById("js_fast_filter").remove(); \
                          document.getElementById("js-orders-fast-filter").remove();'
    driver.execute_script(delete_fast_filter)
    driver.find_element_by_css_selector("#js_export_order").click()
    # 確認匯出訂單明細
    try:
            WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn-block.btn-large.btn_okstyle'))
            )
    except TimeoutException:
            pass
    driver.find_element_by_css_selector(".btn.btn-block.btn-large.btn_okstyle").click()


if __name__ == '__main__':
    login()
    export_order()
