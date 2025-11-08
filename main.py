from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from scraper import scrape_category
from sheets_manager import authorize_google_sheets, update_product_in_sheet

app = FastAPI()

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
        print(f"Scraping category: {category}")
        category_url = f"https://webscraper.io/test-sites/e-commerce/allinone/{category.lower()}"
        products = scrape_category(category_url, category)
        total_products += len(products)

        # Update Google Sheets
        sheet = client.open(SHEET_NAME).worksheet(category)
        for product in products:
            update_product_in_sheet(sheet, product)

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
    # Here you would fetch the products from Google Sheets (to be implemented)
    return {"category": category, "products": []}

@app.get("/price-changes")
async def get_price_changes():
    # Here you would fetch recent price changes (to be implemented)
    return {"date": "2025-10-31", "total_changes": 3, "changes": []}
