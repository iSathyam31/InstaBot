#import libraris
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bsp
import bs4
import time
import pandas as pd


## Username & Password
username = "SAMPLE USERNAME"       
password = "SAMPLE PASSWORD"

#setting up driver
path = "/Users/bhard/Downloads/chromedriver_win32/chromedriver"   ## depends on sytem
driver = webdriver.Chrome(executable_path = path)
driver.maximize_window()

## opening site
site = "https://www.instagram.com/"
driver.get(site)

############################
## 1. LOG IN TO INSTA HANDLE##
## function for log in

def log_in_to_account(driver, username, password):
    
    login = True
    
    wait = WebDriverWait(driver, 10)  ## explicit wait
    
    try:
        ## move to login page
        log_in_path = '//p[@class = "izU2O"]//a'
        log_in = wait.until(EC.element_to_be_clickable((By.XPATH,log_in_path)))
        log_in.click()

        time.sleep(3)   ## waiting for website to switch

        ## enter username
        username_ = wait.until(EC.presence_of_element_located((By.NAME,"username")))
        username_.send_keys(username)

        ## enter password
        password_ = wait.until(EC.presence_of_element_located((By.NAME,"password")))
        password_.send_keys(password)

        ## click login
        log_in_path = '//button[contains(@class, "sqdOP")]'
        log_in = wait.until(EC.presence_of_element_located((By.XPATH,log_in_path)))
        log_in.submit()

        time.sleep(3)  ## waiting for website to switch
        
    except Exception:
        login = False
        
    if login:
        remove_notification(driver, wait)
    
    return login

def remove_notification(driver, wait):
    ## Notifination popup setting up not now, if occur
    try:
        popup_path = '//button[contains(@class, "HoLwm")]'
        not_now_btn = wait.until(EC.element_to_be_clickable((By.XPATH,popup_path)))
        not_now_btn.click()
    except NoSuchElementException:
        print("No Notification Pop up occur")
        
        
login = log_in_to_account(driver, username, password)
if login:
    print("log in successfully")
else:
    print("log in unseccussful, give one more try")    
    
    
    
#######################################
## 2. SEARCHING FOOD ##
## function to search something string like 'food' here

def Search_Handle(driver, string):
    
    wait = WebDriverWait(driver, 10)       ## Explicit Wait
    
    ## search 'food' 
    search_path = '//input[contains(@class, "x3qfX")]'
    search_bar = wait.until(EC.presence_of_element_located((By.XPATH,search_path)))
    search_bar.send_keys(string)
    time.sleep(3)
    
    ## Extracting the handles
    handles = []
    lst = driver.find_elements_by_class_name("Ap253")
    for i in lst:
        handle = i.get_attribute("innerHTML")
        if handle[0] == "#":
            handle = handle[1:]
        handles.append(handle)
        
    ## Erasing string from search bar
    path = '//div[contains(@class, "coreSpriteSearchClear")]'
    remove_btn = wait.until(EC.element_to_be_clickable((By.XPATH,path)))
    remove_btn.click()
        
    return handles   

string = "food"     ## can be changed
handle_list = Search_Handle(driver, string)
cnt = 1
for i in handle_list:
    print(cnt, ".", i)
    cnt += 1     
    
    
###############################
## 3. Follow/Unfollow
## function to follow a given handle/profile

def follow(driver, profile):
    
    previously_follow = False
    
    wait = WebDriverWait(driver, 10)       ## Explicit Wait
    
    ## opening profile
    search_open(driver, profile)
    
    ## following handle
    path = '//button[contains(@class, "_5f5mN")]'
    btn = wait.until(EC.presence_of_element_located((By.XPATH,path)))
    
    ## Checking if i am following or not
    if(btn.get_attribute('innerHTML') == "Follow"):
        btn = wait.until(EC.element_to_be_clickable((By.XPATH,path)))
        btn.click()
    else:
        previously_follow = True
        
    ## coming back to home page
    home = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "oJZym"]/a')))
    home.click()
    
    return previously_follow    


## function to unfollow a given profile

def unfollow(driver, profile):
    
    previously_unfollow = False
    
    wait = WebDriverWait(driver, 10)       ## Explicit Wait
    
    ## opening profile
    search_open(driver, profile)
    
    ## unfollowing handle
    path = '//button[contains(@class, "_5f5mN")]'
    btn = wait.until(EC.presence_of_element_located((By.XPATH,path)))
    
    ## Checking if i am unfollowing or not
    if(btn.get_attribute('innerHTML') != "Follow"):
        btn = wait.until(EC.element_to_be_clickable((By.XPATH,path)))
        btn.click()
        
        ## unfollowing
        path = '//button[contains(@class, "aOOlW ")]'
        btn = wait.until(EC.element_to_be_clickable((By.XPATH,path)))
        btn.click()
    else:
        previously_unfollow = True
        
    ## coming back to home page
    home = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "oJZym"]/a')))
    home.click()
    
    return previously_unfollow   

