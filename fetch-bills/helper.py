import sys
import time
import os
import datetime
import configparser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdav3.client import Client

def parse_config(varGroup, varName):
    # Read the ini file
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

    # Set variables
    return config.get(varGroup, varName)

def start_browser():
    path = directory()
    print("Preparing Firefox options")
    options = Options()
    options.headless = True # False
    options.set_preference('browser.download.folderList', 2) # custom location
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.download.dir', path)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
    options.set_preference('pdfjs.disabled', True)
    print("Starting Firefox")
    driver = webdriver.Firefox(options=options, executable_path='/usr/bin/geckodriver') # /usr/local/bin/geckodriver
    print ("Headless Firefox Initialized")
    return driver

def same_week(givenDate, format):
    d1 = datetime.datetime.strptime(str(givenDate), str(format))
    d2 = datetime.datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year

def directory():
    today = datetime.date.today()
    year, week_num, day_of_week = today.isocalendar()
    directory_name = str(year) + "_cw" + str(week_num)
    path = targetPath + "/" + directory_name
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def download(url, dest):
    import requests
    file = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(file.content)

def upload_webdav():
    options = {
     'webdav_hostname': parse_config('WEBDAV', 'WEBDAV_UPLOAD_URL'),
     'webdav_login':    parse_config('WEBDAV', 'WEBDAV_UPLOAD_USER'),
     'webdav_password': parse_config('WEBDAV', 'WEBDAV_UPLOAD_PW')
    }
    remotePath = parse_config('WEBDAV', 'WEBDAV_UPLOAD_PATH')
    client = Client(options)
    client.verify = False
    today = datetime.date.today()
    year, week_num, day_of_week = today.isocalendar()
    path = str(year) + "_cw" + str(week_num)

    if not client.check(remotePath + "/" + path):
        client.mkdir(remotePath + "/" + path)

    kwargs = {
        'remote_path': remotePath + "/" + path + "/",
        'local_path':  targetPath + "/" + path + "/"
    }
    client.upload_async(**kwargs)

targetPath = parse_config('GENERAL', 'DOWNLOAD_PATH')
