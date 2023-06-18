
def get_sex_comparison_module(df, st, plt):
    age_groups = df["Age"].unique()
    age_groups.sort()

    categories = df["Type"].unique()
    categories.sort()

    st.subheader("Liczba wydanych uprawnień według płci i wieku")
    col1, col2 = st.columns(2)
    with col1:
        selected_age_groups = st.multiselect("Kategoria wiekowa", age_groups, age_groups)
    with col2:
        selected_categories = st.multiselect("Kategoria dokumentu", categories, ["B"])
    if (not selected_age_groups) or (not selected_categories):
        st.text("Musisz wybrać przynajmniej jedną kategorię dokumentu i wieku")
    else:
        df_age = df[df["Age"].isin(selected_age_groups) & (df['Type'].isin(selected_categories))]
        df_age = df_age.groupby(['Date', 'Sex'])['Value'].sum().reset_index()

        df_fe = df_age[df_age['Sex'] == 'KOBIETY']['Value']
        df_ma = df_age[df_age['Sex'] == 'MĘŻCZYŹNI']['Value']

        years = list(range(df['Date'].min(), df['Date'].max()+1))

        fig, ax = plt.subplots()
        ax.plot(years, df_fe, label="Kobiety", color="magenta")
        ax.fill_between(years, df_fe, alpha=0.2, color="orchid")
        ax.plot(years, df_ma, label="Mężczyźni", color="deepskyblue")
        ax.fill_between(years, df_ma, alpha=0.2, color="lightskyblue")

        ax.set_axisbelow(True)
        ax.yaxis.grid()

        ax.set_xticks(years)
        ax.legend()
        st.pyplot(fig, dpi=500)

