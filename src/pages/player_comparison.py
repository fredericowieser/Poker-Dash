import streamlit as st
import matplotlib.pyplot as plt

def players_page(players):
    def make_player_info_card(players, key=0):
        # Net Cash graph creating over all time
        l = len(players)
        option = st.selectbox(
            "Which player to you want to see?",
            (player.name for player in players),
            key=f"{key}",
        )
        for i in range(l):
            if option == players[i].name:
                player = players[i]
                # Player Running Net Graph
                st.pyplot(player.st_cash_v_time, use_container_width=True)

                # Create Stats Dataframe
                st.dataframe(player.stats_df, use_container_width=True)

                # Create Net Cash Dataframe
                st.dataframe(player.net_cash_df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        make_player_info_card(players, 1)
    with col2:
        make_player_info_card(players, 2)