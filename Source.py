import pandas as pd
from time import sleep, strftime
import urllib.request , json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # This module import for sending data to input boxes
from selenium.webdriver.common.action_chains import ActionChains #This module import for using space button for scroll down
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#graph api
access_token=''
account_id=''
account=''


def get_account_info(user):
    try:
        with urllib.request.urlopen('https://graph.facebook.com/v6.0/{}?fields=business_discovery.username({})%7Bbiography%2Cfollowers_count%2Cfollows_count%2Cmedia_count%2Cwebsite%7D&access_token={}'.format(account_id,user,access_token)) as url:
            b_user=json.loads(url.read().decode())
            business_discovery=b_user['business_discovery']
        pass
    except:
        return 0
    b_user_dic={'Username':user,'Followers':business_discovery['followers_count'],'Followings':business_discovery['follows_count'],'Media':business_discovery['media_count'],'Bio':business_discovery['biography'],'Website':business_discovery['website']}
    return b_user_dic

#introduce firefox to selenium
firefoxdriver_path = '' # Change this to your own firefox path!
webdriver = webdriver.Firefox(executable_path=firefoxdriver_path)
sleep(2)

#Log in to instagram accounts
username=''
password=''
backup_code='' #for 2-step verification
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

find_username = webdriver.find_element_by_name('username')
find_username.send_keys(username)
find_password = webdriver.find_element_by_name('password')
find_password.send_keys(password)

button_login = webdriver.find_element_by_css_selector('.L3NKy > div:nth-child(1)')
button_login.click()

#this piece is for two-step athunticating
try:
    WebDriverWait(webdriver,100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div")))
except:
    webdriver.find_element_by_name('verificationCode').send_keys(backup_code)
    webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/button').click()

#this piece ignore pop up asking about notifications
sleep(2)
notnow = webdriver.find_element_by_css_selector('button.aOOlW:nth-child(2)') 
notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications

#start business!
businesses=[] #accounts you want to check and send them a message
message=''#message you want to send
for user in businesses:
    #identify user information
    info_dic=get_account_info(user)
    if info_dic==0:
        continue
    followers=info_dic['Followers']
    followings=info_dic['Followings']
    bio=info_dic['Bio']
    website=info_dic['Website']
    media=info_dic['Media']
    if followers>500 and followings/followers <2 and media>15: #specify conditions you want
        webdriver.get('https://www.instagram.com/{}/'.format(user))
        webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/button').click() #click on message button
        WebDriverWait(webdriver,100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/textarea")))
        text_box=webdriver.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/textarea')
        text_box.click()
        text_box.send_keys(message) #send message to box
        ActionChains(webdriver).send_keys(Keys.ENTER).perform()




