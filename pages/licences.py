import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.licences.sex_comparison import get_sex_comparison_module                       # pyright:ignore
from modules.licences.age_comparison import get_age_comparison_module                       # pyright:ignore

@st.cache_data
def load_data():
    df = pd.read_csv("./data/uprawnienia.csv")
    df_2022 = pd.read_csv("./data/uprawnienia_2022.csv")
    return df, df_2022

st.title("Analiza wydanych uprawnień do kierowania pojazdami") 

data_load_state = st.text("Loading data...")
df, df_2022 = load_data()
data_load_state.text("Done! (using st.cache_data)")

plt.rcParams.update({'font.size': 5})

get_sex_comparison_module(df, st, plt)
get_age_comparison_module(df, st, plt)
