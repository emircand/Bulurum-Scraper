from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
chrome_options.add_argument('--ignore-ssl-errors')  # Also ignore SSL errors

# Initialize WebDriver with options
driver = webdriver.Chrome(executable_path=r'C:\Program Files\chromedriver-win64\chromedriver.exe', options=chrome_options)


with open('tr_sehirler.txt', 'r', encoding='utf-8') as file:
    cities = [line.strip().lower() for line in file if line.strip()]

all_business_list = []

for city_name in cities:
    print(f"Processing city: {city_name}")
    page_number = 0
    city_business_list = []

    while True:
        if page_number >= 1:
            print(f"Scraping page {page_number} of {city_name}...")
            url = f'https://www.bulurum.com/search/gözlükçüler/{city_name}/?page={page_number}'
        else:
            url = f'https://www.bulurum.com/search/gözlükçüler/{city_name}/'
        print(url)
        driver.get(url)
        time.sleep(5)  # Increase wait time for JavaScript to load

        # Additional delay to ensure all dynamic content is loaded
        time.sleep(3)

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        business_list = []

        for item in soup.find_all("div", class_="FreeListingItemBox"):
            full_name = item.find("h2", class_="CompanyName").get_text(strip=True)
            address = item.find("div", class_="FreeListingAddress").get_text(strip=True)
            phone = item.find("div", itemprop="telephone").get_text(strip=True) if item.find("div", itemprop="telephone") else None

            match = re.search(r'\((.*?)\)', full_name)
            owner = match.group(1) if match else None
            name = re.sub(r'\s*\([^)]*\)', '', full_name).strip() if match else full_name

            address_parts = address.split(", ")
            district = address_parts[-2].split(" ")[-1 if len(address_parts) >= 2 else None]
            province = address_parts[-1] if len(address_parts) >= 2 else None

            business_list.append({
                "Optik": name,
                "Optisyen": owner,
                "Adres": address,
                "İlçe": district,
                "İl": province,
                "Telefon": phone
            })

        if not business_list:
            print(f"No more businesses found in {city_name}.")
            break

        city_business_list.extend(business_list)
        page_number += 1
        print(f"Page {page_number - 1} of {city_name} scraped.")

    all_business_list.extend(city_business_list)

driver.quit()  # Close the browser

df = pd.DataFrame(all_business_list)
df.to_excel("businesses_multiple_cities.xlsx", index=False)
print("Excel file has been created with the business details from all cities.")