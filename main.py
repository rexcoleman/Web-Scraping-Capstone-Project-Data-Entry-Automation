from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pdb





#Use beautiful soup to find price, address and link to listings

zillow_url = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56413496923828%2C%22east%22%3A-122.30252303076172%2C%22south%22%3A37.67603960206374%2C%22north%22%3A37.87441023894753%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(zillow_url, headers=headers)
zillow_listings = response.text
soup = BeautifulSoup(zillow_listings, "html.parser")
all_card_elements = soup.select(".property-card-data a")

all_links = []
all_addresses = []
all_prices = []

for link in all_card_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

print(all_links)

for address in all_card_elements:
    address.select(".property-card-data address")
    all_addresses = [address.getText() for address in all_card_elements]
print(all_addresses)

all_price_elements = soup.select(".property-card-data span")

for price in all_price_elements:
    primary_result = price.text
    if "+" in primary_result:
        a = primary_result.split("+")
        all_prices.append(a[0])
    elif "/" in primary_result:
        b = primary_result.split("/")
        all_prices.append(b[0])

print(all_prices)

CHROME_DRIVER_PATH = os.environ.get("/Users/rexcoleman/Development/Drivers/chromedriver_mac64")
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdfxFfILa9v1yYBxhqmoH5o2FnoPOc34-bGd_DhRrm4eTQx3g/viewform?usp=sf_link"
driver = webdriver.Chrome()


for n in range(len(all_links)):
    driver.get(GOOGLE_FORM)
    time.sleep(2)

    address = driver.find_element(By.XPATH,
        "(//input[@class='whsOnd zHQkBf'])[1]")

    price = driver.find_element(By.XPATH,
        "(//input[@class='whsOnd zHQkBf'])[2]")
    link = driver.find_element(By.XPATH,
        "(//input[@class='whsOnd zHQkBf'])[3]")
    submit_button = driver.find_element(By.XPATH, "(//div[@role='button'])[1]")
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()


# pdb.set_trace()












