import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.fuel.orlen import get_orlen_module                         # pyright:ignore
from modules.fuel.fuel_prices import get_fuel_prices_module             # pyright:ignore
from modules.fuel.oil_barrel import get_oil_barrel_module               # pyright:ignore


st.title('Analiza danych finansowych')

@st.cache_data
def load_data():
    orlen = pd.read_csv("./data/PKN.csv")
    oil = pd.read_csv("./data/ropa.csv") 
    usd_pln = pd.read_csv("./data/USD_PLN.csv")
    try:
        fuel = pd.read_csv('./data/paliwa.csv')
    except pd.errors.ParserError:
        fuel = pd.read_csv('./data/paliwa.csv', skiprows=725, header=0)
    return orlen, oil, usd_pln, fuel

data_load_state = st.text("Loading data...")
loaded_data = load_data()
data_load_state.text("Done! (using st.cache_data)")

get_fuel_prices_module(loaded_data[3], st, go)
get_orlen_module(loaded_data[0], st, go)
get_oil_barrel_module([loaded_data[1], loaded_data[2]], st, go)
