from selenium import webdriver
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
#
##PROXY = "11.456.448.110:8080"
##PROXY="60.54.16.223:8888"
##PROXY="1.32.49.253:8080"
##PROXY="128.199.233.192:3128"
#options = webdriver.ChromeOptions()
##options.add_argument('--proxy-server=%s' % PROXY)
#
#chrome = webdriver.Chrome(executable_path="chromedriver", options=options)
#
#format = "%(asctime)s: %(message)s"
#logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
#logging.info("Start time")
#
#chrome.get("https://www.lazada.com.my/products/apple-ipad-mini-6th-gen-wi-fi-i2481158753.html")
##WebDriverWait(chrome, 5).until(EC.visibility_of_element_located((By.XPATH, "//h1[@class = 'pdp-mod-product-badge-title']")))
#
#print(chrome.find_element(By.ID, "pdp-nav").text)
#logging.info("End time")
#
#chrome.quit()
#def testUserLocationZurich(self):
#    self.chrome.get(self.url)
#    search = self.chrome.find_element_by_id('user-city')
#    self.assertIn('Zurich', search.text)

#driver = webdriver.Chrome(executable_path="chromedriver")
##driver.get("https://www.google.com")
#driver.get("https://www.lazada.com.my/products/apple-ipad-mini-6th-gen-wi-fi-i2481158753.html")
#try:
#    time.sleep(5)
#    element = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.CLASS_NAME, "top-links-item orange"))
#    )
#    print(element.text)
#finally:
#    driver.quit()


def get_product_name(driver, class_name):
    return driver.find_element(By.XPATH, "//h1[@class = '" + class_name + "']").text

webdriver.Firefox(service=Service(GeckoDriverManager().install()))

driver = webdriver.Firefox()
driver.get("https://www.lazada.com.my/products/honor-magicbook-x15-i3-2021-space-grey-8gb-ram-256gb-original-1-year-warranty-by-honor-malaysia-i2608649455-s11730638464.html?mp=1&freeshipping=1")

print(get_product_name(driver, "location__address"))
driver.quit()
