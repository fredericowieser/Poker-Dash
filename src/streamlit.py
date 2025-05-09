import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Plotly Libraries
# import plotly
# import plotly.express as px
# import plotly.graph_objects as go
from streamlit_option_menu import option_menu

import streamlit as st
# import streamlit.components.v1 as components
from src.lib import color_red_green_nums
from src.pages.home import home_page
from src.pages.player_comparison import players_page
from src.pages.game_comparison import games_page


def make_gui(df, players, games):
    st.set_page_config(layout="wide")

    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # Side Bar
    mode: str
    with st.sidebar:
        mode = make_sidebar()

    if mode == "Home":
        home_page(
            players=players,
            end_date=df["Date"].iloc[-1],
            total_n_games=len(games),
        )
    if mode == "Players":
        players_page(players)
    if mode == "Games":
        games_page(games)


def make_sidebar():
    choose = option_menu(
        "Poker Dash",
        [
            "Home",
            "Players",
            "Games",
            # TODO: "Player Groups",
            # TODO: "Running Aggregates",
        ],
        icons=[
            "house",
            "person",
            "bullseye",
            #"people",
            #'clock'
        ],
        menu_icon="app-indicator",
        default_index=0,
    )
    return choose
