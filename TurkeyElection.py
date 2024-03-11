from selenium import webdriver
from flask import Flask, render_template, request
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd

app = Flask(__name__)


def fetching():
    driver_path = "https://acikveri.ysk.gov.tr/anasayfa"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd()})
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(driver_path)
    wait = WebDriverWait(driver, 10)

    time.sleep(3)

    element = driver.find_element(
        by=By.XPATH, value='//*[@id="navbarDropdown"]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(3)

    electionType = driver.find_element(
        by=By.CSS_SELECTOR, value='[data-target="#collapse4"]')
    driver.execute_script("arguments[0].click();", electionType)

    time.sleep(3)

    detail = driver.find_element(
        by=By.XPATH, value='//*[@id="collapse4"]/div/div')
    detail.click()

    time.sleep(3)

    electionResult = driver.find_element(
        by=By.XPATH, value='//*[@id="accordionSidebar"]/li[7]/a')
    driver.execute_script("arguments[0].click();", electionResult)

    time.sleep(2)

    generalElection = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.btn.btn-sm.btn-outline-dark.mr-2:nth-child(2)')))

    time.sleep(2)
    try:
        if not os.path.exists("Türkiye.json"):
            driver.execute_script("arguments[0].click();", generalElection)
            time.sleep(3)
            os.rename("IlReferandumSonuc.json", "Türkiye.json")
    except:
        pass

    for i in range(82, 163):
        close_button = driver.find_element(
            by=By.XPATH, value='//*[@id="myModalClose"]/span')

        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(3)
        base = f'text.text-dark:nth-child({i})'

        city = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, base)))
        city_text = city.text

        actions = ActionChains(driver)
        actions.move_to_element(city).click().perform()
        time.sleep(4)

        cityJson = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button.btn-outline-dark:nth-child(2)')))
        time.sleep(3)
        try:
            if not os.path.exists(city_text + ".json"):
                actions.move_to_element(cityJson).click().perform()
                time.sleep(3)
                #driver.execute_script("arguments[0].click();", cityJson)
                time.sleep(4)
                os.rename("IlceReferandumSonuc.json", city_text + ".json")
        except:
            pass
        time.sleep(5)
        driver.back()

        time.sleep(3)

        driver.execute_script("arguments[0].click();", electionResult)

        time.sleep(3)

    driver.quit()


# fetching()

@app.route("/")
def main():
    df = pd.read_json(r"Türkiye.json")

    return render_template("index.html",
                           nameCity=df["İl Adı"].tolist(),
                           noVote=df["Hayır Oranı"].str.replace("%", "").str.replace(
                               ',', '.').astype(float).apply(lambda x: '{:.2f}'.format(x)).tolist(),
                           yesVote=df["Evet Oranı"].str.replace("%", "").str.replace(
                               ',', '.').astype(float).apply(lambda x: '{:.2f}'.format(x)).tolist())


if __name__ == "__main__":
    app.run()
