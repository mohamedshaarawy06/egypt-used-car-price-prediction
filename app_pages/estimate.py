from textwrap import dedent

import pandas as pd
import streamlit as st

from nile_common import (BANNER_IMAGE, TEST_MDAPE, capitalize, clean_name, footer, load_data, load_model,
                         logo_html, model_labels)

df = load_data()
ml_model = load_model()
labels = model_labels()

st.markdown(
    dedent(f"""
    <div class="nv-banner">
        <img class="nv-bg" src="{BANNER_IMAGE}" alt="">
        <div class="nv-content">
            {logo_html()}
            <h1>Estimate your car's price</h1>
            <p>Fill in the car details, then press Estimate.</p>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

st.write("")

with st.container(border=True):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        brand = st.selectbox("Brand", sorted(df["brand"].unique(), key=clean_name), format_func=clean_name)
        cars = df[df["brand"] == brand]

        model = st.selectbox("Model", sorted(cars["model"].unique(), key=labels.get), format_func=labels.get)
        cars = cars[cars["model"] == model]

        model_freq = len(cars)
        bm_first_year = cars["year"].min()

        year = st.selectbox("Year", sorted(cars["year"].unique(), reverse=True))
        cars = cars[cars["year"] == year]

        fuel = st.selectbox("Fuel", sorted(cars["fuel"].unique()), format_func=capitalize)
        cars = cars[cars["fuel"] == fuel]

    latest_year = df["year"].max()
    max_km = int(min((latest_year - year + 1) * 100_000, df["kilometers"].max()))
    # Start from the typical kilometers of this exact car in the data.
    # 0 km on old cars usually means "not filled in", so only recorded values are used;
    # if none exist, fall back to the typical kilometers of all cars from the same year.
    recorded_km = cars.loc[cars["kilometers"] > 0, "kilometers"]
    if recorded_km.empty:
        recorded_km = df.loc[(df["year"] == year) & (df["kilometers"] > 0), "kilometers"]
    default_km = int(min(round(recorded_km.median(), -3), max_km)) if not recorded_km.empty else 0

    with col2:
        transmission = st.selectbox("Transmission", sorted(cars["transmission"].unique()), format_func=capitalize)
        # Color and Location start from the most common value in the data
        colors = sorted(df["color"].unique())
        color = st.selectbox("Color", colors, index=colors.index(df["color"].mode()[0]))
        kilometers = st.number_input("Kilometers", min_value=0, max_value=max_km, value=default_km,
                                     step=5000, help=f"Maximum for a {year} car: {max_km:,} km")
        govs = sorted(df["gov"].unique())
        gov = st.selectbox("Location", govs, index=govs.index(df["gov"].mode()[0]))

    estimate = st.button("Estimate", type="primary", icon=":material/sell:")

if estimate:
    years_since_first_seen = year - bm_first_year
    new_data = pd.DataFrame(columns=df.columns.drop("price"),
                            data=[[brand, model, color, year, fuel, kilometers, transmission, gov,
                                   model_freq, bm_first_year, years_since_first_seen]])

    price = ml_model.predict(new_data)[0]
    low = round(price * (1 - TEST_MDAPE), -3)
    high = round(price * (1 + TEST_MDAPE), -3)

    st.markdown(
        dedent(f"""
        <div class="nv-result">
            <div class="nv-result-label">Expected price · {labels[model]} {year}</div>
            <div class="nv-result-price">{price:,.0f} EGP</div>
            <div class="nv-result-range">Typical range: {low:,.0f} – {high:,.0f} EGP</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    market = df[(df["model"] == model) & (df["year"] == year)]

    st.markdown(f'<div class="nv-section-title">Market prices · {labels[model]} {year}</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.container(key="nv_market").columns(4)
    if len(market) > 1:
        m1.metric("Average price", f"{market['price'].mean():,.0f} EGP")
        m2.metric("Lowest price", f"{market['price'].min():,.0f} EGP")
        m3.metric("Highest price", f"{market['price'].max():,.0f} EGP")
        m4.metric("Listings", f"{len(market):,}")
    else:
        # Only one listing: average, lowest and highest would all be the same number
        m1.metric("Listed price", f"{market['price'].iloc[0]:,.0f} EGP")
        m2.metric("Listings", "1")

    st.markdown('<div class="nv-section-title">Similar cars in the data</div>', unsafe_allow_html=True)
    similar = market.assign(km_diff=(market["kilometers"] - kilometers).abs()).sort_values("km_diff").head(5)
    similar = similar[["kilometers", "transmission", "fuel", "color", "gov", "price"]].assign(
        transmission=similar["transmission"].map(capitalize), fuel=similar["fuel"].map(capitalize))
    st.dataframe(
        similar,
        hide_index=True,
        width="stretch",
        column_config={
            "kilometers": st.column_config.NumberColumn("Kilometers", format="localized"),
            "transmission": "Transmission",
            "fuel": "Fuel",
            "color": "Color",
            "gov": "Location",
            "price": st.column_config.NumberColumn("Price (EGP)", format="localized"),
        },
    )

footer()
