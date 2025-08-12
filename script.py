# scraper.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb+srv://iago:PDJnyuuWFhQjm250@cluster0.8gjkuug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["Price-checker"]
collection = db["Pcs"]

# Sites for scraping
url_pichau = "https://www.pichau.com.br/computadores/pichau-gamer"

# Selenium setup
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/115.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.get(url_pichau)
html = driver.page_source
driver.quit()

# Parse HTML
soup = BeautifulSoup(html, 'html.parser')
nomes_pichau = soup.find_all('h2', class_='MuiTypography-h6')
precos_pichau = soup.find_all('div', class_='mui-144008r-mainWrapper')

# Store results in MongoDB
for i in range(len(nomes_pichau)):
    price_text = precos_pichau[i].get_text(strip=True).split('a partir', 1)[0]
    if 'porR$' in price_text:
        price = price_text.split('porR$', 1)[1].strip()
        
    else:
        price = price_text
        
    
    name = nomes_pichau[i].get_text(strip=True).split(',', 1)[0]
    date = datetime.date.today()

    # Insert into MongoDB
    collection.insert_one({
        "name": name,
        "price": float(price.replace('.', '').replace(',', '.')),  # Store as number
        "date": date.isoformat()
    })
    
    print(f"Saved: {name} - {price} - {date}")
response = requests.get(url_pichau)
