import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import SHEET_NAME

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
    

def authorize_google_sheets():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def create_category_sheet(client, category_name):
    sheet = client.open(SHEET_NAME)
    try:
        worksheet = sheet.worksheet(category_name)
    except:
        worksheet = sheet.add_worksheet(title=category_name, rows="100", cols="10")
        worksheet.append_row([
            "Produit", "Prix Actuel", "Prix Précédent", "Variation (%)",
            "Description", "Rating", "Reviews", "Dernière MAJ"
        ])
    return worksheet

def update_product_in_sheet(sheet, product):
    try:
        cell = sheet.find(product['nom'])
    except gspread.exceptions.CellNotFound:
        cell = None

    row_data = [
        product['nom'],
        product['prix'],
        product['prix'],
        0.0,
        product['description'],
        product['rating'],
        product['reviews'],
        product['date_scraping']
    ]

    if cell:
        old_price = float(sheet.cell(cell.row, 2).value or 0)
        new_price = product['prix']
        variation = ((new_price - old_price)/old_price*100) if old_price else 0
        row_data[1] = new_price
        row_data[2] = old_price
        row_data[3] = variation
        sheet.update(f"A{cell.row}:H{cell.row}", [row_data])
    else:
        sheet.append_row(row_data)
