# Bulurum.com Web Scraper

This repository contains a Python script that utilizes Selenium WebDriver and BeautifulSoup to scrape business listings from `bulurum.com`, a Turkish local business directory. The script is designed to fetch data for various cities listed in a text file and save the collected information to an Excel file.

## Features

- **Scrape Multiple Cities**: Iteratively scrapes business data from multiple cities specified in a text file.
- **Robust Error Handling**: Includes handling for SSL certificate errors and ensures stability across different web environments.
- **Data Extraction**: Extracts business names, addresses, phone numbers, and additional details.
- **Save to Excel**: Outputs the collected data into a structured Excel file, making it easy for non-technical stakeholders to analyze the data.

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.6 or higher
- Selenium
- BeautifulSoup4
- Pandas

You'll also need ChromeDriver installed and accessible from your system path (or modify the script to point to your ChromeDriver's executable path).

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/emircand/Bulurum-Scraper.git
cd Bulurum-Scraper
```

## Usage
Ensure you have a file named tr_sehirler.txt in the same directory as the script. This file should contain the names of the cities, one per line, from which you want to scrape data.
Run the script using Python:
```bash
python scraper.py
```
Once the script completes, check the businesses_multiple_cities.xlsx file in the same directory for the output.

## How It Works
The script initializes a Selenium WebDriver with Chrome options to ignore SSL certificate errors. It reads the list of cities from tr_sehirler.txt and constructs URLs to visit each city page on bulurum.com. For each city, it paginates through the list of businesses, extracting details using BeautifulSoup and storing them in a list. After completing all pages for a city, it moves to the next city until all cities are processed. The collected data is then saved into an Excel file using Pandas.
