from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
from config import HEADLESS

def init_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    driver = webdriver.Chrome()
    return driver

def scrape_category(category_url: str, category_name: str):
    driver = init_driver()
    driver.get(category_url)
    time.sleep(2)
    
    produits = []
    try:
        items = driver.find_elements(By.CLASS_NAME, "product-wrapper")
        for item in items:
            try:
                nom = item.find_element(By.CLASS_NAME, "title").text
                prix_txt = item.find_element(By.CLASS_NAME, "price").text
                prix = float(prix_txt.replace("$",""))
                description = item.find_element(By.CLASS_NAME, "description").text
                rating = len(item.find_elements(By.CLASS_NAME, "ws-icon-star"))
                reviews_txt = item.find_element(By.CLASS_NAME,"review-count").text
                reviews = int(reviews_txt.split()[0])
                url_produit = item.find_element(By.CLASS_NAME, "title").get_attribute("href")
                
                produits.append({
                    "nom": nom,
                    "prix": prix,
                    "description": description,
                    "rating": rating,
                    "reviews": reviews,
                    "categorie": category_name,
                    "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "url": url_produit
                })
            except:
                continue
    finally:
        driver.quit()
    return produits
