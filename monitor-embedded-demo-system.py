""" simple script to monitor embedded demo system """
""" author: Justin Craycraft """
""" email: jraycraft@tableau.com """


import os
import time
import psutil
import json
import requests
# import unittest
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

status = {}

def check_kill():
    """function to manage webdriver process"""
    try:
        driver_process = psutil.Process(driver.service.process.pid)
        if driver_process.is_running():
            print ("driver is running")
            status.update({"driver_status": "driver is running"})

            firefox_process = driver_process.children()
            if firefox_process:
                firefox_process = firefox_process[0]

                if firefox_process.is_running():
                    print("firefox is still running. no sweat, we can quit the driver")
                    status.update({"driver_status": "firefox is still running. no sweat, we can quit the driver"})
                    driver.quit()
                else:
                    print("firefox is dead; can't quit, so lets kill the driver process")
                    status.update({"driver_status": "firefox is dead; can't quit, so lets kill the driver process"})
                    firefox_process.kill()
            else:
                print("driver has died")
                status.update({"driver_status": "driver has died"})
        else:
            print("driver is not currently running")
            status.update({"driver_status": "driver is not currently running"})
    except:
        print("no driver process found")
        # status.update({"driver_status": "no driver process found"})

def start():
    """function to start web driver"""
    try:
        # driver_path = '/Users/jcraycraft/Documents/Projects/geckodriver/geckodriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.implicitly_wait(10)



        # driver_path = '/opt/teds_ec2_monitor/geckodriver'
        # binary = '/opt/teds_ec2_monitor/firefox/firefox-bin'
        # # options = Options()
        # # options.add_argument('-headless')
        # options = Options()
        # options.headless = True
        # # options.headless = False
        # # driver = webdriver.Firefox(executable_path = driver_path, options=options)
        #
        #
        # driver = webdriver.Firefox(firefox_binary=binary, executable_path = driver_path, options=options)

        driver.implicitly_wait(15)
        url = "https://embedded.tableau.com"
        driver.get(url)
        status.update({"initialized headless browser" : "pass"})
        driver.maximize_window()
        return driver

    except WebDriverException as ex:
        status.update({"error": ex.msg})
        print(ex.msg)



def stop():
    """funcion to stop web driver"""
    driver.quit()
    result = status

def test():

    analytics_status = {}

    try:
        time.sleep(20)
        url = 'en/retail/'
        elem = driver.find_element_by_xpath('//a[@href="'+ url +'"]')
        elem.click()
    except NoSuchElementException as ex:
        status.update({"error @ login": ex.msg})

    try:
        time.sleep(5)
        url = '#menu'
        elem = driver.find_element_by_xpath('//a[@href="'+ url +'"]')
        elem.click()
    except NoSuchElementException as ex:
        status.update({"error @ login": ex.msg})

    try:
        time.sleep(5)
        div_id = 'username'
        elem = driver.find_element_by_id(div_id)
        elem.click()
    except NoSuchElementException as ex:
        status.update({"error @ login": ex.msg})

    try:
        time.sleep(5)
        elem = driver.find_element_by_class_name('username-item')
        elem.click()
    except NoSuchElementException as ex:
        status.update({"error @ login": ex.msg})

    try:
        time.sleep(5)
        class_name = 'loginbutton'
        elem = driver.find_element_by_class_name(class_name)
        elem.click()
        status.update({"login" : "pass"})

    except NoSuchElementException as ex:
        status.update({"error @ login": ex.msg})

    try:
        time.sleep(20)
        iframes = driver.find_elements_by_xpath("//iframe[@title='Data Visualization']")

        if len(iframes) == 2:
            status.update({'viz count @ workspace' : 'pass'})

    except NoSuchElementException as ex:
        status.update({'error counting viz @ workspace': ex.msg})

    try:
        target_id = 'news-button'
        elem = driver.find_element_by_id(target_id)
        elem.click()

    except NoSuchElementException as ex:
            status.update({"navigation error @ blog": ex.msg})

    try:
        time.sleep(20)
        iframes = driver.find_elements_by_xpath("//iframe[@title='Data Visualization']")
        if len(iframes) == 2:
            status.update({'viz count @ blog' : 'pass'})

    except NoSuchElementException as ex:
        status.update({"error counting viz @ blog": ex.msg})

    try:
        target_id = 'guided-analytics-button'
        elem = driver.find_element_by_id(target_id)
        elem.click()

    except NoSuchElementException as ex:
        status.update({"navigation error @ guided analytics": ex.msg})

    try:
        time.sleep(20)
        viz_images = driver.find_elements_by_xpath('//*[starts-with(@src, "/tabrestrest")]')
        viz_images = driver.find_elements_by_xpath('//*[starts-with(@src, "/tabrestrest")]')
        count = len(viz_images)

    except NoSuchElementException as ex:
        status.update({"error @ guided analytics": ex.msg})


    for i in range(count):

        try:

            viz = driver.find_elements_by_xpath('//*[starts-with(@src, "/tabrestrest")]')[i]
            actions = ActionChains(driver)
            actions.move_to_element(viz)
            parent_elem = viz.find_element_by_xpath('..')
            url_click = parent_elem.get_attribute("href")

            # get views/workbook/view substring
            start = url_click.find('workbook')
            end = url_click.find('initialview')
            wb_url_click = url_click[start + 8 : end]
            start = url_click.find('initialview')
            view_url_click  = url_click[start + 12:]
            wb_view_url_click = wb_url_click + view_url_click

            actions.click()
            actions.perform()

        except NoSuchElementException as ex:
            status.update({"navigation error @ guided analytics": ex.msg})

        try:
            time.sleep(20)
            iframe = driver.find_element_by_xpath("//iframe[@title='Data Visualization']")
            iframe_src = iframe.get_attribute("src")
            # print(iframe_src)

        except NoSuchElementException as ex:
            status.update({"navigation error @ guided analytics": ex.msg})

        try:
            if iframe_src is not None:
                url_iframe_match = iframe_src.find(wb_view_url_click)
                if url_iframe_match != -1:
                    analytics_status.update({wb_view_url_click : 'pass'})
                    # print(analytics_status)

            target_id = 'nav-caret'
            elem = driver.find_element_by_id(target_id)
            elem.click()
            time.sleep(3)

        except NoSuchElementException as ex:
            status.update({"navigation error @ guided analytics": ex.msg})

        try:
            target_id = 'guided-analytics-button'
            elem = driver.find_element_by_id(target_id)
            elem.click()
            time.sleep(10)

        except NoSuchElementException as ex:
            status.update({"navigation error @ guided analytics": ex.msg})

    status.update({'analytics' : analytics_status})





def sendToSlack():

    jsonData = json.dumps(status)

    message = {
        "text": jsonData
    }

    # jsonData = json.dumps(message)
    slack_channel_url =  'https://hooks.slack.com/services/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'
    response = requests.post(slack_channel_url, json=message)

    print("Status code: ", response.status_code)
    print("Printing Entire Post Request")
    # print(response.json())

    # response.raw
    print(response.text)



if __name__ == '__main__':
    # check_kill()
    driver = start()
    test()
    stop()

    print(status)
    # sendToSlack(output)
