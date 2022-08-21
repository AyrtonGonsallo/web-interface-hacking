import os
import pickle
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import tkinter as tk
from tkinter import filedialog as fd
from test2 import getEntrepriseInfos
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from FolderChooser import Folder

#  pyinstaller --onefile --icon "scrapping.ico" --noconsole gui.py
urls = []
entreprisesInfos = [[], [], [], [], []]
folder = Folder()
currenturl=""

def stringify(chaine):
    n = chaine.count(' ')
    for index in range(0, n):
        chaine = chaine.replace(" ", "+")
    chaine = chaine.replace("(", "%28")
    chaine = chaine.replace(")", "%29")
    chaine = chaine.replace(",", "%2C")
    chaine = chaine.replace("'", "%27")
    return chaine


def init():
    thread = Thread(target=getLiens)
    thread.start()



def getLiens():

    url = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui="
    metier = stringify(e2.get())
    region = stringify(e1.get())
    url += metier
    url += "&ou="
    url += region
    url += "&univers=pagesjaunes"
    page = folder.get_currentPage()
    if page > 1:
        pageUrl = "&page="+str(page)
        url += pageUrl
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=" + folder.get_repertoire())
    driver = webdriver.Chrome("C:/chromedriver.exe", options=options)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    infos = soup.findAll("a", {"class": "bi-denomination"})
    if page > 1:
        total = folder.get_total()
    else:
        total=0
    regex1 = re.compile('.*aucun_resultat.*')
    regex2 = re.compile('.*wording-no-responses.*')
    notfound1 = soup.find("p", {"class": regex1})
    notfound2 = soup.find("h1", {"class": regex2})
    if notfound1 is not None:
        mylist.insert(END,notfound1.getText())
        return 0
    elif notfound2 is not None:
        mylist.insert(END,notfound2.getText())
        return 0
    for infos_div in infos:
        titre_lien = infos_div.get('href')#
        if (titre_lien != "#"):
            mylist.insert(END, str(total + 1) + " https://www.pagesjaunes.fr" + titre_lien)
            urls.append("https://www.pagesjaunes.fr" + titre_lien)
            total += 1
        # if total == 20:
        # break
    folder.set_total(total)
    messagebox.showinfo("Collecte de liens", "Liens des professionels récuperés !")
    button3["state"] = NORMAL
    button3["cursor"] = "hand1"
    button1['text'] = "Page "+str(page+1)+" =>"
    driver.close()



def effacer():
    mylist.delete(0, END)
    urls.clear()


def start():
    thread = Thread(target=getInfos)
    thread.start()


def getInfos():
    button4["state"] = NORMAL
    button4["cursor"] = "hand1"
    mylist.delete(0, END)
    i = 0
    for u in urls:
        mylist.insert(END, u)
        res = getEntrepriseInfos(u)
        mylist.insert(END, res)
        entreprisesInfos[0].append(res[0])
        entreprisesInfos[1].append(res[1])
        entreprisesInfos[2].append(res[2])
        entreprisesInfos[3].append(res[3])
        entreprisesInfos[4].append(res[4])
        i += 1
        time.sleep(1)
    messagebox.showinfo("Resultat", "Données extraites !")


def out():
    thread = Thread(target=exporter)
    thread.start()


def exporter():
    mylist.delete(0, END)
    df = pd.DataFrame({'nom': entreprisesInfos[0], 'activite': entreprisesInfos[1], 'numero': entreprisesInfos[2],
                       'site': entreprisesInfos[3], 'adresse': entreprisesInfos[4]})
    if (os.path.exists("entreprises.csv")):
        df.to_csv("entreprises.csv", mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        df.to_csv("entreprises.csv", index=False, encoding='utf-8-sig')
    messagebox.showinfo("Resultat", "Document csv exporté !")


def reboot():
    e1.delete(0, END)
    e2.delete(0, END)
    folder.erease()
    urls.clear()
    button3["state"] = DISABLED
    button4["state"] = DISABLED
    mylist.delete(0, END)
    entreprisesInfos.clear()
    button1['text'] = "chercher Urls"


master = Tk()
n_rows = 8
n_columns = 15
master.title('Ayrton´s Python Web Scrapping 1.0.3')
master.iconbitmap("C:/scrapping.ico")
for i in range(n_rows):
    master.grid_rowconfigure(i, weight=1)
for i in range(n_columns):
    master.grid_columnconfigure(i, weight=1)

myFont = Font(family='Helvetica', size=15, weight='bold')


def select_folder():
    filename = fd.askdirectory(
        title='Open a file',
        initialdir='/')
    folder.set_repertoire(filename)
    print(filename)
    if filename != "":
        f2 = open("repertoire.txt", "wb")
        pickle.dump(filename, f2)
        f2.close()
        messagebox.showinfo("Confirmation",
                            "Le chemin a bien été trouvé et sauvegardé !")


# open button
open_button = tk.Button(
    master, fg='white', bg='#003eb1', font=myFont, cursor="hand1",
    text='Charger profil chrome',
    command=select_folder
)
open_button.grid(row=0, column=0)

Label(master, text='region', font=myFont).grid(row=1, column=0)
Label(master, text='metier', font=myFont).grid(row=2, column=0)
e1 = Entry(master)
e2 = Entry(master)
e2.insert(-1, 'zingueur')
e1.insert(-1, 'caluire et cuire 69')
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
button1 = Button(master, text='chercher Urls', fg='white', bg='#00b118', font=myFont, cursor="hand1",
                 command=init)
button1.grid(row=3, column=1)
button2 = Button(master, text='effacer', fg='white', bg='#96b100', font=myFont, cursor="hand1",
                 command=effacer, )
button2.grid(row=3, column=0)
button3 = Button(master, text='traiter', fg='white', bg='#b13800', font=myFont, cursor="circle",
                 command=start)
button3.grid(row=3, column=2)
button4 = Button(master, text='exporter', fg='white', bg='#895896', font=myFont, cursor="circle",
                 command=out)
button4.grid(row=3, column=3)
button5 = Button(master, text='réinitialiser', fg='white', bg='#19ad7c', font=myFont, cursor="hand1",
                 command=reboot)
button5.grid(row=5, column=0)
button3["state"] = DISABLED
button4["state"] = DISABLED
frame = Frame(master, highlightbackground="black", highlightthickness=2)
frame.grid(row=4, column=4)
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar2 = Scrollbar(frame, orient='horizontal')
scrollbar2.pack(side=BOTTOM, fill=X)
mylist = Listbox(frame, width=45, height=13, bg='black', fg='white', font=myFont, xscrollcommand=scrollbar2.set,
                 yscrollcommand=scrollbar.set)
mylist.insert(END, 'Ici seront affichés les résultats')
mylist.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=mylist.yview)
scrollbar2.config(command=mylist.xview)

mainloop()
