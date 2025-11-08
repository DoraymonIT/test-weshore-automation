from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_scrape_invalid_category():
    response = client.post("/scrape/now", json={"categories":["Invalid"], "update_sheets": False})
    assert response.status_code == 400

def test_scrape_laptops():
    response = client.post("/scrape/now", json={"categories":["Laptops"], "update_sheets": False})
    assert response.status_code == 200
    assert "categories_scraped" in response.json()
