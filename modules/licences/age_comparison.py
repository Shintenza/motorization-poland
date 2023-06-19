def get_age_comparison_module(df, st, plt):
    years = list(range(df["Date"].min(), df["Date"].max() + 1))
    st.subheader(f"Rozkład wydanych uprawnień na grupy wiekowe")
    year = st.selectbox("Rok", years, index=len(years) - 1)

    fig, ax = plt.subplots()
    grouped_by_age = (
        df[df["Date"] == year].groupby("Age")["Value"].sum().reset_index()
    )

    inner_circle = plt.Circle((0, 0), 0.6, color="white")  # pyright: ignore
    ax.pie(
        grouped_by_age["Value"],
        labels=grouped_by_age["Age"],
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    ax.add_artist(inner_circle)

    st.pyplot(fig, dpi=1000)
