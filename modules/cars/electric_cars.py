import numpy as np
from matplotlib.ticker import ScalarFormatter
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from slugify import slugify
import requests
import pandas as pd
import geopandas

def get_electric_cars_module(df, st, plt):
    grouped_df = df[df["FuelType"] == "ENERGIA ELEKTRYCZNA"].groupby(["Region", "Year"]).size().reset_index(name="Count")

    pivoted_df = grouped_df.pivot(index="Region", columns="Year", values="Count").reset_index()
    pivoted_df = pivoted_df.fillna(0)

    heights = pivoted_df.loc[:, 2013:2022].values.transpose()
    heights = np.flipud(heights)

    st.subheader("Liczba zarejestrowanych pojazdów elektrycznych w danych województwach")

    fig = go.Figure()
    years = pivoted_df.columns[-1:0:-1]

    for i in range(len(heights)):
        fig.add_trace(go.Bar(x=pivoted_df["Region"], y=heights[i], name=years[i]))

    fig.update_layout(
        barmode='stack',
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        yaxis_type='log',
        yaxis=dict(tickformat='.0f'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        title=""
    )

    st.plotly_chart(fig)

    st.subheader("Liczba stacji ładowania pojazdów elektrycznych")

    region_shape_df = geopandas.read_file("./data/wojewodztwa.shp", encoding="utf-8")
    region_shape_df = region_shape_df[['JPT_NAZWA_', 'geometry']]
    region_shape_df.rename(columns={'JPT_NAZWA_' : 'region'}, inplace=True)
    region_shape_df['region-slugified'] = region_shape_df['region'].apply(lambda x: slugify(x))

    base_url = 'https://mapaelektromobilnosci.pl/'

    tmp_col = ['region-slugified', 'value']
    tmp_df = pd.DataFrame(columns=tmp_col)

    for region in region_shape_df['region-slugified']:
        url = base_url + region
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        amount_of_stations = soup.find_all("div", class_="total")[1].text
        amount_of_stations = int(amount_of_stations)
        new_row_df = pd.DataFrame([[region, amount_of_stations]], columns=tmp_col)
        
        tmp_df = pd.concat([tmp_df, new_row_df], ignore_index=True)

    region_shape_df = pd.merge(region_shape_df, tmp_df, on='region-slugified')

    region_shape_df = region_shape_df.sort_values('value', ascending=False)
    region_shape_df['region'] = region_shape_df['region'].apply(lambda x: x.upper())

    fig, ax = plt.subplots()
    region_shape_df.plot(column='value', cmap='summer', legend=True, ax=ax)
    ax.set_axis_off()

    for i, row in region_shape_df.iterrows():
        ax.annotate(
            text=f'{row["region"]}\n{int(row["value"])}',
            xy=row["geometry"].centroid.coords[0],
            ha="center",
        )
    st.pyplot(fig, dpi=300)
