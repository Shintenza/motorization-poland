import pandas as pd

def get_oil_barrel_module(data, st, go):

    st.subheader('Cena baryłki ropy w złotówkach')
    # Wczytanie danych z plików CSV
    df_oil = data[0] 
    df_usd_pln = data[1] 

    # Konwersja formatu daty
    df_oil['Data'] = pd.to_datetime(df_oil['Data'], format='%d.%m.%Y')
    df_usd_pln['Data'] = pd.to_datetime(df_usd_pln['Data'], format='%d.%m.%Y')

    # Wybór danych z zakresu dat 2009-07-13 do 2023-06-07
    start_date = pd.to_datetime('2009-07-13')
    end_date = pd.to_datetime('2023-06-07')
    df_oil_filtered = df_oil[(df_oil['Data'] >= start_date) & (df_oil['Data'] <= end_date)]
    df_usd_pln_filtered = df_usd_pln[(df_usd_pln['Data'] >= start_date) & (df_usd_pln['Data'] <= end_date)]

    # Przeliczenie separatora dziesiętnego w kolumnie 'Ostatnio' na kropkę i konwersja na float
    df_usd_pln_filtered['Ostatnio'] = df_usd_pln_filtered['Ostatnio'].str.replace(',', '.').astype(float)

    # Obliczenie średniej arytmetycznej dla każdego rekordu
    df_oil_filtered['MIN'] = df_oil_filtered['Min.'].str.replace(',', '.').astype(float)
    df_oil_filtered['MAX'] = df_oil_filtered['Max.'].str.replace(',', '.').astype(float)
    df_oil_filtered['Srednia'] = (df_oil_filtered['MIN'] + df_oil_filtered['MAX']) / 2

    # Przeliczenie ceny ropy z USD na PLN
    df_oil_filtered['Srednia_PLN'] = df_oil_filtered['Srednia'] * df_usd_pln_filtered['Ostatnio']

    # Tworzenie wykresu
    fig = go.Figure()

    # Dodawanie danych do wykresu
    fig.add_trace(go.Scatter(x=df_oil_filtered['Data'], y=df_oil_filtered['Srednia_PLN'], name='Cena ropy (PLN)'))

    # Konfiguracja wyglądu wykresu
    fig.update_layout(
        xaxis=dict(
            title='Data',
            tickformat='%Y-%m-%d',
            rangeslider=dict(visible=True),
            type='date'
        ),
        yaxis=dict(title='Cena ropy (PLN)'),
        title='Wykres ceny baryłki ropy w złotówkach',
        hovermode='x'
    )

    # Wyświetlanie wykresu w Streamlit
    st.plotly_chart(fig)
