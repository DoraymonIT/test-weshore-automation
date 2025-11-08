import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import SHEET_NAME
import gspread
from gspread.exceptions import IncorrectCellLabel
from datetime import datetime
# Function to authorize Google Sheets API
def authorize_google_sheets():
    creds = Credentials.from_service_account_file('credentials.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
    
    # creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

    client = gspread.authorize(creds)
    return client

# Function to create a sheet for each category
def create_category_sheet(client, category_name):
    sheet = client.open(SHEET_NAME)
    try:
        try:
            worksheet = sheet.worksheet(category_name)
            print(f"Worksheet '{category_name}' already exists.")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=category_name, rows="100", cols="10")
            worksheet.append_row([
                "Produit", "Prix Actuel", "Prix Précédent", "Variation (%)",
                "Description", "Rating", "Reviews", "Dernière MAJ"
            ])
            print(f"{worksheet.title} created successfully.")
        return worksheet
    except Exception as e:
        print(f"Error creating sheet: {e}")
        return None

# Function to update or add product data to Google Sheets


def update_product_in_sheet(sheet, product,category):
    """
    Met à jour un produit existant ou l'ajoute à Google Sheets.
    """
    worksheet =  sheet.worksheet(category)
    
    try:
        # Cherche le produit par nom
        print(f"{sheet}")
        cell = worksheet.find(product['nom'])
    except IncorrectCellLabel:
        cell = None

    if cell:
        # Produit existant, mise à jour du prix et de la variation
        old_price = float(worksheet.cell(cell.row, 2).value)
        new_price = product['prix']
        variation = ((new_price - old_price) / old_price) * 100

        worksheet.update_cell(cell.row, 2, new_price)          # Prix actuel
        worksheet.update_cell(cell.row, 4, round(variation, 2)) # Variation (%)
        worksheet.update_cell(cell.row, 8, datetime.now().strftime('%Y-%m-%d %H:%M:%S')) # Dernière MAJ

    else:
        # Nouveau produit, ajout à la fin
        row = [
            product['nom'],                   # Produit
            product['prix'],                  # Prix actuel
            product['prix'],                  # Prix précédent (1ère fois)
            0.0,                              # Variation
            product['description'],           # Description
            product['rating'],                # Rating
            product['reviews'],               # Reviews
            product['date_scraping']          # Date scraping
        ]
        worksheet.append_row(row)