## 4

profile = "So Delhi"        ## can be changed

## follow
previously_follow = follow(driver, profile)
if(previously_follow):
    print("Already Following")
else:
    print("Start Following")
    
    
time.sleep(3)    


## unfollow
previously_unfollow = unfollow(driver, profile)
if(previously_unfollow):
    print("Already not Following")
else:
    print("Start Unfollowing")
    
###################################
## 4. Like/Unlike ##
## function to liking the first no_of_post of a profile

def like(driver, profile, no_of_post):
    
    wait = WebDriverWait(driver, 10)       ## Explicit Wait
    
    previously_like = False
    
    ## opening profile
    search_open(driver, profile)
    
    ## Extracting The No_of_posts
    btn = driver.find_elements_by_class_name("_bz0w")
    path = "//div[contains(@class,'_bz0w')]/a"
    btn = wait.until(EC.presence_of_all_elements_located((By.XPATH,path)))
    while len(btn) < no_of_post:
        driver.execute_script('window.scrollBy(0, 1000);')         ## Scrolling
        btn = wait.until(EC.presence_of_all_elements_located((By.XPATH,path)))
        
    print("number of posts extracted: ", len(btn))
    
    cnt = 1
    for i in btn:
        i.click()
        time.sleep(3)
        
        ## Checking if ith post is liked before or not
        cond = driver.find_elements_by_xpath("//*[name()='svg']")[6]
        if(cond.get_attribute("aria-label") == "Like"):    ## finding the like one
            path = '//button[contains(@class, "wpO6b")]'
            like_unlike = wait.until(EC.element_to_be_clickable((By.XPATH,path)))
            like_unlike.click()
        else:
            previously_like = True
            
        ## exiting the post
        exit = driver.find_element_by_class_name("ckWGn")
        exit.click()
        
        ## mainatining the number of post
        if cnt == no_of_post:
            break
        cnt += 1
        
    ## coming back to home page
    home = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "oJZym"]/a')))
    home.click()
    
    return previously_like   
   
   
## function to disliking the first no_of_post of a profile

def unlike(driver, profile, no_of_post):
    
    wait = WebDriverWait(driver, 10)       ## Explicit Wait
    
    previously_unlike = False
    
    ## opening profile
    search_open(driver, profile)
    
    ## Extracting The No_of_posts
    btn = driver.find_elements_by_class_name("_bz0w")
    path = "//div[contains(@class,'_bz0w')]/a"
    btn = wait.until(EC.presence_of_all_elements_located((By.XPATH,path)))
    while len(btn) < no_of_post:
        driver.execute_script('window.scrollBy(0, 1000);')         ## Scrolling
        btn = wait.until(EC.presence_of_all_elements_located((By.XPATH,path)))
        
    print("number of posts extracted: ", len(btn))
    
    cnt = 1
    for i in btn:
        i.click()
        time.sleep(3)
        
        ## Checking if ith post is liked before or not
        cond = driver.find_elements_by_xpath("//*[name()='svg']")[6]
        if(cond.get_attribute("aria-label") == "Unlike"):    ## finding the like one
            path = '//button[contains(@class, "wpO6b")]'
            like_unlike = wait.until(EC.element_to_be_clickable((By.XPATH,path)))
            like_unlike.click()
        else:
            previously_unlike = True
            
        ## exiting the post
        exit = driver.find_element_by_class_name("ckWGn")
        exit.click()
        
        ## mainatining the number of post
        if cnt == no_of_post:
            break
        cnt += 1
        
    ## coming back to home page
    home = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "oJZym"]/a')))
    home.click()
    
    return previously_unlike   
 
 
 
## 5

profile = "dilsefoodie"        ## can be changed
no_of_post = 30

## like
previously_like = like(driver, profile, no_of_post)
if(previously_like):
    print("Already one of the post is liked")
else:
    print("No Post is liked before")
    
    
time.sleep(3)

    
## unlike
previously_unlike = unlike(driver, profile, no_of_post)
if(previously_unlike):
    print("Already one of the post is not liked")
else:
    print("Unliked all now, no post is disliked before")       