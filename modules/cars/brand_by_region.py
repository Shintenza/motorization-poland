import pandas as pd
import geopandas

def get_brand_by_region_module(df, st, plt):
    years = list(range(df["Year"].min(), df["Year"].max()+1))

    avaliable_options = ["Ogólnie","Nowe", "Używane"]

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.slider("Wybierz rok", min_value=years[0], max_value=years[len(years)-1], value=years[0])
    with col2:
        selected_type = st.selectbox("Wybierz rodzaj pojazdu:", avaliable_options)

    filters = []
    new = ["NOWY ZAKUPIONY W KRAJU", "NOWY IMPORT INDYW"]
    used = ["UŻYW. IMPORT INDYW", "UŻYW. ZAKUPIONY W KRAJU"]
    if selected_type == "Nowe":
        filters.extend(new)
    elif selected_type == "Używane":
        filters.extend(used)
    else:
        filters.extend(new)
        filters.extend(used)


    region_shape_df = geopandas.read_file("./data/wojewodztwa.shp", encoding="utf-8")
    region_shape_df["JPT_NAZWA_"] = region_shape_df["JPT_NAZWA_"].str.upper()
    region_shape_df.rename(columns={"JPT_NAZWA_": "Region"}, inplace=True)
    region_shape_df = region_shape_df[["Region", "geometry"]]

    grouped_df = df[(df["Year"] == selected_year) & (df["Source"].isin(filters))].groupby(["Region", "Brand", "Model"]).size().reset_index(name="Count")
    grouped_df = grouped_df.groupby("Region").apply(lambda x: x.nlargest(1, "Count")).reset_index(drop=True)

    region_shape_df = pd.merge(region_shape_df, grouped_df, on="Region")
   
    st.subheader(f"Najczęściej rejestrowany pojazd w województwach ({selected_year})")
    fig, ax = plt.subplots()

    region_shape_df.plot(column="Count", ax=ax, cmap="Pastel2", linewidth=2, edgecolor='w')

    for i, row in region_shape_df.iterrows():
        ax.annotate(
            text=f'{row["Brand"]}\n{row["Model"]}',
            xy=row["geometry"].centroid.coords[0],
            ha="center",
        )

    ax.set_axis_off()
    
    st.pyplot(fig)
