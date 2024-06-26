from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Initialize WebDriver
driver = webdriver.Chrome(executable_path=r'C:\Program Files\chromedriver-win64\chromedriver.exe')

# Define a translation table for Turkish characters to English
turkish_to_english = str.maketrans('ğüşıöçĞÜŞİÖÇ', 'gusiocGUSIOC')

with open('tr_sehirler.txt', 'r', encoding='utf-8') as file:
    cities = [line.split('\t')[2].strip().lower().translate(turkish_to_english) for line in file.readlines()]

all_business_list = []

for city_name in cities:
    print(f"Processing city: {city_name}")
    page_number = 1
    city_business_list = []

    while True:
        url = f'https://www.bulurum.com/search/gözlükçüler/{city_name}/?page={page_number}'
        driver.get(url)
        time.sleep(2)  # Wait for JavaScript to load

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
            district = address_parts[-2].split(" ")[-1] if len(address_parts) >= 2 else None
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