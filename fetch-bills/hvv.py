from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import datetime
import time

import helper

url = "https://www.hvv.de/en/meinhvv#/login"
uname = helper.parse_config('HVV', 'HVV_LOGIN_USER')
pw = helper.parse_config('HVV', 'HVV_LOGIN_PW')

def fetch_bill(driver):
    # Login
    print("Opening login page")
    driver.get(url)
    mainWindow = driver.current_window_handle
    time.sleep(1)
    print("Performing login")
    driver.find_elements_by_xpath('//*[@id="username"]')[0].send_keys(uname)
    driver.find_elements_by_xpath('//*[@id="password"]')[0].send_keys(pw)
    time.sleep(1)
    submitButton = driver.find_element_by_xpath('//button[@name="button" and @type="submit"]')
    driver.execute_script("arguments[0].scrollIntoView();", submitButton)
    submitButton.click()
    # Open tickets
    time.sleep(1)
    print("Opening ticket history")
    ticketHistory = driver.find_element_by_xpath('//*[text()="History of orders at the Online Shop"]')
    driver.execute_script("arguments[0].scrollIntoView();", ticketHistory)
    ticketHistory.click()
    time.sleep(1)
    tableRows = driver.find_elements_by_class_name('c-accordion--shop-history')
    print("Iterating over every row in the bills table")
    for row in tableRows:
        bill = row.find_element_by_class_name("c-accordion__shop-history-header-data--order-date")
        print("Checking bill with date " + bill.text)
        if helper.same_week(bill.text, '%d %B %Y %H:%M'):
            print("The bill is from this week")
            print("Expanding the dropdown for this ticket")
            bill.click()
            time.sleep(10)
            link = row.find_element_by_class_name('o-button__button')
            print("Found link with id "+ link.get_attribute("id"))
            print("Downloading bill")
            driver.execute_script("window.open('" + link.get_attribute("href") + "', '_blank')")
        else:
            print("The bill is not from this week, ignoring")
    print("Closing browser")
    time.sleep(2)
    driver.quit()
