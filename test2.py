from time import sleep
import regex as re
from selenium import webdriver
from bs4 import BeautifulSoup
from FolderChooser import Folder

folder = Folder()


def getEntrepriseInfos(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=" + folder.get_repertoire())
        driver = webdriver.Chrome("C:/chromedriver.exe", options=options)
        driver.get(url)
    except:
        print("ptit probleme")
    sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    entrepriseInfos = []
    regex1 = re.compile('.*pj-on-autoload teaser-header.*')
    infos = soup.find("div", {"class": regex1})
    try:
        nom = infos.find("h1", {"class": "noTrad no-margin"}).text
    except:
        nom = ""
    try:
        activite = infos.find("span", {"class": "activite"}).text
    except:
        activite = ""
    try:
        regex2 = re.compile('.*teaser-footer fd-bloc.*')
        contacts = soup.find("div", {"class": regex2})
    except:
        print(nom)

    try:
        regex2 = re.compile('.*btn btn_tertiary pj-lb pj-link.*')
        numero = contacts.find("a", {"class": regex2}).text.strip()
    except:
        numero = ""
        print(nom)
    try:
        regex2 = re.compile('.*Site internet du professionnel nouvelle fenêtre.*')
        siteLink = contacts.find("a", {"title": regex2})
        site = siteLink.find("span", {"class": "value"}).text
    except:
        site = "https://ayr-streaming.herokuapp.com/"
        print(nom)
    try:
        adressesLink = contacts.find("a", {
            "class": "teaser-item black-icon address streetAddress clearfix map-click-zone pj-lb pj-link"})
        adresseTab = adressesLink.findAll("span", {"class": "noTrad"})
        adresse = ""
        for adr in adresseTab:
            adresse += adr.text
    except:
        adresse = ""
        print(nom)

    entrepriseInfos.append(nom)
    entrepriseInfos.append(activite)
    entrepriseInfos.append(numero)
    entrepriseInfos.append(site)
    entrepriseInfos.append(adresse)
    driver.close()
    return entrepriseInfos
