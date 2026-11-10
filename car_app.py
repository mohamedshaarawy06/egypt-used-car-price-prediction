import pandas as pd
import streamlit as st
import joblib

st.set_page_config(layout='wide', page_title='Car Price Project')

st.title('Used Car Price Prediction')
st.write('Enter the car details, then press **Predict** to see the expected price in Egypt.')

df = pd.read_csv('car_usage_clean.csv')

ml_model = joblib.load('final_model.pkl')

with st.expander('Show sample of the data'):
    st.dataframe(df.head())

st.sidebar.header('Car Info')

brand = st.sidebar.selectbox('Brand', sorted(df['brand'].unique()))
cars = df[df['brand'] == brand]

model = st.sidebar.selectbox('Model', sorted(cars['model'].unique()))
cars = cars[cars['model'] == model]

model_freq = len(cars)
bm_first_year = cars['year'].min()

year = st.sidebar.selectbox('Year', sorted(cars['year'].unique(), reverse=True))
cars = cars[cars['year'] == year]

fuel = st.sidebar.selectbox('Fuel', sorted(cars['fuel'].unique()))
cars = cars[cars['fuel'] == fuel]

latest_year = df['year'].max()

col1, col2 = st.columns(2)

with col1:
    transmission = st.selectbox('Transmission', sorted(cars['transmission'].unique()))
    color = st.selectbox('Color', sorted(df['color'].unique()))

max_km = int(min((latest_year - year + 1) * 100_000, df['kilometers'].max()))

with col2:
    kilometers = st.number_input('Kilometers', min_value=0, max_value=max_km, value=min(100_000, max_km), step=5000,
                                 help=f'Maximum for a {year} car: {max_km:,} km')
    gov = st.selectbox('Location', sorted(df['gov'].unique()))

years_since_first_seen = year - bm_first_year

if st.button('Predict', type='primary'):
    new_data = pd.DataFrame(columns=df.columns.drop('price'),
                            data=[[brand, model, color, year, fuel, kilometers, transmission, gov,
                                   model_freq, bm_first_year, years_since_first_seen]])

    price = ml_model.predict(new_data)[0]

    st.success(f'Expected price: {price:,.0f} EGP')
