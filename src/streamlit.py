import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go

def make_gui(df, players, games):
    # Side Bar
    mode: str
    with st.sidebar:
        mode = make_sidebar()
        
    if mode == "Home": home_page(players)
    if mode == "Players": players_page(players)
    
    
def make_sidebar():
    choose = option_menu(
        "Poker Dash", 
        [
            "Home",
            "Players",
            "Games",
            "Player Groups",
            "Running Aggregates",
            
        ],
        icons=[
            'house',
            'person',
            'bullseye',
            'people',
            'clock'
        ],
        menu_icon="app-indicator",
        default_index=0,
        )
    return choose
    

def home_page(players):
    # Title + Intro
    st.title('Poker Dashboard')
    st.text('This is a web app to allow exploration of our weekly Poker games, I hope you enjoy!')
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    for player in players:
        if player.n_games > 4:
            #if player.name == "Catherine":
            #    import ipdb; ipdb.set_trace()
            ax.plot(player.dates, player.running_net, 'o-', label=f'{player.name}')
    
    ax.set_xlabel('Date')  # Add an x-label to the axes.
    ax.set_ylabel('Weekly Net Cash (£GBP)')  # Add a y-label to the axes.
    ax.set_title('Running Net for All Games')  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    st.pyplot(fig)
    
def players_page(players):
    def make_player_info_card(players, key=0):
        # Net Cash graph creating over all time
        l = len(players)
        option = st.selectbox(
            'Which player to you want to see?',
            (player.name for player in players),
            key=f"{key}"
        )
        for i in range(l):
            if option == players[i].name:
                player = players[i]
                # Player Running Net Graph
                st.pyplot(player.st_cash_v_time)
        
                # Create Stats Dataframe
                st.dataframe(player.stats_df)
            
    col1, col2 = st.columns(2)
    with col1:
        make_player_info_card(players, 1)
    with col2:
        make_player_info_card(players, 2)

        