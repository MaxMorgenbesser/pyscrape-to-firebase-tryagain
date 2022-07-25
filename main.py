#importing packages to be used later
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTML
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase
from requests_html import HTMLSession

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)
db=firestore.client()
firebase = firebase.FirebaseApplication('https://scraping-practice-py.firebaseio.com', None)

def create():
    url = input('Please enter the URL of the site you would like to get information from: ')
    session = HTMLSession()
    response = session.get(url)
    title = response.html.find('title', first=True).text
    description = response.html.xpath("//meta[@name='description']/@content")
    canonical = response.html.xpath("//link[@rel='canonical']/@href")
    author = response.html.xpath("//meta[@name='author']/@content")
    image = response.html.xpath("//meta[@property='og:image']/@content")
    collectName=input("Please enter the name of the collection you would like to create. \n")
    db.collection(collectName).document(title).set(
        {'Title': title,
         'Author': author,
         'Description': description,
         'Image': image,
         'Canonical link': canonical
         }
    )

def read():
    collect=input("Please enter the name of the collection you would like to read.\n")
    docs=input("Please enter the name of the document you would like to read.\n")
    doc = db.collection(collect).document(docs).get()
    print(doc.to_dict())

def update():
    collect = input("Please enter the name of the collection you would like to update.\n")
    docs = input("Please enter the name of the document you would like to update.\n")
    attrib=input("Please enter the name of the attribute you would like to update.\n")
    change=input("Please enter what you would like to change the value to. \n")
    db.collection(collect).document(docs).update({attrib:change})

def delete():
    collect=input("Please enter the collection you would like to delete from: \n")
    docs=input("Please enter the document you would like to delete: \n")
    db.collection(collect).document(docs).delete()


def main():
    doCrud = 'Y'
    while doCrud.upper() == 'Y':
        crud = input("Would you like to Create,Read,Update or Delete?\n (c,r,u,d): ")
        if crud.upper() == 'C':
            create()
            doCrud = input('Would you like to create, read, update or delete anything else?\n(y/n): ')
        if crud.upper() == 'R':
            read()
            doCrud = input('Would you like to create, read, update or delete anything else?\n(y/n): ')
        if crud.upper() == 'U':
            update()
            doCrud = input('Would you like to create, read, update or delete anything else?\n(y/n): ')
        if crud.upper() == 'D':
            delete()
            doCrud = input('Would you like to create, read, update or delete anything else?\n(y/n): ')
main()