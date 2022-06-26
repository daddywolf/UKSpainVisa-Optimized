import ssl
import time

import pyttsx3
import undetected_chromedriver

from utils.config import TIMEOUT, CENTER_MAN, MODE_NORMAL, No1
from utils.log import logger
from visa import Visa


def init_driver():
    profile = {
        "profile.default_content_setting_values.notifications": 1  # block notifications
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    chrome_options = undetected_chromedriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")

    driver = undetected_chromedriver.Chrome(options=chrome_options)
    driver.implicitly_wait(1)
    driver.delete_all_cookies()
    return driver


def monitor(email, password, url, centers, mode):

    driver = init_driver()
    visa = Visa(driver)
    try:
        visa.go_to_appointment_page(url)
        time.sleep(5)
        visa.login(email, password)
        visa.go_to_book_appointment(url, email)
        visa.select_centre(centers[0], centers[1], centers[2], email)
        while True:
            dates = visa.check_available_dates(mode, centers[3], email)
            if dates:
                logger.info(f"USER {email} DAY AVAILABLE: {dates}")
                pyttsx3.speak(f"day available {email} {dates}")
                time.sleep(10)
                # 10s 后继续进入下一个循环
            else:
                logger.info(f"{email}: NO DAY AVAILABLE...")
                time.sleep(TIMEOUT)
                driver.refresh()

    except Exception as e:
        logger.error(f'Monitor runtime error from {email} {e}')
        driver.quit()
        monitor(email, password, url, centers, mode)


if __name__ == "__main__":
    pyttsx3.speak("Notification Test OK")
    monitor(*No1[0])
    # 执行部分
    # pool = threadpool.ThreadPool(len(USERS))
    # gl_tasks = threadpool.makeRequests(monitor, USERS)
    # for task in gl_tasks:
    #     pool.putRequest(task)
    # pool.wait()
