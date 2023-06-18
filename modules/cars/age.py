import geopandas
import pandas as pd
def get_age_module(df, st, plt):
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    df["Age"] = df["Year"] - df["ProductionYear"]
    mean_age = df[(df["Source"] == "UŻYW. IMPORT INDYW") | (df["Source"] == 'UŻYW. ZAKUPIONY W KRAJU')]
    mean_age = mean_age.groupby(["Year", "Region"])["Age"].mean().round().reset_index()
    mean_age_by_years = mean_age.groupby("Year")["Age"].mean().round().reset_index()

    region_shape_df = geopandas.read_file("./data/wojewodztwa.shp", encoding="utf-8")
    region_shape_df["JPT_NAZWA_"] = region_shape_df["JPT_NAZWA_"].str.upper()
    region_shape_df.rename(columns={"JPT_NAZWA_": "Region"}, inplace=True)
    region_shape_df = region_shape_df[["Region", "geometry"]]

    region_shape_df = pd.merge(region_shape_df, mean_age, on="Region")

    fig, ax = plt.subplots()

    year = st.slider('Rok', 2010, 2022, 2017) 
    st.subheader(f"Średnia wieku rejestrowanych pojazdów dla danych województw w roku {year}")
    region_shape_df_year = region_shape_df[region_shape_df["Year"] == year]
    region_shape_df_year.plot(column="Age", ax=ax, cmap="summer", edgecolor='white')

    for i, row in region_shape_df_year.iterrows():
        ax.annotate(
            text=f'{row["Region"]}\n{int(row["Age"])}',
            xy=row["geometry"].centroid.coords[0],
            ha="center",
        )

    ax.set_axis_off()
    st.pyplot(fig)
    print(df[(df["Region"] == "PODKARPACKIE") & df["Year"] == 2021])
