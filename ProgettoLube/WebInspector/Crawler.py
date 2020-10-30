import os
import urllib
from os.path import basename

import requests
from bs4 import BeautifulSoup

#TODO: controllare anche i tag picture o altri(boh) perche le immagini non stanno solo dentro i tag img
def avvia(url):
    lista = findhref(url)
    for element in lista:
        print("ANALIZZO : "+element)

        page = requests.get(element)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        images = body.findAll('img')
        for image in images:
            # print image source
            print(image['src'])
            urlimg = image['src']
            if urlimg[0:4] != "http":
                urlimg = element + urlimg
            print("Salvo immagine")
            path = os.path.join(r"C:\Users\matti\PycharmProjects\WebInspector\images" + "\\" + basename(urlimg))
            print(path)
            #TODO: fare un if dove si controlla requests.get(urlimg).content se restituisce qualcosa che è minore di 10k
            with open(path, "wb") as f:
                f.write(requests.get(urlimg).content)



# Per trovare tutti i sotto link di un sito root da cui scaricare le foto
# forse bisognerebbe riusarlo anche per i sotto link stessi
# Ritorna la lista dei sotto link di un seed
def findhref(root):
    page = requests.get(root)
    soup = BeautifulSoup(page.content, 'html.parser')
    lista=[]
    lista.append(root)
    for link in soup.find_all('a'):
        if (link.get('href'))[0:4] != 'http':
            # print("TREE "+root + '/' + (link.get('href')))
            href = root + "/" +(link.get('href'))
            lista.append(href)
    #print(href_tags)
    return lista
