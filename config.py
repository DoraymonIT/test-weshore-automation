import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Sheets API settings
SHEET_NAME = "Product Price Tracker"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # ID from Google Sheets URL

# Selenium settings
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True") == "True"  # Set headless mode from .env

# API Settings (FastAPI)
API_PORT = 8000
