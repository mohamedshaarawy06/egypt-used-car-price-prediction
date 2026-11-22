from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent

# Median absolute % error of the final model on the test set (from the notebook)
TEST_MDAPE = 0.1142

# Car photos (Unsplash) stored in static/ and served by Streamlit (enableStaticServing in .streamlit/config.toml)
HERO_IMAGE = "app/static/hero.jpg"
BANNER_IMAGE = "app/static/banner.jpg"


@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "car_usage_clean.csv")


@st.cache_resource
def load_model():
    return joblib.load(BASE_DIR / "final_model.pkl")


# --- Display-only names: the model always receives the original values ---

def clean_name(name):
    """'Mazda 3 || Mazda 3' -> 'Mazda 3', 'Canghe || Changhe Q7' -> 'Changhe Q7'."""
    return name.replace("Canghe || ", "").split(" || ")[0]


@st.cache_data
def model_labels():
    """Clean label for every model; if two models of a brand would look the same, keep both parts."""
    models = load_data()[["brand", "model"]].drop_duplicates()
    models["label"] = models["model"].map(clean_name)
    clash = models.duplicated(["brand", "label"], keep=False)
    models.loc[clash, "label"] = models.loc[clash, "model"].str.replace(" || ", " / ", regex=False)
    return dict(zip(models["model"], models["label"]))


def capitalize(value):
    """'gas' -> 'Gas', 'natural gas' -> 'Natural gas', 'CVT' stays 'CVT'."""
    return value if value.isupper() else value[0].upper() + value[1:]


CSS = """
<style>
.block-container {padding-top: 2rem; max-width: 1150px;}

.nv-logo {font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px;}
.nv-logo .nile {color: #FFFFFF;}
.nv-logo .value {color: #F59E0B;}

.nv-hero {
    border-radius: 18px;
    padding: 3.2rem 3rem;
    color: #FFFFFF;
    background-color: #0B1F3A;
    background-image:
        linear-gradient(90deg, #0B1F3A 0%, #0B1F3A 32%, rgba(11,31,58,0.55) 52%, rgba(11,31,58,0.05) 100%),
        var(--hero-img);
    background-repeat: no-repeat;
    background-size: cover, 68% auto;
    background-position: center, right center;
    min-height: 330px;
}
.nv-hero h1 {color: #FFFFFF; font-size: 2.6rem; line-height: 1.15; margin: 1.2rem 0 0.8rem 0; max-width: 560px;}
.nv-hero p {color: #DCE4F2; font-size: 1.1rem; max-width: 520px; margin: 0;}

.nv-banner {
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    background-color: #0B1F3A;
    /* Same layout as the home hero: text on navy at the left, the whole car visible at the right */
    background-image:
        linear-gradient(90deg, #0B1F3A 0%, #0B1F3A 40%, rgba(11,31,58,0.5) 58%, rgba(11,31,58,0) 75%),
        var(--banner-img);
    background-repeat: no-repeat;
    background-size: cover, 60% auto;
    background-position: center, right 38%;
}
.nv-banner h1 {color: #FFFFFF; font-size: 2rem; margin: 0.6rem 0 0.3rem 0;}
.nv-banner p {color: #DCE4F2; margin: 0;}

.nv-card {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    height: 100%;
}
.nv-stat-number {font-size: 2rem; font-weight: 800; color: #0B1F3A;}
.nv-stat-label {color: #5B6B82; font-size: 0.95rem;}

.nv-step-number {
    display: inline-block; width: 34px; height: 34px; line-height: 34px;
    border-radius: 50%; background: #FEF3C7; color: #B45309;
    text-align: center; font-weight: 800; margin-bottom: 0.6rem;
}
.nv-step {min-height: 195px;}
.nv-step-title {font-weight: 700; font-size: 1.05rem; color: #0B1F3A;}
.nv-step-text {color: #5B6B82; font-size: 0.95rem;}

.nv-result {
    background: #0B1F3A;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    color: #FFFFFF;
    text-align: center;
}
.nv-result-label {color: #B9C6DA; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;}
.nv-result-price {color: #F59E0B; font-size: 2.8rem; font-weight: 800; margin: 0.3rem 0;}
.nv-result-range {color: #DCE4F2; font-size: 1rem;}

.nv-section-title {font-size: 1.35rem; font-weight: 800; color: #0B1F3A; margin: 2rem 0 0.8rem 0;}
.nv-footer {color: #7A889E; font-size: 0.85rem; text-align: center; margin-top: 3rem;}
.nv-hero [data-testid="stHeaderActionElements"], .nv-banner [data-testid="stHeaderActionElements"] {display: none;}

/* Home call-to-action: bigger, bold and gently pulsing to catch the eye */
.st-key-nv_cta button {
    padding: 0.85rem 1.8rem;
    border-radius: 12px;
    animation: nv-pulse 1.8s ease-in-out infinite;
}
.st-key-nv_cta button p,
.st-key-nv_cta button span {font-size: 1.2rem; font-weight: 800;}
.st-key-nv_cta button:hover {animation-play-state: paused;}
@keyframes nv-pulse {
    0%   {transform: scale(1);    box-shadow: 0 0 0 0 rgba(217,119,6,0.55);}
    50%  {transform: scale(1.06); box-shadow: 0 0 0 14px rgba(217,119,6,0);}
    100% {transform: scale(1);    box-shadow: 0 0 0 0 rgba(217,119,6,0);}
}
/* Respect users who turned off animations in their system settings */
@media (prefers-reduced-motion: reduce) {
    .st-key-nv_cta button {animation: none;}
}

/* Phones and small tablets (kept last so it overrides the rules above) */
@media (max-width: 768px) {
    .nv-hero {
        padding: 2rem 1.5rem;
        min-height: 0;
        background-image: linear-gradient(rgba(11,31,58,0.78), rgba(11,31,58,0.78)), var(--hero-img);
        background-size: cover, cover;
        background-position: center, center;
    }
    .nv-hero h1 {font-size: 2rem;}
    .nv-banner {
        padding: 1.6rem 1.5rem;
        background-image: linear-gradient(rgba(11,31,58,0.78), rgba(11,31,58,0.78)), var(--banner-img);
        background-size: cover, cover;
        background-position: center, center 45%;
    }
    .nv-banner h1 {font-size: 1.6rem;}
    .nv-step {min-height: 215px;}
    .nv-result {padding: 1.4rem 1rem;}
    .nv-result-price {font-size: 2rem;}
    /* Market prices: 2 per row on phones instead of 4 stacked */
    .st-key-nv_market [data-testid="stHorizontalBlock"] {flex-wrap: wrap; gap: 1rem 0.75rem;}
    .st-key-nv_market [data-testid="stColumn"] {flex: 1 1 calc(50% - 0.75rem) !important; min-width: calc(50% - 0.75rem) !important;}
    .st-key-nv_market [data-testid="stMetricValue"] {font-size: 1.35rem;}
}
/* Phones: columns stack, so cards no longer need equal heights */
@media (max-width: 640px) {
    .nv-step {min-height: 0;}
}
</style>
"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)


def logo_html():
    return '<div class="nv-logo"><span class="nile">Nile</span><span class="value">Value</span></div>'


def footer():
    st.markdown(
        f'<div class="nv-footer">NileValue · Estimates are based on {len(load_data()):,} used car listings in Egypt '
        'and are for guidance only</div>',
        unsafe_allow_html=True,
    )
