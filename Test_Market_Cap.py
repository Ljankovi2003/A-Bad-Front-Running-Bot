import time
import requests
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Main loop
while True:
    try:
        with open("sve_addrese.txt", "r") as a_file:
            lines = a_file.read().splitlines()

        # Check for new tokens
        if len(lines) > 0:
            token_address = lines[-1]
            print("Checking token:", token_address)

            # Fetch Poocoin link
            pocoin_link = f"https://poocoin.app/tokens/{token_address}"
            driver.get(pocoin_link)

            # Wait for MC element
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                              "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.TokenChart_stats__3732U.d-block.bg-dark-1.shadow.pt-3.text-small > div:nth-child(3) > span.text-success")))
            mc_txt = driver.find_element(By.CSS_SELECTOR,
                                         "#root > div > div.d-none.d-md-flex.flex-column.flex-grow-1 > div.d-flex.flex-column.flex-grow-1.pe-2 > div > div.TokenChart_stats__3732U.d-block.bg-dark-1.shadow.pt-3.text-small > div:nth-child(3) > span.text-success")

            mc = float(mc_txt.text.replace("$", "").replace(",", ""))
            print("Market Cap:", mc)

            if 500 < mc < 10000:
                # Check for honeypot
                URL = f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token={token_address}"
                response = requests.post(url=URL).text
                if response[15:19] == "fals":
                    print("Good token:", token_address)
                    with open('mc_filter.txt', 'a') as myfile:
                        myfile.write(token_address + "\n")
                    with open('Svi.txt', 'a') as b_file:
                        b_file.write(token_address + "\n")
    except Exception as exc:
        print("Error:", exc)

    time.sleep(10)
