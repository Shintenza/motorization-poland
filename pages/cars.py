import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.cars.brands import get_brands_module                       # pyright:ignore
from modules.cars.sources import get_sources_module                     # pyright:ignore
from modules.cars.registered_stats import get_registered_stats_module   # pyright:ignore
from modules.cars.brand_by_region import get_brand_by_region_module     # pyright:ignore
from modules.cars.fuel import get_fuel_module                           # pyright:ignore
from modules.cars.age import get_age_module                             # pyright:ignore
from modules.cars.age_groups import get_age_groups_module               # pyright:ignore

st.title("Analiza zarejestrowanych pojazdów w CEPiK")

@st.cache_data
def load_data():
    data = pd.read_csv("./data/registered_cars_complete.csv")
    return data

data_load_state = st.text("Loading data...")
df = load_data()
data_load_state.text("Done! (using st.cache_data)")

plt.rcParams.update({'font.size': 5})

get_brands_module(df, st, plt)
get_brand_by_region_module(df, st, plt)
get_sources_module(df, st, plt)
get_registered_stats_module(df, st, plt)
get_fuel_module(df, st, plt)
get_age_groups_module(df, st, plt)
get_age_module(df, st, plt)
