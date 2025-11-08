from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from scraper import scrape_category
from sheets_manager import authorize_google_sheets, create_category_sheet, update_product_in_sheet
from config import CATEGORIES, SHEET_NAME

app = FastAPI()

class ScrapeRequest(BaseModel):
    categories: List[str]
    update_sheets: bool

@app.post("/scrape/now")
async def scrape_now(request: ScrapeRequest):
    client = authorize_google_sheets()
    categories_scraped = []
    total_products = 0

    for category in request.categories:
        if category not in CATEGORIES:
            raise HTTPException(status_code=400, detail=f"Category '{category}' not recognized")
        category_path = CATEGORIES[category]
        category_url = f"https://webscraper.io/test-sites/e-commerce/allinone/{category_path}"
        products = scrape_category(category_url, category)
        total_products += len(products)

        if request.update_sheets:
            sheet = create_category_sheet(client, category)
            for product in products:
                update_product_in_sheet(sheet, product)
        categories_scraped.append(category)

    return {
        "status": "success",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories_scraped": categories_scraped,
        "total_products": total_products
    }

@app.get("/products/{category}")
async def get_products(category: str):
    client = authorize_google_sheets()
    try:
        sheet = client.open(SHEET_NAME).worksheet(category)
        data = sheet.get_all_records()
        return {"category": category, "products": data}
    except:
        raise HTTPException(status_code=404, detail="Category not found")

@app.get("/price-changes")
async def get_price_changes():
    # Implémentation simple : récupérer toutes les variations >0
    client = authorize_google_sheets()
    sheet = client.open(SHEET_NAME)
    changes = []
    for ws in sheet.worksheets():
        records = ws.get_all_records()
        for r in records:
            if r.get("Variation (%)", 0) != 0:
                changes.append(r)
    return {"total_changes": len(changes), "changes": changes}
