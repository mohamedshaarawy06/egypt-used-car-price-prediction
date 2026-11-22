import streamlit as st

from nile_common import apply_style

st.set_page_config(page_title="NileValue | Used Car Prices in Egypt", page_icon="🚗", layout="wide")

apply_style()

home = st.Page("app_pages/home.py", title="Home", icon=":material/home:", default=True)
estimate = st.Page("app_pages/estimate.py", title="Estimate Price", icon=":material/sell:")

page = st.navigation([home, estimate], position="top")
page.run()
