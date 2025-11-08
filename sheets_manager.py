import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Function to authorize Google Sheets API
def authorize_google_sheets():
    creds = Credentials.from_service_account_file('credentials.json', scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    return client

# Function to create a sheet for each category
def create_category_sheet(client, category_name):
    sheet = client.open(SHEET_NAME)
    try:
        worksheet = sheet.add_worksheet(title=category_name, rows="100", cols="10")
        worksheet.append_row(["Produit", "Prix Actuel", "Prix Précédent", "Variation (%)", "Description", "Rating", "Reviews", "Dernière MAJ"])
    except Exception as e:
        print(f"Error creating sheet: {e}")

# Function to update or add product data to Google Sheets
def update_product_in_sheet(sheet, product):
    # Find if the product already exists (by name)
    cell = sheet.find(product['nom'])
    if cell:
        old_price = float(sheet.cell(cell.row, 2).value)
        new_price = product['prix']
        # Calculate price variation
        variation = ((new_price - old_price) / old_price) * 100
        sheet.update_cell(cell.row, 2, new_price)
        sheet.update_cell(cell.row, 4, variation)
        sheet.update_cell(cell.row, 8, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        # If product does not exist, append it
        sheet.append_row([
            product['nom'], 
            product['prix'], 
            product['prix'],  # First entry, so current and previous price are the same
            0.0,  # No variation on first entry
            product['description'],
            product['rating'],
            product['reviews'],
            product['date_scraping']
        ])
