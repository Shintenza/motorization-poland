def get_accidents_module(data, st, plt):
    st.subheader('Przyczyny wypadków samochodowych w Polsce w latach 2014-2021')
    accidents_df = data[0]
    accidents_df["Ważniejsze przyczyny wypadków"] = accidents_df[
        "Ważniejsze przyczyny wypadków"
    ].str.replace("wina kierujących pojazdami - ", "")

    df_grouped = accidents_df.groupby("Ważniejsze przyczyny wypadków")["Wartosc"].sum()

    fig, ax = plt.subplots(figsize=(10, 6))

    num_colors = len(df_grouped)
    colors = plt.cm.Set3(range(num_colors))
    bars = ax.bar(df_grouped.index, df_grouped.values, color=colors)

    ax.set_ylabel("Liczba wypadków")

    ax.set_xticklabels([])
    ax.legend(
        bars,
        df_grouped.index,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=3,
        title="Przyczyny",
        facecolor="white",
        edgecolor="black",
    )

    plt.subplots_adjust(bottom=0.3)
    st.pyplot(fig, dpi=300)

    fig, ax = plt.subplots()
    st.subheader('Liczba śmierci na drogach na 100 tys. mieszkańców w Polsce w latach 2000-2021')
    df = data[1] 

    df_pl = df[df['geo'] == 'PL']
    ax.plot(df_pl['TIME_PERIOD'], df_pl['OBS_VALUE'], label='Polska')
    ax.set_xlabel('Lata')
    ax.set_ylabel('Śmierci / 100 tys. mieszkańców')
    st.pyplot(fig)
