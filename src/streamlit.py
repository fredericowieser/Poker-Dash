from src.lib import color_red_green_nums
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
import random

def make_gui(df, players, games, guests, regulars):
    st.set_page_config(layout="wide")
    
    # Side Bar
    mode: str
    with st.sidebar:
        mode = make_sidebar()
        
    if mode == "Home": home_page(players, guests, regulars)
    if mode == "Players": players_page(players)
    if mode == "Games": games_page(games)
    
    
def make_sidebar():
    choose = option_menu(
        "Poker Dash", 
        [
            "Home",
            "Players",
            "Games",
            #TODO: "Player Groups",
            #TODO: "Running Aggregates",
            
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
    

def home_page(players, guests, regulars):
    # Title + Intro
    st.title('Poker Dashboard')
    st.markdown('This is a web app to allow exploration of our weekly Poker games, I hope you enjoy!')
    
    # Main Plot of Regulae
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    for player in regulars:
        ax.plot(player.dates, player.running_net, 'o-', label=f'{player.name}')
    
    # TODO: Add more advanced lengeding with this 
    # https://python-graph-gallery.com/web-line-chart-with-labels-at-line-end/
    ax.set_xlabel('Date')  # Add an x-label to the axes.
    ax.set_ylabel('Weekly Net Cash (£GBP)')  # Add a y-label to the axes.
    ax.set_title('Running Net for All Regular Players')  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    ax.grid()
    st.pyplot(fig)
        
    # Main Rankings
    data = []
    for player in players:
        data.append([
            player.name,
            player.current_net,
            player.n_games,
            player.n_wins,
            player.avg_n_buyins,
            player.invested_cash
        ])
            
    all_time_net_df = pd.DataFrame(data, columns=[
        'Weekly Net',
        'Cash (£GBP)',
        'No. Games',
        'Wins',
        'Avg. Buy-Ins',
        'Invested',
    ])
    all_time_net_df = all_time_net_df.set_index(all_time_net_df.columns[0])
    all_time_net_df = all_time_net_df.sort_values(by=['Cash (£GBP)'], ascending=False)
    
    # Todo: Display values with 2dp    
    for i in range(len(all_time_net_df['Cash (£GBP)'])):
        all_time_net_df['Cash (£GBP)'][i] = round(
            all_time_net_df['Cash (£GBP)'][i].tolist(),
            2,
        )
        
    all_time_net_df = all_time_net_df.style.applymap(color_red_green_nums)
    st.dataframe(all_time_net_df, use_container_width=True, height=37*len(players))

    
    # Rules and Info
    st.title('Information')
    st.markdown(
        """
        - When speaking about regular and guest players we mean players who have played more the 3 games and those with 3 and under.
        
        - Everyone starts with the same amount of money,
        
        - If you lose all your money you can buyin upto the same amount you started with.
        
        """
    )
    
    

def players_page(players):
    def make_player_info_card(players, key=0):
        # Net Cash graph creating over all time
        l = len(players)
        option = st.selectbox(
            'Which player to you want to see?',
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


def games_page(games):
    def make_game_info_card(games, key=0):
        # Net Cash graph creating over all time
        l = len(games)
        option = st.selectbox(
            'Which game to you want to see?',
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

        