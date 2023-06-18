import streamlit as st
import pandas as pd

def get_orlen_module(df, st, go):

    st.subheader('Ceny akcji spółki PKN Orlen')
    # Przekształcenie formatu daty
    df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

    # Filtrowanie danych w zadanym przedziale czasowym
    start_date = pd.to_datetime('2009-07-13')
    end_date = pd.to_datetime('2023-06-07')
    filtered_df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

    # Konwersja formatu cen akcji na wartości liczbowe
    filtered_df['Max.'] = pd.to_numeric(filtered_df['Max.'].str.replace(',', '.'))
    filtered_df['Min.'] = pd.to_numeric(filtered_df['Min.'].str.replace(',', '.'))

    # Obliczanie ceny średniej
    filtered_df['Średnia'] = (filtered_df['Max.'] + filtered_df['Min.']) / 2

    # Tworzenie wykresu
    fig = go.Figure()

    # Dodawanie danych do wykresu
    fig.add_trace(go.Scatter(x=filtered_df['Data'], y=filtered_df['Średnia'], name='Cena średnia'))

    # Konfiguracja wyglądu wykresu
    fig.update_layout(
        xaxis=dict(
            title='Data',
            tickformat='%Y-%m-%d',
            rangeslider=dict(visible=True),
            type='date'
        ),
        yaxis=dict(title='Cena akcji (PLN)'),
        title='Ceny akcji spółki PKN Orlen',
        hovermode='x'
    )

    # Wyświetlanie wykresu w Streamlit
    st.plotly_chart(fig)
