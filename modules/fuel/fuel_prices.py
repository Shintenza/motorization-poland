import pandas as pd

def get_fuel_prices_module(df, st, go):

    st.subheader('Ceny paliw')
    # Sprawdzenie istnienia kolumny "Data"
    if 'Data' not in df.columns:
        raise KeyError("Kolumna 'Data' nie istnieje w pliku CSV.")

    # Konwersja kolumny "Data" na typ datetime
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

    # Usunięcie wierszy, w których nie udało się sparsować daty
    df.dropna(subset=['Data'], inplace=True)

    # Ustawienie kolumny "Data" jako indeks
    df.set_index('Data', inplace=True)

    # Wybór paliw do wyświetlenia na wykresie
    show_e95 = st.checkbox('Cena E95', value=True)
    show_on = st.checkbox('Cena ON', value=True)

    # Filtruj dane na podstawie wybranych paliw
    filtered_df = df[['Cena E95', 'Cena ON']]

    # Tworzenie wykresu
    fig = go.Figure()

    # Dodawanie linii dla wybranych paliw
    if show_e95:
        fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['Cena E95'], name='Cena E95', line=dict(color='green')))

    if show_on:
        fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['Cena ON'], name='Cena ON', line=dict(color='black')))

    # Konfiguracja wyglądu wykresu
    fig.update_layout(
        xaxis=dict(
            title='Data',
            tickformat='%Y-%m-%d',
            rangeslider=dict(visible=True),
            type='date'
        ),
        yaxis=dict(title='Cena (PLN)'),
        title='Wykres cen paliw',
        hovermode='x',
        width=800,
        height=600
    )

    # Wyświetlanie wykresu w Streamlit
    st.plotly_chart(fig)
