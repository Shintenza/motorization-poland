import numpy as np


def get_fuel_module(df, st, plt):
    years = list(range(df["Year"].min(), df["Year"].max() + 1))
    on_e = (
        df[
            (df["FuelType"] == "BENZYNA")
            | (df["FuelType"] == "ENERGIA ELEKTRYCZNA")
            | (df["FuelType"] == "OLEJ NAPĘDOWY")
        ]
        .groupby(["Year", "FuelType"])
        .size()
        .reset_index(name="Count")
    )

    st.subheader(
        f"Liczba rejestrowanych pojazdów na benzynę i  olej napędowy w latach {years[0]}-{years[-1]}"
    )

    fig, ax = plt.subplots()
    ax.plot(
        years,
        on_e[on_e["FuelType"] == "BENZYNA"]["Count"],
        label="Benzyna",
    )
    ax.plot(
        years,
        on_e[on_e["FuelType"] == "OLEJ NAPĘDOWY"]["Count"],
        label="Olej napędowy",
    )
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    st.subheader(f"Liczba rejestrowanych pojazdów elektrycznych w latach {years[0]}-{years[-1]}")

    fig, ax = plt.subplots()
    ax.plot(
        years,
        on_e[on_e["FuelType"] == "ENERGIA ELEKTRYCZNA"]["Count"],
        color="olivedrab"
    )
    ax.grid(True)
    st.pyplot(fig)
