# 🧠 Test Technique R&D — Suivi Automatique des Prix E-commerce

Ce projet est une **application Python complète** permettant de **scraper automatiquement des produits e-commerce**, **suivre les changements de prix** et **mettre à jour un Google Sheet** via l’**API Google Sheets**, tout en exposant les données à travers une **API REST (FastAPI)**.

---

## 🚀 Fonctionnalités principales

✅ Scraping automatique de plusieurs catégories de produits
✅ Export structuré des données vers Google Sheets
✅ Détection et suivi des changements de prix
✅ API REST complète (FastAPI)
✅ Architecture modulaire et commentée
✅ Scheduler automatique (optionnel)
✅ Alertes e-mail sur changements de prix (optionnel)

---

## 🧱 Structure du projet

```
projet/
├── main.py              # Application FastAPI (API REST)
├── scraper.py           # Logique de scraping avec Selenium
├── sheets_manager.py    # Gestion des interactions avec Google Sheets
├── models.py            # Modèles Pydantic pour la validation des données
├── config.py            # Configuration et variables d’environnement
├── credentials.json     # Identifiants du compte de service Google 
├── requirements.txt     # Dépendances Python
├── .env                 # Variables d’environnement
└── README.md            # Documentation complète
```

---

## ⚙️ Installation et Préparation

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/<ton-nom-utilisateur>/price-tracker.git
cd price-tracker
```

### 2️⃣ Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration de l’API Google Sheets

### Étape 1 : Activer l’API Google Sheets

1. Rendez-vous sur [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un **nouveau projet**.
3. Activez les APIs :

   * **Google Sheets API**
   * **Google Drive API**
4. Créez un **compte de service** (IAM & Admin → Comptes de service).
5. Téléchargez le fichier `credentials.json` et placez-le à la racine du projet.

---

### Étape 2 : Créer et partager le Google Sheet

1. Créez une nouvelle feuille Google Sheets nommée **`Product Price Tracker`**.
2. Partagez-la avec l’adresse e-mail du **compte de service** (ex: `bot@project-id.iam.gserviceaccount.com`).
3. Copiez l’**ID de la feuille** (dans l’URL) :

   ```
   https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit
   ```

---

### Étape 3 : Créer le fichier `.env`

```bash
SPREADSHEET_ID=ton_spreadsheet_id
HEADLESS_MODE=True
```

---

## 🧠 Utilisation

### 🕵️ 1. Tester le scraper seul

Pour tester uniquement le scraping sans lancer l’API :

```bash
python scraper.py
```

---

### 🧩 2. Lancer l’API FastAPI

```bash
uvicorn main:app --reload --port 8000
```

L’API sera disponible à :
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔗 Endpoints REST

### 📤 POST `/scrape/now`

Déclenche immédiatement le scraping et met à jour Google Sheets.

```bash
curl -X POST "http://127.0.0.1:8000/scrape/now" \
     -H "Content-Type: application/json" \
     -d '{"categories": ["Laptops", "Tablets", "Touch"], "update_sheets": true}'
```

**Réponse :**

```json
{
  "status": "success",
  "timestamp": "2025-10-31T14:30:00",
  "categories_scraped": ["Laptops", "Tablets", "Touch"],
  "total_products": 45,
  "price_changes_detected": 3
}
```

---

### 📄 GET `/products/{category}`

Récupère les produits d’une catégorie spécifique.

```bash
curl http://127.0.0.1:8000/products/Laptops
```

**Exemple de réponse :**

```json
{
  "category": "Laptops",
  "products": [
    {
      "nom": "Asus VivoBook",
      "prix": 295.99,
      "prix_precedent": 300.00,
      "variation": -1.34,
      "description": "Ordinateur portable léger et performant",
      "rating": 4,
      "reviews": 10,
      "derniere_maj": "2025-10-31 14:30"
    }
  ]
}
```

---

### 📉 GET `/price-changes`

Retourne les derniers changements de prix détectés.

```bash
curl http://127.0.0.1:8000/price-changes
```

**Exemple :**

```json
{
  "date": "2025-10-31",
  "total_changes": 3,
  "changes": [
    {
      "product": "Asus VivoBook",
      "category": "Laptops",
      "old_price": 300.00,
      "new_price": 295.99,
      "variation_percent": -1.34
    }
  ]
}
```

---

## 🕰 Automatisation quotidienne (optionnel)

Pour exécuter le scraping automatiquement chaque jour à **9h00**, activez le **scheduler APScheduler** :

```python
# main.py
from apscheduler.schedulers.background import BackgroundScheduler

def tache_scraping_quotidienne():
    print("Lancement du scraping quotidien...")
    # Appel à la fonction scrape_now()

scheduler = BackgroundScheduler()
scheduler.add_job(tache_scraping_quotidienne, 'cron', hour=9, minute=0)
scheduler.start()
```

---

## ✉️ Alertes e-mail (optionnel)

Envoyez un e-mail lorsqu’un changement de prix est détecté :

```python
import smtplib
from email.mime.text import MIMEText

def envoyer_alerte_email(produit, ancien_prix, nouveau_prix):
    msg = MIMEText(f"Changement de prix pour {produit} :\nAncien prix : {ancien_prix}\nNouveau prix : {nouveau_prix}")
    msg['Subject'] = f"Alerte prix : {produit}"
    msg['From'] = "ton.email@example.com"
    msg['To'] = "destinataire@example.com"

    with smtplib.SMTP('smtp.gmail.com', 587) as serveur:
        serveur.starttls()
        serveur.login("ton.email@example.com", "motdepasse")
        serveur.send_message(msg)
```

---



## 🧰 Améliorations possibles

* 🔹 Sauvegarde locale dans une base SQLite ou Firestore
* 🔹 Historique de prix et graphiques d’évolution
* 🔹 Interface web pour visualiser les données
* 🔹 Authentification JWT pour sécuriser l’API
* 🔹 Dockerisation du projet
* 🔹 Tests unitaires avec `pytest`

---


---

## 👨‍💻 Exemple d’exécution

```bash
uvicorn main:app --reload
```

✅ Le scraping s’exécute
✅ Les données sont envoyées sur Google Sheets
✅ Les endpoints FastAPI renvoient les résultats au format JSON

---

