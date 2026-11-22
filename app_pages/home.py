from textwrap import dedent

import streamlit as st

from nile_common import HERO_IMAGE, TEST_MDAPE, footer, load_data, logo_html

df = load_data()

st.markdown(
    dedent(f"""
    <div class="nv-hero" style="--hero-img: url('{HERO_IMAGE}');">
        {logo_html()}
        <h1>Know your car's real price in Egypt</h1>
        <p>Data-driven price estimates for used cars, built on {len(df):,} real listings from the Egyptian market.</p>
    </div>
    """),
    unsafe_allow_html=True,
)

st.write("")
if st.container(key="nv_cta").button("Estimate my car's price", type="primary", icon=":material/arrow_forward:"):
    st.switch_page("app_pages/estimate.py")

st.markdown('<div class="nv-section-title">NileValue in numbers</div>', unsafe_allow_html=True)

stats = [
    (f"{len(df):,}", "Used car listings analysed"),
    (f"{df['brand'].nunique()} brands", f"{df['model'].nunique()} different models"),
    (f"~{TEST_MDAPE:.0%}", "Typical difference from the real price"),
]
for col, (number, label) in zip(st.columns(3), stats):
    col.markdown(
        f'<div class="nv-card"><div class="nv-stat-number">{number}</div>'
        f'<div class="nv-stat-label">{label}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="nv-section-title">How it works</div>', unsafe_allow_html=True)

steps = [
    ("Choose your car", "Pick the brand, model, year and fuel. Only cars that exist in the market data are shown."),
    ("Add the details", "Enter the transmission, color, kilometers and location of the car."),
    ("Get the price", "See the expected price, a typical price range and real prices of similar cars."),
]
for i, (col, (title, text)) in enumerate(zip(st.columns(3), steps), start=1):
    col.markdown(
        f'<div class="nv-card nv-step"><div class="nv-step-number">{i}</div>'
        f'<div class="nv-step-title">{title}</div>'
        f'<div class="nv-step-text">{text}</div></div>',
        unsafe_allow_html=True,
    )

footer()
