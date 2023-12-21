# Import Libaries and Dependencies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import os
import time

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Initialize Chrome options
options = Options()

# Set Chrome options
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.72 Safari/537.36')
options.add_argument("--disable-images")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Base URL
base_url = 'https://www.wineenthusiast.com/?s=&search_type=ratings&page={}&drink_type=wine'
base_url_year_style = 'https://www.wineenthusiast.com/?s=&search_type=ratings&page={}&drink_type=wine&wine_style={}&pub_date=%253A{}'
base_url_year = 'https://www.wineenthusiast.com/?s=&search_type=ratings&page={}&drink_type=wine&pub_date=%253A{}'
base_url_style = 'https://www.wineenthusiast.com/?s=&search_type=ratings&page={}&drink_type=wine&wine_style={}'

# Wine styles to iterate over
wine_styles = ['Red', 'White', 'Sparkling', 'Rose', 'Dessert', 'Port%252FSherry', 'Fortified']

# List to hold wine names and URLs
data = []

# Set Page Counter
page_counter = 0

# Iterate through up to 48 pages without year and wine style
for page in range(1, 49):
    try:
        driver.get(base_url.format(page))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
        time.sleep(2)
        page_counter += 1
        if page_counter > 25:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            driver.quit()
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(base_url.format(page))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
            time.sleep(2)
            page_counter = 0
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ratings-block__info")))

        # Find all wine blocks
        wine_blocks = driver.find_elements(By.CLASS_NAME, 'ratings-block__info')

        for block in wine_blocks:
            try:
                if block.find_elements(By.XPATH, './/h3[@class="info__title"]/a'):
                    wine_link_element = block.find_element(By.XPATH, './/h3[@class="info__title"]/a')
                    wine_name = wine_link_element.text.strip()
                    wine_url = wine_link_element.get_attribute('href')
                    # Add to list
                    data.append({'Wine Name': wine_name, 'URL': wine_url})
            except Exception as e:
                print(f"Error processing a wine block: {e}")
    except TimeoutException:
        print(f"Timed out waiting for page {page} to load")
        print("Browser became unresponsive. Restarting WebDriver.")
        driver.quit()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(base_url.format(page))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
        time.sleep(2)
        continue # Skip to the next iterations

            
# Loop through pages, years, and wine styles
for year in range(2004, 2024, 3):
    for wine_style in wine_styles:
        for page in range(1, 49):
            try:
                driver.get(base_url_year_style.format(page, wine_style, year))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                time.sleep(2)
                page_counter += 1
                if page_counter > 25:
                    driver.delete_all_cookies()
                    driver.execute_script("window.localStorage.clear();")
                    driver.execute_script("window.sessionStorage.clear();")
                    driver.quit()
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.get(base_url_year_style.format(page, wine_style, year))
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                    time.sleep(2)
                    page_counter = 0
                WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ratings-block__info")))

                # Find all wine blocks
                wine_blocks = driver.find_elements(By.CLASS_NAME, 'ratings-block__info')

                for block in wine_blocks:
                    try:
                        if block.find_elements(By.XPATH, './/h3[@class="info__title"]/a'):
                            wine_link_element = block.find_element(By.XPATH, './/h3[@class="info__title"]/a')
                            wine_name = wine_link_element.text.strip()
                            wine_url = wine_link_element.get_attribute('href')
                            # Add to list
                            data.append({'Wine Name': wine_name, 'URL': wine_url})
                    except Exception as e:
                        print(f"Error processing a wine block: {e}")
            except TimeoutException:
                print(f"Timed out waiting for page {page}, year {year}, style {wine_style} to load")
                print("Browser became unresponsive. Restarting WebDriver.")
                driver.quit()
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(base_url_year_style.format(page, wine_style, year))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                time.sleep(2)
                continue

# Loop through pages and years
for year in range(2004, 2023, 2):
        for page in range(1, 49):
            try:
                driver.get(base_url_year.format(page, year))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                time.sleep(2)
                page_counter += 1
                if page_counter > 25:
                    driver.delete_all_cookies()
                    driver.execute_script("window.localStorage.clear();")
                    driver.execute_script("window.sessionStorage.clear();")
                    driver.quit()
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.get(base_url_year.format(page, year))
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                    time.sleep(2)
                    page_counter = 0
                WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ratings-block__info")))

                    
                # Find all wine blocks
                wine_blocks = driver.find_elements(By.CLASS_NAME, 'ratings-block__info')

                for block in wine_blocks:
                    try:
                        if block.find_elements(By.XPATH, './/h3[@class="info__title"]/a'):
                            wine_link_element = block.find_element(By.XPATH, './/h3[@class="info__title"]/a')
                            wine_name = wine_link_element.text.strip()
                            wine_url = wine_link_element.get_attribute('href')
                            # Add to list
                            data.append({'Wine Name': wine_name, 'URL': wine_url})
                    except Exception as e:
                        print(f"Error processing a wine block: {e}")
            except TimeoutException:
                print(f"Timed out waiting for page {page}, year {year} to load")
                print("Browser became unresponsive. Restarting WebDriver.")
                driver.quit()
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(base_url_year.format(page, year))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                time.sleep(2)
                continue


# Loop through pages and wine styles
for wine_style in wine_styles:
    for page in range(1, 49):
        try:
            driver.get(base_url_style.format(page, wine_style))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
            time.sleep(2)
            page_counter += 1
            if page_counter > 25:
                driver.delete_all_cookies()
                driver.execute_script("window.localStorage.clear();")
                driver.execute_script("window.sessionStorage.clear();")
                driver.quit()
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(base_url_style.format(page, wine_style))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
                time.sleep(2)
                page_counter = 0
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ratings-block__info")))

            # Find all wine blocks
            wine_blocks = driver.find_elements(By.CLASS_NAME, 'ratings-block__info')

            for block in wine_blocks:
                try:
                    if block.find_elements(By.XPATH, './/h3[@class="info__title"]/a'):
                        wine_link_element = block.find_element(By.XPATH, './/h3[@class="info__title"]/a')
                        wine_name = wine_link_element.text.strip()
                        wine_url = wine_link_element.get_attribute('href')
                        # Add to list
                        data.append({'Wine Name': wine_name, 'URL': wine_url})
                except Exception as e:
                    print(f"Error processing a wine block: {e}")
        except TimeoutException:
            print(f"Timed out waiting page {page}, style {wine_style} to load")
            print("Browser became unresponsive. Restarting WebDriver.")
            driver.quit()
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(base_url_style.format(page, wine_style))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
            time.sleep(2)
            continue

# Convert the list to DataFrame
df = pd.DataFrame(data)

# Remove duplicates and reset index
df = df.drop_duplicates(subset='Wine Name', keep='first')
df = df.reset_index(drop=True)

# Optionally, save to CSV file
df.to_csv(os.path.join(current_directory, 'output', 'wine_links.csv'), index=False)

driver.quit()