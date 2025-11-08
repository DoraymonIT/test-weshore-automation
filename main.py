from http.client import HTTPException
from time import time
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from scrapy import scrape_category
from sheets_manager import authorize_google_sheets, create_category_sheet, update_product_in_sheet
from config import SHEET_NAME, SPREADSHEET_ID

app = FastAPI()

# Map category names to paths
CATEGORIES = {
    "Laptops": "computers/laptops",
    "Tablets": "computers/tablets",
    "Touch": "phones/touch"
}

class ScrapeRequest(BaseModel):
    categories: List[str]
    update_sheets: bool

@app.post("/scrape/now")
async def scrape_now(request: ScrapeRequest):
    client = authorize_google_sheets()
    categories_scraped = []
    price_changes_detected = 0
    total_products = 0

    for category in request.categories:

        category_path = CATEGORIES[category]
        # category_url = f"https://webscraper.io/test-sites/e-commerce/allinone/{category_path}"
        # print(f" URL: {category_url}")
        products = scrape_category(category, category_path)
        # create_category_sheet(client, category)
        
        total_products += len(products)
        # Update Google Sheets
        sheet = client.open(SHEET_NAME)
        create_category_sheet(client, category)

        # time.sleep(2)  # Petite pause pour laisser la worksheet se créer

        for product in products:
            update_product_in_sheet(sheet, product, category)

        categories_scraped.append(category)

    return {
        "status": "success",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "categories_scraped": categories_scraped,
        "total_products": total_products,
        "price_changes_detected": price_changes_detected
    }

@app.get("/products/{category}")
async def get_products(category: str):
    client = authorize_google_sheets()
    sheet = client.open(SHEET_NAME)

    try:
        worksheet = sheet.worksheet(category)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found in Google Sheets")
    
    records = worksheet.get_all_records()  # Récupère tous les produits
    products = []
    for r in records:
        products.append({
            "nom": r["Produit"],
            "prix": r["Prix Actuel"],
            "prix_precedent": r["Prix Précédent"],
            "variation": r["Variation (%)"],
            "description": r["Description"],
            "rating": r["Rating"],
            "reviews": r["Reviews"],
            "dernier_maj": r["Dernière MAJ"]
        })

    return {"category": category, "products": products}


@app.get("/price-changes")
async def get_price_changes():
    client = authorize_google_sheets()
    sheet = client.open(SHEET_NAME)

    total_changes = 0
    changes_list = []

    for category in CATEGORIES.keys():
        try:
            worksheet = sheet.worksheet(category)
        except Exception:
            continue  # Si la feuille n'existe pas, on passe

        records = worksheet.get_all_records()
        for r in records:
            if float(r["Variation (%)"]) != 0:
                total_changes += 1
                changes_list.append({
                    "category": category,
                    "nom": r["Produit"],
                    "prix_precedent": r["Prix Précédent"],
                    "prix_actuel": r["Prix Actuel"],
                    "variation": r["Variation (%)"],
                    "dernier_maj": r["Dernière MAJ"]
                })

    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_changes": total_changes,
        "changes": changes_list
    }

