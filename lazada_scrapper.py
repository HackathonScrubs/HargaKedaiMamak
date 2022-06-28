import requests
import csv
from email import charset
import time
import random
import re
import threading
import logging
import time
# from hmni import hmni
from xml.dom.minidom import TypeInfo
import rapidfuzz
from thefuzz import fuzz, process
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from colorama import Fore, Back, Style

def init_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)

def get_lazada_link(file):
    lazada_links = []
    with open(file) as links_csv:
        csv_reader = csv.reader(links_csv)
        for row in csv_reader:
            lazada_links.append(row[0])
    return lazada_links

def save_lazada_data(data):
    filename = "exported_products_" + datetime.now().strftime("%d_%H_%M_%S") + ".csv"
    with open(filename,  mode = 'w', newline = '', encoding = "utf-8") as exported_csv:
        csv_writer = csv.writer(exported_csv, delimiter = ',', quotechar = '"')
        for product in data:
            row = [product["link"], product["product_name"], product["product_price"]]
            csv_writer.writerow(row)

def get_product_name(driver, class_name):
    return driver.find_element(By.XPATH, "//h1[@class = '" + class_name + "']").text

def get_product_price(driver, class_name):
    return driver.find_element(By.XPATH, "//span[@class = '" + class_name + "']").text

def scrape_lazada(driver, links, start, end):
    data = []
    driver.set_page_load_timeout(3);
    print(Fore.BLUE + "STARTED SELENIUM SCRAPPING" + Fore.RESET)
    for i in range(start, end):
        product = {}
        try:
            driver.get(links[i])
            #time.sleep(10)
        except:
            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE).perform()
        product["link"] = links[i]
        product_name = get_product_name(driver, "pdp-mod-product-badge-title")
        #print(product_name)
        product["product_name"] = product_name
        product_price = get_product_price(driver, "pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl")
        product["product_price"] = product_price
        data.append(product)
        print(Fore.GREEN + "Completed scrapping URL (" , i+1 , "/" , end-start , ")" + links[i])
    print(Fore.GREEN + "FINISHED SELENIUM SCRAPPING")
    driver.quit()
    return data

def scrape_lazada_beautifulsoup(links, start, end):
    data = []
    print(Fore.BLUE + "STARTED BEAUTIFULSOUP SCRAPPING")
    for i in range(start, end):
        page = requests.get(links[i])
        soup = BeautifulSoup(page.content, "html.parser")
        product = {}
        product["link"] = links[i]
        find_title = soup.find("h1", class_="pdp-mod-product-badge-title")
        if (find_title):
            product["product_name"] = find_title.text
        else:
            product["product_name"] = None
        find_price = soup.find("span", class_="pdp-price pdp-price_type_normal pdp-price_color_orange pdp-primece_size_xl")
        if (find_price):
            product["product_price"] = find_price.text
        else:
            product["product_price"] = None
        data.append(product)
        print(Fore.GREEN + "Completed scrapping URL (" , i+1 , "/" , end-start , ")" + links[i])
    print(Fore.GREEN + "FINISHED BEAUTIFULSOUP SCRAPPING")
    return data

def get_exported_data():
    exported_data = []
    with open("exported_products_27_18_13_32.csv", encoding = "utf-8") as data_csv:
        csv_reader = csv.reader(data_csv)
        for row in csv_reader:
            exported_data.append(row)
    return exported_data

def get_products_csv():
    products_csv_data = []
    with open("products.csv") as products_csv:
        csv_reader = csv.reader(products_csv)
        for row in csv_reader:
            products_csv_data.append(row)
    return products_csv_data

def similarity_calculator(word1, word2, word3):
    score_1 = rapidfuzz.fuzz.token_set_ratio(word1, word2) 
    score_2 = rapidfuzz.fuzz.token_set_ratio(word1, word3)
    # score_1 = score_1/100
    # score_2 = score_2/100
    score = 0.5*score_1 + 0.5*score_2
    return score

def similarity_calculator2(word1, word2, word3):
    score_1 = rapidfuzz.fuzz.partial_token_ratio(word1, word2) 
    score_2 = rapidfuzz.fuzz.partial_token_ratio(word1, word3)
    # score_1 = score_1/100
    # score_2 = score_2/100
    score = 0.5*score_1 + 0.5*score_2
    return score

def fuzzy_search(exported_data, products_csv_data, options):
    total_matches = []
    no_apple = []
    
    for k in exported_data:
        if (k[1].find("Apple") < 0 and k[1].find("iPad") < 0):
            no_apple.append(k)
    
    for k in no_apple:
        matches = []
        asteriskless = k[1][:(k[1].find("*") if k[1].find("*") > 0 else len(k[1]))]
        spaced = re.sub("([^ ])\(", r"\1 (", asteriskless)
        g_removed = re.sub("\(([4-5]G)\)", r"\1", spaced)
        product = re.sub("\(.*$", "", g_removed)
        specs = re.sub(".*\((.*)\).*", r"\1", g_removed)
        print(product + specs)
        
        for j in products_csv_data:
            if similarity_calculator(product, j[1], j[2]) >= 90:
                if similarity_calculator2(product, j[1], j[2]) >= 90:
                    matches.append(j[2])
        total_matches.append(process.extractOne(product, matches)[0] if process.extractOne(product, matches) else None)
    
    if options == 1:
        for i, j in zip(no_apple, total_matches):
            print(i[1], "=====", j, "\n")

    return total_matches

lazada_links = get_lazada_link("lazada_links.csv")
driver = init_driver()
start = random.randint(0, 66)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Started Scraping Time")
data = scrape_lazada(driver, lazada_links, 0, 66)
logging.info("Finished Scraping Time")
#save_lazada_data(data)

#lazada_links = get_lazada_link("lazada_links.csv")
#start = random.randint(0, 66)
#data = scrape_lazada_beautifulsoup(lazada_links, 0, 66)
#save_lazada_data(data)

#total_matches = fuzzy_search(get_exported_data(), get_products_csv(), 1)
#print("Matched " + str(sum([m is not None for m in total_matches]) / len(total_matches) * 100) + "%")
