from src.lib import color_red_green_nums
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import plotly
import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit.components.v1 as components
import datetime
from math import ceil, floor

def make_gui(df, players, games, player_ratings):
    st.set_page_config(layout="wide")
    
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    
    # Side Bar
    mode: str
    with st.sidebar:
        mode = make_sidebar()
        
    if mode == "Home": home_page(
        players=players,
        end_date=df['Date'].iloc[-1],
        total_n_games=len(games),
    )
    if mode == "Players": players_page(players)
    if mode == "Games": games_page(games)
    if mode == "GELO": ratings_page(player_ratings)
    
    
def make_sidebar():
    choose = option_menu(
        "Poker Dash", 
        [
            "Home",
            "Players",
            "Games",
            "GELO"
            #TODO: "Player Groups",
            #TODO: "Running Aggregates",
            
        ],
        icons=[
            'house',
            'person',
            'bullseye',
            'people',
            #'clock'
        ],
        menu_icon="app-indicator",
        default_index=0,
        )
    return choose


def home_page(players, end_date, total_n_games):
    # Title + Intro
    st.title('Poker Dash')
    
    selected_n_games = st.select_slider(
        'Select how many games the players shown have played:',
        options=range(total_n_games),
        value=round(total_n_games/2),
    )
    
    selected_players = []
    for player in players:
        if player.n_games > selected_n_games: selected_players.append(player)
    
    fig = make_main_page_graph(selected_players, end_date, selected_n_games)
    st.pyplot(fig)
    
    # # Plotly: Main Plot of Regulars
    # fig = go.Figure()
    
    # for player in regulars:
    #     fig.add_trace(go.Scatter(
    #         x=player.dates,
    #         y=player.running_net,
    #         mode='lines+markers',
    #         name=player.name,
    #     ))
    
    # # TODO: Add more advanced lengeding with this 
    # # https://python-graph-gallery.com/web-line-chart-with-labels-at-line-end/
    # fig.update_layout(
    #     title='Running Net for All Regular Players',
    #     xaxis_title='Date',
    #     yaxis_title='Net Cash (£GBP)'
    # )
    
    # st.plotly_chart(
    #     fig,
    #     use_container_width=True,
    #     theme=None,
    # )
        
    # Main Rankings
    data = []
    for player in selected_players:
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
    st.title('Leaderboard')
    st.dataframe(all_time_net_df, use_container_width=True, height=39*len(selected_players))

    
    # Rules and Info
    st.title('Information')
    st.markdown(
        """
        - Players are considered 'Regular' if they have played more than 3 games, or a 'Guest' if they have played 3 games or lower
        
        - Everyone starts with the same amount of money - the buy in limit (£5)
        
        - If you lose all your money you can buy in up to the buy in limit
        
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

def ratings_page(ratings_arr):
    # Main Plot of Regulae
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    n_games = len(ratings_arr)

    for i in range(n_games):
        player = ratings_arr[i]
        if player.n_games > 5: 
            ax.plot(
                player.rating_data_date,
                player.rating_data_rating,
                'o-',
                label=f'{player.name}'
            )

    # TODO: Add more advanced lengeding with this 
    # https://python-graph-gallery.com/web-line-chart-with-labels-at-line-end/
    ax.set_xlabel('Date')  # Add an x-label to the axes.
    ax.set_ylabel('GELO rating')  # Add a y-label to the axes.
    ax.set_title('Running GELO ratings for players with >4 games')  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    ax.grid()
    st.pyplot(fig)

    
def player_comparison_page(players):
    return None


def history_page():
    return None


def friends_and_foes_page(players):
    return None


def data_upload_page(players):
    return None


def awards_page(players):
    return None


def raw_data_page(players):
    return None


def make_main_page_graph(selected_players, end_date, selected_n_games):
    # Main Plot of Regulars
    fig = plt.figure()
    #fig.patch.set_facecolor('mediumseagreen')
    fig.patch.set_facecolor('lightblue')
    
    for player in selected_players:
        plt.plot(
            player.dates,
            player.running_net,
            '-',
            label=f'{player.name}',
            color=player.color,
        )
    
    # TODO: Add more advanced lengeding with this 
    # https://python-graph-gallery.com/web-line-chart-with-labels-at-line-end/
    plt.xlabel('Date')
    plt.ylabel('Weekly Net Cash (£GBP)')
    plt.title(
        f'Running Net for Selected Players (No. Games > {selected_n_games})'
    )
    
    plt.style.use('dark_background')
    #plt.style.use('ggplot')
    plt.grid(visible=True, alpha=0.25)

    x_mid = end_date + datetime.timedelta(days=7)
    x_end = end_date + datetime.timedelta(days=14)
    
    #import ipdb; ipdb.set_trace()
    
    tmp_max = 0
    tmp_min = 0
    for player in selected_players:
        if tmp_max < player.max_rn: tmp_max = player.max_rn
        if tmp_min > player.min_rn: tmp_min = player.min_rn
    
    def rnd(x, up=True, grain=5):
        if up: return ceil(x / grain) * grain
        return floor(x / grain) * grain
    
    MAX_RN = rnd(tmp_max)
    MIN_RN = rnd(tmp_min, up=False)
    
    plt.ylim(MIN_RN-5, MAX_RN+5)
    
    #Sort selected_players by current running net
    #create a numpy array to spread out line plot labels
    selected_players.sort(
        key=lambda x: x.current_net
    )
    
    Y_ENDS = np.linspace(MIN_RN, MAX_RN, num=len(selected_players))
    
    i = 0
    for player in selected_players:
        
        y_end = Y_ENDS[i]
        
        # Create points for dashed line
        x_start = player.dates[-1]
        y_start = player.running_net[-1]
        y_mid = player.running_net[-1]
        
        # Add line based on three points
        plt.plot(
            [x_start, x_mid, x_end], 
            [y_start, y_mid, y_end], 
            color=player.color, 
            alpha=0.75, 
            ls="dashed"
        )
        
        # Add Player name label
        plt.text(
            x_end, 
            y_end, 
            player.name, 
            color=player.color, 
            fontsize=12, 
            weight="bold",
            va="center",
        )
        
        i += 1

    fig.autofmt_xdate()
    
    return fig
