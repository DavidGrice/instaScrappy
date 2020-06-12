# IMPORT DEPENDENCIES/LIBRARIES
import urllib
import urllib3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import os
import getpass
import re
from pynput.keyboard import Key, Controller 

#Instagram login
def instagramLogin(wd):
    # find element username and password for inputting login info
    user = wd.find_element_by_name("username")
    password = wd.find_element_by_name("password")
    # Clear the fields
    user.clear()
    password.clear()
    # Ask user for login information
    instagram_username = getpass.getpass("Please enter your Instagram user account: ")
    user.send_keys(instagram_username)
    instagram_password = getpass.getpass("Please enter your Instagram password: ")
    password.send_keys(instagram_password)
    time.sleep(5)
    wd.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(5)
    time.sleep(5)
    return

# CREATE ONE FOLDER FOR MULTIPLE FOLDERS
def makeMainDirectory(directory):
    main_directory = directory
    if not os.path.isdir(main_directory):
        os.mkdir(main_directory)
        os.chdir(main_directory)

# LOCATING AND SOTRING INFOR FOR INSTAGRAM ACCOUNT
def getInstagramAccount(instagramUsername, wd):
    time.sleep(5)
    instagram_holder = instagramUsername
    wd.get('https://www.instagram.com/'+instagram_holder+'/')
    # scraping photos
    scrapeInstagramAccountImages(instagram_holder, wd)

    # get inspector
    getInspector()

    # instagram actions
    hrefActions = getInstagramActions(instagram_holder, wd)

    # scraping following
    following = getFollowingInformation(hrefActions, wd)
    hrefActions = getInstagramActions(instagram_holder, wd)
    print(following)

    # scraping followers
    followers = getFollowersInformation(hrefActions, wd)
    print(followers)

def scrapeInstagramAccountImages(instagram_holder,wd):
    lenOfPage = wd.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage")
    match=False
    x = 100
    while(match == False):

        #directory of instagram account
        directory = instagram_holder
        lastCount = lenOfPage
        instagram_urls = []
        time.sleep(30)
        instagram_capture = wd.find_elements_by_xpath("//img[@class='FFVAD']")

        for i in instagram_capture:
            # appending src for images to download
            instagram_urls.append(i.get_attribute('src'))
        
        #create directory for instagram account
        if not os.path.isdir(directory):
            os.mkdir(directory)
        
        for i, link in enumerate(instagram_urls):
            path = os.path.join(instagram_holder, '{:06}.jpg'.format(i+x))
            
            try:
                urllib.request.urlretrieve(link, path)
            except:
                print("Unable to download and place inside of folder")
        
        x+=100
        lenOfPage = wd.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage")

        if (lastCount==lenOfPage):
            match=True

## ACTIONS FOR GETTING FOLLOWER/FOLLOWING
def getInstagramActions(instagram_holder, wd):
    wd.get('https://www.instagram.com/'+instagram_holder+'/')
    time.sleep(5)
    href_temp = wd.find_elements_by_xpath("//li[@class=' LH36I']")
    return href_temp

def getInspector():
    # MAKE SURE THAT YOU HAVE THE CHROME DRIVER CLICKED ON
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press('i')
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
    keyboard.release('i')
    time.sleep(5)

def getFollowingInformation(actions, wd):
    following_names = []
    following = actions[2]
    following.click()
    time.sleep(20)
    following_temp = wd.page_source
    following_data = bs(following_temp, 'html.parser')
    following_name = following_data.find_all('a')
    for i in following_name:
        following_names.append(i.get("title"))
    clean_following_names = [x for x in following_names if x != None]
    return clean_following_names

def getFollowersInformation(actions, wd):
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


def main():
    DRIVER_PATH = './chromedriver.exe'
    wd = webdriver.Chrome(executable_path = DRIVER_PATH)
    wd.get('https://www.instagram.com/accounts/login/')
    time.sleep(5)
    instagramLogin(wd)
    mainAccountDirectory = input(str("Please type a name to store your instagram accounts into: "))
    makeMainDirectory(mainAccountDirectory)
    while(True):
        instagramAccount = input(str("Please type Instagram account for me to find or 'quit' to end program: "))
        if(instagramAccount=='quit'):
            return False
        else:
            ### INSERT FUNCTIONS
            getInstagramAccount(instagramAccount, wd)

if __name__ == "__main__":
    main()