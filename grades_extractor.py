# Imports
from bs4 import BeautifulSoup
import re
import os
from time import sleep
import urllib.request
import requests
import errno
import shutil
import sys
import traceback
import requests
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pickle 
import collections
import notify2
from time import gmtime, strftime

# Import variables
username = os.environ['uservar']
pwd = os.environ['passvar']

# Selenium configurations
chromeOptions = webdriver.ChromeOptions()
root_path = "./"
chromedriver = root_path + "chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
driver.minimize_window()

# User agent configurations
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'

# Load website
driver.get("https://apply.iiita.ac.in/unified_login/")
time.sleep(3)

# Login
driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(username)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(pwd)
time.sleep(1)
driver.find_element_by_xpath("/html/body/div/div/div/section/form/div[3]/input[2]").click()
time.sleep(5)

# You may increase below timer to 10 if you have slow internet connection.
time.sleep(5)


results = []
try:
	for row in driver.find_elements_by_xpath("/html/body/div/div/div[3]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div"):
		results.append(row.text)
except Exception as e:
	print("Extraction attempt failed. Please try again with correct Credentials.")
	sys.exit()
filename = 'results.sav'

prev_results = pickle.load(open(filename, 'rb'))
notify2.init('IIITA GRADE NOTIFIER')

if collections.Counter(results) == collections.Counter(prev_results):
	print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + ": No updates found")
else:
	print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + ": Updates found")
	pickle.dump(results, open(filename, 'wb'))
	display_str =""
	for result in results:
		display_str += result
		display_str += "\n" 
	print(display_str)
	alert = notify2.Notification('IIITA GRADE NOTIFIER', 'Grades have been updated')
	alert.show()

driver.close()
