def get_deaths_eu_module(df, st, plt):
    grouped_data = df.groupby('geo')
    st.subheader("Ilość śmierci na drogach na 100 tys. mieszkańców w UE w latach 2000-2021")

    checkboxes = {}
    countries = list(grouped_data.groups.keys())
    countries.sort()

    num_columns = 5

    fig, ax = plt.subplots()

    columns = st.columns(num_columns)

    selected_by_default = ["PL", "DE", "FR", "HU"]

    for i, country in enumerate(countries):
        if country in selected_by_default:
            checkboxes[country] = columns[i % num_columns].checkbox(country, value=True)
        else:
            checkboxes[country] = columns[i % num_columns].checkbox(country, value=False)
        if checkboxes[country]:
            ax.plot(grouped_data.get_group(country)['TIME_PERIOD'], grouped_data.get_group(country)['OBS_VALUE'],
                    label=country)
    ax.set_xlabel('Rok')
    ax.set_ylabel('Ilość śmierci na 100 tys. mieszkańców')
    ax.legend()

    st.pyplot(fig)
