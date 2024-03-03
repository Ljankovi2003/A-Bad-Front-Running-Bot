import datetime
import time
import requests
import bs4
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

myfile = open('increasinghold_filter.txt', 'w', buffering=1)
lista = []

options = webdriver.EdgeOptions()
options.add_argument("headless")
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

while True:
    try:
        with open("mc_filter.txt", "r") as a_file:
            lines = a_file.read().splitlines()

        if lines:
            time.sleep(5)
            for token_address in lines:
                link = "https://bscscan.com/token/" + token_address
                driver.get(link)
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#ContentPlaceHolder1_tr_tokenHolders > div > div.col-md-8 > div > div")))
                html = driver.page_source
                soup = bs4.BeautifulSoup(html, "lxml")
                element = soup.findAll('div', {'class': "mr-3"})[0].text
                holders_txt = element.split(" ")[0]
                holders = int(holders_txt.replace(",", ""))
                print(holders)

                if holders > 40 and token_address not in lista:
                    lista.append(token_address)
                    myfile.write(token_address + "\n")
                    time_now = datetime.datetime.now()
                    myfile.write(str(time_now) + "\n")

                    pocoin_link = "https://poocoin.app/tokens/" + token_address
                    driver.get(pocoin_link)
                    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.d-flex.flex-column.flex-grow-1.ps-2.pt-2.lh-1 > div.d-flex.align-items-start.flex-wrap > div.mt-1.ps-2.d-flex.align-items-center.flex-grow-1 > div > div.d-flex.flex-wrap > div > span")))
                    price_txt = driver.find_element(By.CSS_SELECTOR, "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.d-flex.flex-column.flex-grow-1.ps-2.pt-2.lh-1 > div.d-flex.align-items-start.flex-wrap > div.mt-1.ps-2.d-flex.align-items-center.flex-grow-1 > div > div.d-flex.flex-wrap > div > span")
                    element_txt = price_txt.text
                    element3 = element_txt.replace("$", "")
                    myfile.write(element3 + "\n")

                    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.TokenChart_stats__3732U.d-block.bg-dark-1.shadow.pt-3.text-small > div:nth-child(3) > div > div:nth-child(1) > a:nth-child(5)")))
                    link = driver.find_element(By.CSS_SELECTOR, "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.TokenChart_stats__3732U.d-block.bg-dark-1.shadow.pt-3.text-small > div:nth-child(3) > div > div:nth-child(1) > a:nth-child(5)").get_attribute("href")

                    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.TokenChart_stats__3732U.d-block.bg-dark-1.shadow.pt-3.text-small > div:nth-child(3) > span.text-success")))
                    mc_txt = driver.find_element(By.CSS_SELECTOR, "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.TokenChart_stats__3732U.d-block.bg-dark-1.shadow.pt-3.text-small > div:nth-child(3) > span.text-success")
                    mc1 = mc_txt.text

                    myfile.write(mc1 + "\n")
    except Exception as exc:
        print("Error:", exc)
        driver.close()
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
