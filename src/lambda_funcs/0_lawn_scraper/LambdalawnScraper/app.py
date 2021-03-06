import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def lambda_handler(event, context):
    options = Options()
    options.binary_location = "/opt/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome("/opt/chromedriver", chrome_options=options)

    driver.get("https://www.bryantpark.org/")
    print(f"Headless Chrome Initialized, Page title: {driver.title}")

    try:
        status_text = (
            WebDriverWait(driver, 3)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[4]/div[1]/section/section/div[1]/div/div[2]/div[2]/section/div/h4",
                    )
                )
            )
            .text
        )

        temp_F = (
            WebDriverWait(driver, 3)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[4]/div[1]/section/section/div[1]/div/div[2]/div[1]/section/div/div/div[2]/section/p",
                    )
                )
            )
            .text
        )

    finally:
        driver.close()
        driver.quit()

    temp_F_clean = temp_F.split("\u00b0")[0]

    status_and_temp = {"raw_lawn_status": status_text, "temp_F": temp_F_clean}

    return {
        "statusCode": 200,
        "body": status_and_temp,
    }
