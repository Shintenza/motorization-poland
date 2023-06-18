import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.accidents.deaths_eu import get_deaths_eu_module                     # pyright:ignore

st.title('Analiza danych związanych z wypadkami')

@st.cache_data
def load_data():
    deaths = pd.read_csv("./data/deaths-europe.csv")
    return deaths

data_load_state = st.text("Loading data...")
loaded_data = load_data()
data_load_state.text("Done! (using st.cache_data)")

get_deaths_eu_module(loaded_data, st, plt)
