def get_age_groups_module(df, st, plt):
    st.subheader("Liczba rejestrowanych pojazdów w danym wieku")
    used = ["UŻYW. IMPORT INDYW", "UŻYW. ZAKUPIONY W KRAJU"]
    df_filtered = df[df["Source"].isin(used)]
    df_filtered["Age"] = df["Year"] - df["ProductionYear"]

    selected_range_df = df_filtered[(df_filtered["Age"] >= 1) & (df_filtered["Age"] <= 30)]
    selected_range_df = selected_range_df.groupby("Age").size().reset_index(name="Count")

    fig, ax = plt.subplots()
    ax.barh(y=selected_range_df["Age"], width=selected_range_df["Count"], color='orangered')
    ax.set_yticks(range(len(selected_range_df["Age"])+1))
    st.pyplot(fig)
