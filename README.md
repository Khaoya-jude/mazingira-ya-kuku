# 🐔 Mazingira ya Kuku — Nairobi Poultry Hub
### A Django MVP for Nairobi Egg Farmers

---

## Problem Statement

Egg farmers in Nairobi's peri-urban belt (Dagoretti, Kikuyu, Kiambu corridor) face five
compounding crises:

| # | Problem | Data point |
|---|---------|-----------|
| 1 | **High feed costs** | Feed = 85–90% of production cost; Kenyan farmers pay 42–54% more than peers in South Africa (CAK inquiry 2024) |
| 2 | **Transport & market costs** | Non-tariff barriers, fuel costs, middlemen squeeze margins further |
| 3 | **Disease outbreaks** | Newcastle disease endemic; vaccine cold-chain failures and counterfeit vaccines rampant |
| 4 | **Counterfeit inputs** | 15% of smallholders suspected counterfeit vaccines (KALRO 2024 study); cold-chain failures lead to potency loss |
| 5 | **Information gap** | Extension worker-to-farmer ratio exceeds 1:1000 across Kenya; no digital advisory for poultry |

---

## Solution: Five Feature Modules

### 1. 🌽 FeedWatch
- **Crowdsourced feed price board** — farmers submit prices observed at any agrovet
- **Price trend charts** by county and feed type (layers mash, chick mash, etc.)
- **Bulk-buy group organiser** — coordinate 10–20 farmers to buy together, saving 10–20%
- Simple upvoting to verify recent/accurate submissions

### 2. 🥚 EggMarket
- **Farmer egg listings** — post grade, quantity, price, availability
- **Direct buyer matching** — hotels, restaurants, schools, retailers browse and send inquiries
- **Market price index** — crowdsourced and admin-curated daily egg prices by Nairobi area
- Removes 1–2 layers of middlemen, improving farm-gate prices by 15–30%

### 3. 🛡️ FarmGuard
- **Disease outbreak map** — geo-tagged reports from farmers, visible to all
- **SMS alerts** — automatically broadcast to farmers within same sub-location when outbreak confirmed
- **Symptom checker** — select symptoms, get likely diagnosis + vet referral
- **Vaccination record log** — track what was given, to how many birds, what's due next
- **QR-verified vaccine authenticity** (via TrustShop integration)

### 4. ✅ TrustShop
- **Verified supplier directory** — KEBS-registered, DVS-approved suppliers only
- **QR code scanning** — scan any vaccine/feed bag to verify authenticity against database
- **Community reviews** — farmers rate and review after purchase
- Combats counterfeit vaccines and substandard feed

### 5. 📚 AgriLearn
- **Extension articles** in English + Kiswahili
- **SMS-ready tips** — 160-character versions of every article for offline farmers
- **Vet directory** — licensed vets available for farm visits
- **Ask an Expert Q&A** — post a question, get a vet response within 48h

### Bonus: 📊 Farm Dashboard
- Weekly production logging (eggs produced/sold, revenue, feed cost, mortality)
- Profit/loss tracking with Chart.js visualisation
- Feed cost per egg metric — key productivity indicator

---

## Architecture

```
mazingira_ya_kuku/
├── config/
│   ├── settings.py        # Django settings
│   └── urls.py            # Root URL conf
├── apps/
│   ├── accounts/          # Custom FarmerUser model, dashboard, farm records
│   ├── feed_watch/        # Feed prices, bulk buying
│   ├── egg_market/        # Egg listings, buyer matching
│   ├── farm_guard/        # Disease alerts, symptom checker, vaccination log
│   ├── trust_shop/        # Verified suppliers, QR verification
│   └── agri_learn/        # Articles, vet directory, Ask an Expert
├── templates/             # Django templates (Bootstrap 5)
├── static/                # CSS, JS, images
└── locale/                # i18n: English + Kiswahili
```

---

## Quick Start

```bash
# 1. Clone and enter directory
cd mazingira_ya_kuku

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cat > .env << 'EOF'
SECRET_KEY=your-long-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
AT_USERNAME=sandbox
AT_API_KEY=your_africastalking_key
EOF

# 5. Create __init__.py files for apps
for app in accounts feed_watch egg_market farm_guard trust_shop agri_learn; do
  touch apps/$app/__init__.py
done
touch config/__init__.py

# 6. Run migrations
python manage.py makemigrations accounts feed_watch egg_market farm_guard trust_shop agri_learn
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Load initial disease data (create this fixture)
python manage.py loaddata initial_diseases

# 9. Run server
python manage.py runserver
```

Then visit:
- **http://127.0.0.1:8000/** — Landing page
- **http://127.0.0.1:8000/admin/** — Admin panel
- **http://127.0.0.1:8000/health/alerts/** — Disease map (public)
- **http://127.0.0.1:8000/feed/prices/** — Feed prices (public)

---

## Key Integrations to Add (Post-MVP)

| Integration | Purpose | Service |
|-------------|---------|---------|
| SMS alerts | Disease broadcast, USSD fallback | Africa's Talking |
| Maps | Disease outbreak map | Leaflet.js + OpenStreetMap |
| Payments | Group buying payment | M-Pesa Daraja API |
| QR codes | Supplier/vaccine verification | `qrcode` library (already in requirements) |
| Push notifications | Disease alerts | Firebase FCM |

---

## Mobile-First Design Principles

1. **Works on 2G** — no heavy JS frameworks; Bootstrap 5 only
2. **SMS fallback** — every feature has an SMS equivalent (ALERT, PRICE, FEED keywords)
3. **Kiswahili support** — django-i18n with `locale/sw/` translations
4. **Low-literacy UX** — large icons, simple forms, minimal text input
5. **Offline disease reference** — static disease card pages cached for offline use

---

## Business Model (Suggested)

| Revenue stream | Mechanism |
|---------------|-----------|
| Verified supplier listings | Agrovet pays KES 2,000/month for "Verified" badge |
| Bulk-buy coordination fee | 1% of group purchase value |
| Premium farmer tier | Farm analytics, priority vet Q&A — KES 300/month |
| NGO/donor funding | Disease surveillance data is valuable to KALRO, FAO |
| SMS subscription | Bulk SMS credits sold to county agricultural offices |

---

## Development Roadmap

**Phase 1 (MVP — 8 weeks):** This codebase
**Phase 2 (3 months):** M-Pesa integration, Leaflet disease map, offline PWA
**Phase 3 (6 months):** AI symptom checker, automated SMS broadcasts, mobile app

---

*Built for: Nairobi peri-urban egg farmers, Dagoretti, Kikuyu, Kiambu corridor*
*Stack: Django 4.2, Bootstrap 5, SQLite → PostgreSQL, Africa's Talking SMS*
