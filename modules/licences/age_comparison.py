def get_age_comparison_module(df, st, plt):
    years = list(range(df["Date"].min(), df["Date"].max()+1))

    col1, col2 = st.columns(2)
    with col2:
        option = st.selectbox("Rok", years, index=len(years)-1)
    with col1:
        fig, ax = plt.subplots()
        grouped_by_age = df[df["Date"]==option].groupby("Age")["Value"].sum().reset_index()

        inner_circle = plt.Circle( (0,0), 0.6, color='white') # pyright: ignore
        ax.pie(grouped_by_age["Value"], labels=grouped_by_age["Age"], wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' })
        ax.add_artist(inner_circle)
        # ax.text(0,0, 'Rozkład wydanych uprawnień\n na grupy wiekowe dla 2022 roku', ha='center', va='center', fontsize=2.)

        st.pyplot(fig, dpi=1000)
