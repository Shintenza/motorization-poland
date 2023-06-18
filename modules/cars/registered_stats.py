def get_registered_stats_module(df, st, plt):
    years = list(range(df["Year"].min(), df["Year"].max() + 1))
    number_of_registered_cars = df.value_counts("Year").reset_index(name="Count")
    number_of_registered_cars = number_of_registered_cars.sort_values("Year")

    st.subheader("Liczba rejestrowanych pojazdów na przestrzeni lat 2010-2022")

    fig, ax = plt.subplots()
    ax.plot(years, number_of_registered_cars["Count"])
    ax.plot(years, number_of_registered_cars["Count"], "o")
    ax.get_yaxis().set_visible(False)
    for i, value in enumerate(number_of_registered_cars["Count"]):
        ax.text(
            years[i], value + 20000, f"{value}", ha="center", va="bottom", fontsize="4"
        )

    fig.set_size_inches(6, 3)
    st.pyplot(fig)

    used_cars = (
        df[
            (df["Source"] == "UŻYW. IMPORT INDYW")
            | (df["Source"] == "UŻYW. ZAKUPIONY W KRAJU")
        ]
        .groupby("Year")
        .size()
        .reset_index(name="Count")
    )
    new_cars = (
        df[
            (df["Source"] == "NOWY IMPORT INDYW")
            | (df["Source"] == "NOWY ZAKUPIONY W KRAJU")
        ]
        .groupby("Year")
        .size()
        .reset_index(name="Count")
    )

    st.subheader("Liczba zarejestrowanych nowych i używanych pojazdów w latach 2010-2022")

    fig, ax = plt.subplots()
    ax.plot(years, used_cars["Count"], color="salmon", label="Pojazdy używane")
    ax.fill_between(years, used_cars["Count"], color="salmon", alpha=0.2)
    ax.plot(years, new_cars["Count"], color="teal", label="Pojazdy nowe")
    ax.fill_between(years, new_cars["Count"], color="aqua", alpha=0.2)
    ax.ticklabel_format(style="plain")
    ax.legend()

    st.pyplot(fig)
