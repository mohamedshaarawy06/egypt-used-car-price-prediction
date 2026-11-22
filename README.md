# 🚗 Used Car Price Prediction — Egypt

Predicting the asking price of used cars in the Egyptian market with a tuned **CatBoost** regression pipeline, served through an interactive **Streamlit** web app.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?logo=scikitlearn&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-1.2-FFCC00)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://nilevalue.streamlit.app)

🔗 **Live app:** [nilevalue.streamlit.app](https://nilevalue.streamlit.app)

---

## 📌 Overview

The used-car market in Egypt has very wide price ranges (from ~13K to 10M EGP), and prices depend on many factors: brand, model, year, mileage, transmission, location and more.
This project builds an end-to-end machine learning workflow to estimate a fair price for a car:

1. **Data cleaning** of ~17K raw listings
2. **Exploratory data analysis** (EDA) with interactive Plotly charts
3. **Feature engineering**
4. **Model comparison** (XGBoost vs LightGBM vs CatBoost)
5. **Hyperparameter tuning** (RandomizedSearchCV + Optuna)
6. **Deployment** as a Streamlit app

---

## 📊 Results

Final model: **CatBoost** inside a scikit-learn `Pipeline`, trained on `log(price)` with `TransformedTargetRegressor`.

| Metric (held-out test set) | Score |
|---|---|
| R² (log price) | **94.58%** |
| R² (EGP) | 81.84% |
| MAE | 69,425 EGP |
| Median Absolute % Error | **11.42%** |

> R² in EGP is lower because a few rare luxury cars are hard to price; the typical error is about 11%.

**Most important features:** model, year, transmission, brand.

---

## 🗂️ Dataset

`used_cars_in_egypt.csv` — 17,159 used-car listings from the Egyptian market.

| Column | Description |
|---|---|
| Brand | Car manufacturer (94 brands) |
| Model | Car model within the brand (828 models) |
| Color | Exterior color |
| Year | Manufacturing year (1951 – 2023) |
| Fuel | gas, diesel, natural gas, Electric, Hybrid |
| Kilometers | Distance driven (text, e.g. `"130,000 Km"`) |
| Trasmission | automatic / manual / CVT *(misspelled in source)* |
| Price | Asking price in EGP — **target** |
| Gov | Listing location (governorate / city / district) |

After cleaning, **16,817** rows remain and are saved in `car_usage_clean.csv`.

---

## 🔧 Methodology

### Data Cleaning
- Fixed column names (`Trasmission` → `transmission`, lowercase)
- Dropped missing years and duplicate rows
- Converted `price` and `kilometers` from text to numbers
- Normalized whitespace in brand/model names; model = `brand + model`
- Removed unrealistic prices (< 10K or ≥ 100M EGP) and mileage (≥ 1M km or > 100K km per year)

### Feature Engineering
| Feature | Meaning |
|---|---|
| `model_freq` | How common the model is in the market |
| `bm_first_year` | First year the model appears in the data |
| `years_since_first_seen` | `year - bm_first_year` (generation proxy) |

### Preprocessing (`ColumnTransformer`)
| Encoder | Columns |
|---|---|
| One-Hot Encoding | `fuel`, `transmission` |
| Binary Encoding | `color` |
| Target Encoding (5-fold) | `brand`, `model`, `gov` |
| Passthrough | numeric features |

### Modeling
- 5-fold cross-validation comparison of XGBoost, LightGBM and CatBoost (raw and log target)
- CatBoost won and was tuned with **RandomizedSearchCV** and **Optuna**
- Best params: `depth=7`, `learning_rate≈0.055`, `iterations=1571`, `l2_leaf_reg≈6.53`, `random_strength≈9.46`

---

## 📁 Project Structure

```
.
├── car_usage_prediction.ipynb   # Full workflow: cleaning, EDA, modeling, evaluation
├── car_app.py                   # Streamlit web app (NileValue) – entry point & navigation
├── nile_common.py               # Shared style, data/model loading
├── app_pages/
│   ├── home.py                  # Home page
│   └── estimate.py              # Price estimate page
├── static/                      # Car photos used on the site
├── .streamlit/config.toml       # Site theme colors
├── final_model.pkl              # Trained pipeline (preprocessing + CatBoost)
├── used_cars_in_egypt.csv       # Raw dataset
├── car_usage_clean.csv          # Cleaned dataset (used by the app)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/mohamedshaarawy06/egypt-used-car-price-prediction.git
cd egypt-used-car-price-prediction
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

> ⚠️ Keep the pinned versions — `final_model.pkl` was saved with these library versions and may not load with others.

### 3. Run the app
```bash
streamlit run car_app.py
```
Then open `http://localhost:8501` in your browser.

### 4. Explore the notebook
```bash
jupyter notebook car_usage_prediction.ipynb
```

---

## 🖥️ The App

**NileValue** ([nilevalue.streamlit.app](https://nilevalue.streamlit.app)) is a two-page site:

- **Home** – overview of the data and how it works
- **Estimate Price** – choose **Brand → Model → Year → Fuel** (only combinations that exist in the data are shown), set transmission, color, kilometers and location, then press **Estimate** to get:
  - the expected price in EGP with a typical range (± the model's test MdAPE, ~11%)
  - real market prices (average / lowest / highest) for the same model and year
  - the most similar cars in the data

Photos are from [Unsplash](https://unsplash.com).

---

## 🛠️ Tech Stack

`Python` · `pandas` · `NumPy` · `scikit-learn` · `CatBoost` · `XGBoost` · `LightGBM` · `category_encoders` · `Optuna` · `Plotly` · `Streamlit` · `joblib`
