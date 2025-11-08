# models.py
from pydantic import BaseModel
from typing import List, Optional

# Requête POST /scrape/now
class ScrapeRequest(BaseModel):
    categories: List[str]
    update_sheets: bool = True

# Modèle d’un produit
class Product(BaseModel):
    nom: str
    prix: float
    description: str
    rating: float
    reviews: int
    categorie: str
    date_scraping: str
    url: str
    prix_precedent: Optional[float] = None
    variation: Optional[float] = None
