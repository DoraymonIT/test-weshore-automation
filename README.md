# 🧠 Test Technique R&D — Suivi Automatique des Prix E-commerce

Ce projet est une **application Python complète** permettant de **scraper automatiquement des produits e-commerce**, **suivre les changements de prix** et **mettre à jour un Google Sheet** via l’**API Google Sheets**, tout en exposant les données à travers une **API REST (FastAPI)**.

---

## 🚀 Fonctionnalités principales

✅ Scraping automatique de plusieurs catégories de produits
✅ Export structuré des données vers Google Sheets
✅ API REST complète (FastAPI)
✅ Scheduler automatique  (Pas tester de mon cote )
✅ Alertes e-mail sur changements de prix (Pas tester de mon cote )

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
└── tests.md            # Documentation complète
└──└── test.api.py            #  Le test des APIs
└──└── scraper.py            # Tester la Logique de scraping avec Selenium
└──└──  sheets_manager.py    # tester la Gestion des interactions avec Google Sheets
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
2. Créez un **nouveau projet** : Test WeShore Automation.
3. Activez les APIs :

   * **Google Sheets API**
   * **Google Drive API**
4. Créez un **compte de service** (IAM & Admin → Comptes de service)." scrapy-data@test-weshore-automation.iam.gserviceaccount.com
5. Téléchargez le fichier `credentials.json` et placez-le à la working Folder du projet.

---

### Étape 2 : Créer et partager le Google Sheet

1. Créez une nouvelle feuille Google Sheets nommée **`Product Price Tracker`**.
2. Partagez-la avec l’adresse e-mail du **compte de service** (ex: `scrapy-data@test-weshore-automation.iam.gserviceaccount.com`).
3. Copiez l’**1_7YOn6iLkYl87zfWGYIUHEI6evo15wl7FEDbd5NiD5k** (dans l’URL) :

   ```
   https://docs.google.com/spreadsheets/d/1_7YOn6iLkYl87zfWGYIUHEI6evo15wl7FEDbd5NiD5k/edit
   ```

---

### Étape 3 : Créer le fichier `.env`

```bash
SPREADSHEET_ID=1_7YOn6iLkYl87zfWGYIUHEI6evo15wl7FEDbd5NiD5k
HEADLESS_MODE=True
...
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

👉 Pour le Swagger :  [http://127.0.0.1:8000/docs#/default](http://127.0.0.1:8000/docs#/default)

---

## 🔗 Endpoints REST

### 📤 POST `/scrape/now`

Déclenche immédiatement le scraping et met à jour Google Sheets.

```bash
curl -X POST "http://127.0.0.1:8000/scrape/now" 

     Request Body '{"categories": ["Laptops", "Tablets", "Touch"], "update_sheets": true}'
```


---

### 📄 GET `/products/{category}`

Récupère les produits d’une catégorie spécifique.

```bash
curl http://127.0.0.1:8000/products/Laptops
Parameter : Laptops
```
```

---

### 📉 GET `/price-changes`
- NB : J'ai mis la logic mais n'est pas encore tester , j'ai besoin de temps pour debugger .
Retourne les derniers changements de prix détectés.

```bash
curl http://127.0.0.1:8000/price-changes
```


```

---

## 🕰 Automatisation quotidienne 

Pour exécuter le scraping automatiquement chaque jour à **9h00**, J'active le **scheduler APScheduler** avec le script below:

```python
# main.py
from apscheduler.schedulers.background import BackgroundScheduler

def tache_scraping_quotidienne():
    print("Lancement du scraping quotidien...")
    <!-- Appel A la fonction main qui se base ici : @app.post("/scrape/now")  -->
    scrape_now()

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
    # // J'ai besoin de configuer un email avec accces : SnedOnBehalf
    msg['From'] = 
    msg['To'] = "bendrimou@gmail.com"

    with smtplib.SMTP('smtp.gmail.com', 587) as serveur:
        serveur.starttls()
        serveur.login("bendrimou@gmail.com", "itsASecret")
        serveur.send_message(msg)
```

---



## 🧰 Améliorations possibles


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

