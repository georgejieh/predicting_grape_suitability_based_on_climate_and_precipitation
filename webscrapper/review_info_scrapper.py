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
df = pd.read_csv(os.path.join(current_directory, 'output', 'wine_links.csv'))

# Initialize Chrome options
options = Options()

# Set Chrome options
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.72 Safari/537.36')
options.add_argument("--disable-images")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# DataFrame to hold scraped data
scraped_data = pd.DataFrame(columns=['Wine Name', 'Region 1', 'Region 2', 'Region 3', 'Country', 'Score', 'Price', 'Winery', 'Variety', 'Wine Type'])

# Function to safely get text from elements
def safe_get_text(driver, by, selector):
    try:
        element = driver.find_element(by, selector)
        return element.text.strip()
    except NoSuchElementException:
        return None

# Function to safely get text from elements using XPATH
def safe_get_text_by_xpath(driver, xpath):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return [element.text.strip() for element in elements]
    except NoSuchElementException:
        return []

page_counter = 0

# Iterate through URLs in the DataFrame
for idx, row in df.iterrows():
    url = row['URL']
    driver.get(url)
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
            driver.get(url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
            time.sleep(2)
            page_counter = 0
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'review-title')))
    except TimeoutException:
        print(f"Timeout or invalid page at URL: {url}")
        driver.quit()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        continue  # Skip to the next URL

    wine_name = safe_get_text(driver, By.CLASS_NAME, 'review-title')
    
    # If wine_name is not found, skip to the next URL
    if not wine_name:
        continue    
    
    # Using relative XPATH to get region elements
    region_xpath = '//*[@id="single-page"]/header/div/div/div/div/div[2]/span[2]/a'
    region_elements = safe_get_text_by_xpath(driver, region_xpath)
    region_value = safe_get_text(driver, By.CSS_SELECTOR, 'div.region .value a')

    # Process regions
    country = region_elements[-1] if region_elements else None
    region_1 = region_value if region_value in region_elements else None
    region_2 = region_elements[-2] if len(region_elements) > 1 and region_elements[-2] != region_value else None
    region_3 = region_elements[-3] if len(region_elements) > 2 and region_elements[-3] != region_value else None

    # Extract score and price
    score = re.sub(r'RATING\n', '', safe_get_text(driver, By.CLASS_NAME, 'score'))
    price = re.sub(r'PRICE\n', '', safe_get_text(driver, By.CLASS_NAME, 'price'))

    winery = safe_get_text(driver, By.CSS_SELECTOR, 'div.winery .value a')
    variety = safe_get_text(driver, By.CSS_SELECTOR, 'div.variety .value a')
    wine_type = safe_get_text(driver, By.CSS_SELECTOR, 'div.wine-type .value a')

    # Create a new DataFrame row
    new_row = {'Wine Name': wine_name, 'Region 1': region_1, 'Region 2': region_2, 'Region 3': region_3, 'Country': country, 'Score': score, 'Price': price, 'Winery': winery, 'Variety': variety, 'Wine Type': wine_type}
    new_row_df = pd.DataFrame([new_row])

    # Concatenate new row to scraped_data DataFrame
    scraped_data = pd.concat([scraped_data, new_row_df], ignore_index=True)
    
    # Save to CVS just in case script crashes out
    scraped_data.to_csv(os.path.join(current_directory, 'output', 'wine_info.csv'), index=False)

# Close the WebDriver
driver.quit()

# Save to CSV file
scraped_data.to_csv(os.path.join(current_directory, 'output', 'wine_info.csv'), index=False)