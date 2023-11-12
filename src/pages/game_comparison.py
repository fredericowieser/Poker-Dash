import streamlit as st
import matplotlib.pyplot as plt

def games_page(games):
    def make_game_info_card(games, key=0):
        # Net Cash graph creating over all time
        l = len(games)
        option = st.selectbox(
            "Which game to you want to see?",
            (game.datestr for game in games),
            key=f"{key}",
        )
        for i in range(l):
            if option == games[i].datestr:
                game = games[i]
                # Create Stats Dataframe
                st.dataframe(game.stats_df, use_container_width=True)

                # Create Scoreboard Dataframe
                st.dataframe(game.scoreboard_df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        make_game_info_card(games, 1)
    with col2:
        make_game_info_card(games, 2)