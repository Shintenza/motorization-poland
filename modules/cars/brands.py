def get_brands_module(df, st, plt):

    col1, col2 = st.columns(2)
    with col1:
        year_to_filter = st.slider('Rok', 2010, 2022, 2022)
    with col2:
        number_of_brands = st.slider('Liczba wyników', 2, 35, 10) 

    most_popular_brands = df[df["Year"]==year_to_filter].groupby('Brand').size().reset_index(name='Count')
    most_popular_brands = most_popular_brands.sort_values('Count', ascending=False).head(number_of_brands)

    most_popular_cars = df[df["Year"] == int(year_to_filter)].groupby(["Brand", "Model"]).size().reset_index(name="Count")
    most_popular_cars = most_popular_cars.sort_values("Count", ascending=False).head(number_of_brands)
    most_popular_cars["FullName"] = most_popular_cars.apply(lambda row: f"{row['Brand']} {row['Model']}", axis=1)

    st.subheader(f"Najpopularniejsza marka pojazdów w roku {year_to_filter}")
    fig, ax = plt.subplots()
    ax.hlines(y=most_popular_brands["Brand"], xmin=0, xmax= most_popular_brands["Count"], color="magenta")
    ax.plot(most_popular_brands["Count"], most_popular_brands["Brand"], "o", color="magenta")
    for i, count in enumerate(most_popular_brands["Count"]):
        plt.text(count + 2000, i, str(count), va='center')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader(f"Najczęściej rejestrowane pojazdy w {year_to_filter}")
    fig, ax = plt.subplots()
    ax.hlines(y=most_popular_cars["FullName"], xmin=0, xmax= most_popular_cars["Count"], color="cyan")
    ax.plot(most_popular_cars["Count"], most_popular_cars["FullName"], "o", color="cyan")
    for i, count in enumerate(most_popular_cars["Count"]):
        plt.text(count + 1000, i, str(count), va='center')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)
