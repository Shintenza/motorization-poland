import geopandas
import pandas as pd


def get_region_comparison_module(df, st, plt):

    st.subheader("Liczba wydanych uprawnień województwami w roku 2022")

    checkboxes = {}

    categories = df["Type"].unique()
    NUMBER_OF_COLS = 5
    columns = st.columns(NUMBER_OF_COLS)

    selected_by_default = ["B"]
    selected_by_user = []

    for i, category in enumerate(categories):
        if category in selected_by_default: 
            checkboxes[category]  = columns[i%NUMBER_OF_COLS].checkbox(category, value=True)
        else:
            checkboxes[category]  = columns[i%NUMBER_OF_COLS].checkbox(category, value=False)
    

    for category in checkboxes:
        if checkboxes[category]:
            selected_by_user.append(category)

    region_grouped = df[df["Type"].isin(selected_by_user)].groupby("Region").size().reset_index(name="Count")
    region_shape_df = geopandas.read_file("./data/wojewodztwa.shp", encoding="utf-8")
    region_shape_df["JPT_NAZWA_"] = region_shape_df["JPT_NAZWA_"].str.upper()
    region_shape_df.rename(columns={"JPT_NAZWA_": "Region"}, inplace=True)
    region_shape_df = region_shape_df[["Region", "geometry"]]

    region_shape_df = pd.merge(region_shape_df, region_grouped, on="Region")

    fig, ax = plt.subplots()
    region_shape_df.plot(
        column="Count", ax=ax, cmap="Set3", linewidth=2, edgecolor="w"
    )

    for i, row in region_shape_df.iterrows():
        ax.annotate(
            text=f'{row["Region"]}\n{row["Count"]}',
            xy=row["geometry"].centroid.coords[0],
            ha="center",
        )

    ax.set_axis_off()
    st.pyplot(fig, dpi=300)
