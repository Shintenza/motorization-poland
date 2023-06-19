def get_cat_comparison_module(df, st, px):
    st.subheader("Rozkład wydanych uprawnień na kategorie dla 2022 roku")
    grouped_by_types = df.groupby("Type").size().reset_index(name="Count")
    fig = px.pie(grouped_by_types, values="Count", names="Type")
    st.plotly_chart(fig)
