import os
from dotenv import load_dotenv
import json
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


load_dotenv()
INPUT_URL = os.getenv('INPUT_URL')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')


chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get(INPUT_URL)


def json_dump():
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'quote')))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dic = {}
    data = soup.find_all('div', 'quote')

    for el in data: 
        
        text = el.find('span', 'text').text[1:-1]
        by = el.find('small', 'author').text
        tags_div = el.find('div', 'tags').text.replace("Tags: ", "").split(" ")

        dic.update({"text": text})
        dic.update({"by": by})
        dic.update({"tags": tags_div})
        
        with open(OUTPUT_FILE, "a") as outfile:
            json.dump(dic, outfile, indent=3)


def main():
    try:
        for i in range(10):
            json_dump()
            driver.find_element(By.PARTIAL_LINK_TEXT, 'Next').click()
    except:
        print("Everything has been scraped, work done!")


if __name__ == '__main__':
    main()
