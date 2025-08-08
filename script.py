import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import datetime
import pyodbc
import os

import dotenv
import pandas as pd
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship


#sites para scraping
url_pichau = "https://www.pichau.com.br/computadores/pichau-gamer"
url_terabyte = "https://www.terabyteshop.com.br/pc-gamer"

#conectar com o bd
conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=server_name;"
                      "Database=db_name;"
                      "Trusted_Connection=yes;")


CHROMEDRIVER_PATH = '/path/to/chromedriver'  # Change this if needed
#para abrir o navegador
options = Options()
options.add_argument("--headless=new")  # Run without opening browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
#pegar info da pagina
driver = webdriver.Chrome()
driver.get(url_pichau)
html = driver.page_source

#deixar a info legivel
soup = BeautifulSoup(html, 'html.parser')
#pegar a info relevante do site
nomes_pichau = soup.find_all('h2', class_='MuiTypography-h6')
precos_pichau = soup.find_all('div', class_='mui-144008r-mainWrapper')

#usar soh as infos necessarias
for i in range(len(nomes_pichau)):
    price_text = precos_pichau[i].get_text(strip=True).split('a partir', 1)[0]
    if 'porR$' in price_text:
        price = price_text.split('porR$', 1)[1].strip()
    else:
        price = price_text
    print(f"Computador: {nomes_pichau[i].get_text(strip=True).split(',', 1)[0]} por: {price} no dia: {datetime.date.today()}")
driver.quit()