#!/usr/bin/env python
# coding: utf-8

# ## Imports

import urllib
import urllib3
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import os
import getpass
import re
from pynput.keyboard import Key, Controller

def scrapeInstagramAccountImages(instagram_holder):
    lenOfPage = wd.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    x=100
    while(match==False):

        directory = instagram_holder
        lastCount = lenOfPage
        time.sleep(30)
        test_urls = []
        testy = wd.find_elements_by_xpath('//img[@class="FFVAD"]')

        for i in testy:
            test_urls.append(i.get_attribute('src'))

        if not os.path.isdir(directory):
            os.mkdir(directory)

        for i,link in enumerate(test_urls):
            path = os.path.join(instagram_holder,'{:06}.jpg'.format(i+x))
            try:
                urllib.request.urlretrieve(link, path)
            except:
                print('failure')

        x+=100

        lenOfPage = wd.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        if lastCount==lenOfPage:
            match=True

def makeMainDirectory(directory):
    main_directory = directory
    if not os.path.isdir(main_directory):
        os.mkdir("INSTAGRAM_ACCOUNTS")
        os.chdir("INSTAGRAM_ACCOUNTS")
    return

def getFollowingInformation(actions):
    following_names = []
    following = actions[2]
    following.click()
    time.sleep(20)
    follow_temp = wd.page_source
    following_data = bs(follow_temp, 'html.parser')
    following_name = following_data.find_all('a')
    for i in following_name:
        following_names.append(i.get("title"))
    clean_following_names = [x for x in following_names if x != None]
    return clean_following_names

def getInstagramActions(instagram_holder):
    wd.get('https://www.instagram.com/'+instagram_holder+'/')
    time.sleep(5)
    href_temp = wd.find_elements_by_xpath("//li[@class=' LH36I']")
    return href_temp

def getFollowersInformation(actions):
    followers_names = []
    followers = actions[1]
    followers.click()
    time.sleep(20)
    followers_temp = wd.page_source
    followers_data = bs(followers_temp, 'html.parser')
    followers_name = followers_data.find_all('a')
    for i in followers_name:
        followers_names.append(i.get("title"))
    clean_followers_names = [x for x in followers_names if x != None]
    return clean_followers_names

def getInstagramAccount(instagram_username):
    instagram_holder = instagram_username
    wd.get('https://www.instagram.com/'+instagram_holder+'/')
    scrapeInstagramAccountImages(instagram_holder)
    time.sleep(5)
    getInspector()
    hrefActions = getInstagramActions(instagram_holder)
    following = getFollowingInformation(hrefActions)
    hrefActions = getInstagramActions(instagram_holder)
    followers = getFollowersInformation(hrefActions)
    getInspector()
    time.sleep(5)
    return

def instagramLogin():
    user = wd.find_element_by_name("username")
    password = wd.find_element_by_name("password")
    # Clear the input fields
    user.clear()
    password.clear()
    instagram_username = getpass.getpass("Please enter your Instagram user account: ")
    user.send_keys(instagram_username)
    instagram_password = getpass.getpass("Please enter your Instagram password: ")
    password.send_keys(instagram_password)
    time.sleep(5)
    wd.find_element_by_xpath("//button[@type='submit']").click()
    # Keep the page loaded for 8 seconds
    time.sleep(8)
    wd.get('https://www.instagram.com/'+instagram_username+'/')
    time.sleep(5)
    return

def getInspector():
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press('i')
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
    keyboard.release('i')
    time.sleep(5)


# ## Driver initiation + going to instagram

DRIVER_PATH = '../WEBSCRAPING/chromedriver.exe'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
time.sleep(5)
wd.get('https://www.instagram.com/accounts/login/')
time.sleep(5)

# ## Username + password for logging into Insta

instagramLogin()

# ## Gathering all following usernames

makeMainDirectory("INSTAGRAM_ACCOUNTS")
instagramAccount = input(str("Please type an instagram username for me to find: "))
getInstagramAccount(instagramAccount)
wd.close()

## IMPROVEMENTS
## Make list of followers and following into a scroll down event.