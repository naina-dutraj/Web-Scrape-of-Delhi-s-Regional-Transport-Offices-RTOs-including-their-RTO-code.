import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://loconav.com/rto-offices/delhi'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.get(url)

css_selector = 'div.state-offices-row'
list_of_rto_office = driver.find_elements(By.CSS_SELECTOR, value=css_selector)

record = []
for office in list_of_rto_office:
    address = office.find_element(By.CSS_SELECTOR, value='p').get_attribute('innerHTML').strip()
    rto_code = office.find_element(By.CSS_SELECTOR, value='p.text-center').get_attribute('innerHTML').strip()
    record.append([address, rto_code])

driver.quit()

url = 'https://www.google.com/maps'

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.get(url)

time.sleep(2)

pprint(record)

new_record = []
for row in record:
    # search_box = driver.find_element(By.CSS_SELECTOR, value="input.searchboxinput[id='searchboxinput'][name='q']")
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys("RTO Office, "+row[0])
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)

    new_url = driver.current_url
    coordinates = new_url.split('@')[1].split(',')[0:2]

    latitude = coordinates[0]
    longitude = coordinates[1]
    new_record.append(row+[latitude, longitude])

    search_box.clear()

driver.quit()

pprint(new_record)
df = pd.DataFrame(new_record, columns=['Office Address', 'RTO Code', 'Latitude', 'Longitude'])
df.to_csv('RTO_Database.csv', index=False, encoding='utf-8')