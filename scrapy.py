# Import des librairies nécessaires
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

# -----------------------------
# Configuration principale
# -----------------------------

BASE_URL = "https://webscraper.io/test-sites/e-commerce/allinone"

# Catégories à surveiller
CATEGORIES = {
    "Laptops": "computers/laptops",
    "Tablets": "computers/tablets",
    "Touch": "phones/touch"
}

# Mode headless (le navigateur ne s’affiche pas)
HEADLESS = True


# -----------------------------
# Fonction d’initialisation du driver Selenium
# -----------------------------
def init_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless")
        # J'ai ajouter ces deux elements juste poue etre sur que ca marche dans ma machine .
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Création du service
    service = Service(ChromeDriverManager().install())

    # On passe le service ET les options
    driver = webdriver.Chrome()

    return driver


# -----------------------------
# Fonction pour scraper une catégorie donnée
# -----------------------------
def scrape_category(category_name: str, category_path: str):
    """
    Scrape tous les produits d’une catégorie spécifique.

    Paramètres :
        category_name (str) : Nom de la catégorie (ex : 'Laptops')
        category_path (str) : Chemin relatif dans l’URL (ex : 'computers/laptops')

    Retourne :
        Une liste de dictionnaires contenant les infos produits.
    """

    # Initialisation du navigateur
    driver = init_driver()

    # Construction de l’URL complète
    url = f"{BASE_URL}/{category_path}"
    print(f"🕷️ Scraping catégorie : {category_name} → {url}")

    # Ouverture de la page
    driver.get(url)
    time.sleep(2)  # Petite pause pour laisser la page charger

    produits = []

    try:
        # Chaque produit est dans une balise <div class="product-wrapper">
        items = driver.find_elements(By.CLASS_NAME, "product-wrapper")
        print(f"Nombre d’éléments product-wrapper trouvés pour {category_name} : {len(items)}")

        # Parcours de chaque produit
        for item in items:
            try:
                # J'ai utilisé des sélecteurs CSS pour extraire les informations
                # Nom du produit
                nom = item.find_element(By.CSS_SELECTOR, "a.title").text
                # Prix brut (texte)
                prix_txt = item.find_element(By.CSS_SELECTOR, "h4.price span[itemprop='price']").text
                # Prix en float
                prix = float(prix_txt.replace("$", "").strip())
                # Description
                description = item.find_element(By.CSS_SELECTOR, "p.description").text
                # Rating (nombre d’étoiles)
                rating = len(item.find_elements(By.CSS_SELECTOR, ".ws-icon-star"))
                # Nombre de reviews brut (texte)
                reviews_txt = item.find_element(By.CSS_SELECTOR, "span[itemprop='reviewCount']").text
                # Nombre de reviews en entier
                reviews = int(reviews_txt.strip())

                # URL complète du produit
                url_rel = item.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                # url_produit = urljoin("https://webscraper.io/test-sites/e-commerce/allinone", url_rel)
                # Création du dictionnaire pour ce produit
                produit = {
                    "nom": nom,
                    "prix": prix,
                    "description": description,
                    "rating": rating,
                    "reviews": reviews,
                    "categorie": category_name,
                    "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "url": url_rel
                }

                # Ajout à la liste
                produits.append(produit)

            except Exception as e:
                print(f"⚠️ Erreur d’extraction sur un produit ({category_name}) : {e}")

    except Exception as e:
        print(f"❌ Erreur de chargement de la catégorie {category_name} : {e}")

    finally:
        # Toujours fermer le navigateur pour libérer les ressources
        driver.quit()

    print(f"✅ {len(produits)} produits extraits pour la catégorie '{category_name}'")
    return produits


# -----------------------------
# Fonction principale - Scraping multi-catégories
# -----------------------------
def scrape_all_categories():
    """
    Lance le scraping sur toutes les catégories définies dans CATEGORIES.
    Retourne un dictionnaire complet avec toutes les données.
    """

    all_data = {}

    for cat_name, cat_path in CATEGORIES.items():
        # Gestion de retry (jusqu’à 3 essais si erreur)
        for attempt in range(3):
            try:
                produits = scrape_category(cat_name, cat_path)
                all_data[cat_name] = produits
                break  # Si succès, on passe à la catégorie suivante
            except Exception as e:
                print(f"⚠️ Tentative {attempt+1}/3 échouée pour {cat_name} : {e}")
                time.sleep(2)
        else:
            print(f"❌ Impossible de scraper la catégorie {cat_name} après 3 tentatives.")

    print("🎉 Scraping terminé pour toutes les catégories !")
    return all_data


# -----------------------------
# TEST LOCAL
# -----------------------------
# if __name__ == "__main__":
#     # Lancer le scraping complet
#     resultat = scrape_all_categories()

#     # Affichage d’un résumé
#     for cat, produits in resultat.items():
#         print(f"\n📦 Catégorie : {cat} ({len(produits)} produits)")
#         for p in produits[:3]:  # On n’affiche que les 3 premiers
#             print(f" - {p['nom']} → {p['prix']} $")