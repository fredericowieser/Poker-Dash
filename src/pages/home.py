import datetime
from math import ceil, floor
from typing import List

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

from src.lib import color_red_green_nums
from src.objects import Player


def home_page(players, end_date, total_n_games):
    st.title("Poker Dash")

    # Select Players based on N gmaes played
    selected_n_games = st.select_slider(
        "Select how many games the players shown have played:",
        options=range(total_n_games),
        value=round(total_n_games ** (1 / 2)),
    )
    selected_players = []
    for player in players:
        if player.n_games > selected_n_games:
            selected_players.append(player)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = make_main_page_graph(selected_players, end_date, selected_n_games)
        st.pyplot(fig)
    with col2:
        fig = make_gelo_graph(selected_players, end_date, selected_n_games)
        st.pyplot(fig)

    #fig1 = make_an_last_n_games_graph(selected_players)
    #st.pyplot(fig1)

    # Main Rankings
    data = []
    COLUMNS = [
        "Name",
        "Cash (£)",
        "GELO",
        "No. Games",
        "Wins",
        "Avg. Buy-Ins",
        "Invested (£)",
        "Std. Dev. WN (£)",
        "Avg. WN (£)",
        "Avg. WN Last 3 Games (£)",
        "Avg. WN Last 5 Games (£)",
        "Avg. WN Last 8 Games (£)",
        "Win-Loss Ratio",
        "Last Game",
    ]
    for player in selected_players:
        data.append(
            [
                player.name,
                player.current_net,
                player.current_gelo,
                player.n_games,
                player.n_wins,
                player.avg_n_buyins,
                player.invested_cash,
                player.std_dev_net_cash,
                player.avg_net_cash,
                np.average(player.net_last_n_games(3)),
                np.average(player.net_last_n_games(5)),
                np.average(player.net_last_n_games(8)),
                player.win_loss_ratio,
                player.dates[-1],
            ]
        )

    all_time_net_df = pd.DataFrame(
        data,
        columns=COLUMNS,
    )
    all_time_net_df = all_time_net_df.set_index(all_time_net_df.columns[0])
    all_time_net_df = all_time_net_df.sort_values(
        by=["Cash (£)"],
        ascending=False,
    )

    st.title("Leaderboard")
    st.dataframe(
        all_time_net_df.style.format(
            subset=[
                "Cash (£)",
                "GELO",
                "Avg. Buy-Ins",
                "Invested (£)",
                "Std. Dev. WN (£)",
                "Avg. WN (£)",
                "Avg. WN Last 3 Games (£)",
                "Avg. WN Last 5 Games (£)",
                "Avg. WN Last 8 Games (£)",
            ], formatter="{:.2f}"
        ).applymap(color_red_green_nums),
        use_container_width=True,
        height=39*len(selected_players),
    )

    st.title("Plot Creator")

    # TODO: Add random scatter.s = len(COLUMNS)
    ax_x = st.selectbox(
        "Choose the X axis of the scatter plot below.",
        COLUMNS,
        index=1,
    )
    ax_y = st.selectbox(
        "Choose the Y axis of the scatter plot below.",
        COLUMNS,
        index=2,
    )
    d = st.number_input('Select degree of polynomial for curve fit', value=2)
    col5, col6 = st.columns(2)
    with col5:
        x = st.checkbox('Show y=0')
    with col6:
        y = st.checkbox('Show x=0')

    # all_time_net_df['Date'] = all_time_net_df['Date'].astype(str)
    scatter_fig = make_2D_plot_on_players(
        all_time_net_df,
        ax_x,
        ax_y,
        selected_players,
        xax=True if x else False,
        yax=True if y else False,
        d=d
    )
    st.pyplot(scatter_fig)

    st.title("Static Plots")

    col3, col4 = st.columns(2)
    with col3:
        fig1 = make_2D_plot_on_players(
            all_time_net_df,
            "Std. Dev. WN (£)",
            "Avg. Buy-Ins",
            selected_players
        )
        st.pyplot(fig1)
    with col4:
        fig = make_2D_plot_on_players(
            all_time_net_df,
            "Std. Dev. WN (£)",
            "Avg. WN (£)",
            selected_players,
            xax=True,
        )
        st.pyplot(fig)

def make_2D_plot_on_players(df, c1: str, c2: str, selected_players: List, xax=False, yax=False, d=2):
    x = df[c1]
    y = df[c2]

    fig = plt.figure()

    if xax: plt.axhline(y=0, c="white", label="y=0", alpha=0.75)
    if yax: plt.axvline(x=0, c="white", label="x=0", alpha=0.75)

    # Scatter Plot of Players
    for player in selected_players:
        plt.scatter(
            x[player.name],
            y[player.name],
            label=f"{player.name}",
            c=player.color,
        )
        plt.text(
            x[player.name],
            y[player.name],
            f"{player.name}",
        )

    # Regression of Players
    x_np = x.values.reshape(-1, 1)
    y_np = y.values.reshape(-1, 1)

    model = Pipeline([
        ('poly', PolynomialFeatures(degree=d)),
        ('linear', LinearRegression(fit_intercept=False))
    ])

    model.fit(x_np, y_np)  # perform linear regression
    x_np_sorted = sorted(x_np)
    x_lin = np.linspace(x_np_sorted[0], x_np_sorted[-1])
    y_pred = model.predict(x_lin)  # make predictions
    plt.plot(x_lin, y_pred, color='pink')

    plt.xlabel(c1)
    plt.ylabel(c2)
    plt.title(
        f"{c1} vs. {c2}"
    )
    plt.style.use("dark_background")
    plt.grid(visible=True, alpha=0.25)

    return fig
    

def rnd(x, up=True, grain=5):
    if up:
        return ceil(x / grain) * grain
    return floor(x / grain) * grain


def make_main_page_graph(selected_players, end_date, selected_n_games):
    fig = plt.figure()

    for player in selected_players:
        plt.plot(
            player.dates,
            player.running_net,
            "-",
            label=f"{player.name}",
            c=player.color,
        )

    plt.xlabel("Date")
    plt.ylabel("Weekly Net Cash (£GBP)")
    plt.title(
        f"Running Net for Selected Players (No. Games > {selected_n_games})"
    )

    plt.style.use("dark_background")
    plt.grid(visible=True, alpha=0.25)

    x_mid = end_date + datetime.timedelta(days=7)
    x_end = end_date + datetime.timedelta(days=14)

    tmp_max = 0
    tmp_min = 0
    for player in selected_players:
        if tmp_max < player.max_rn:
            tmp_max = player.max_rn
        if tmp_min > player.min_rn:
            tmp_min = player.min_rn

    MAX_RN = rnd(tmp_max)
    MIN_RN = rnd(tmp_min, up=False)

    plt.ylim(MIN_RN - 5, MAX_RN + 5)

    # Sort selected_players by current running net
    # create a numpy array to spread out line plot labels
    selected_players.sort(key=lambda x: x.current_net)

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
            color="white",
            alpha=0.4,
            ls="dashed",
        )

        # Add Player name label
        plt.text(
            x_end,
            y_end,
            player.name,
            c=player.color,
            fontsize=12,
            weight="bold",
            va="center",
        )

        i += 1

    fig.autofmt_xdate()

    return fig

def make_gelo_graph(selected_players, end_date, selected_n_games):
    fig = plt.figure()

    selected_players.sort(key=lambda x: x.current_gelo)

    for player in selected_players:
        plt.plot(
            player.rating_data_date,
            player.rating_data_rating,
            "-",
            label=f"{player.name}",
            c=player.color,
        )

    plt.xlabel("Date")
    plt.ylabel("GELO")
    plt.title(
        f"GELO for Selected Players (No. Games > {selected_n_games})"
    )

    plt.style.use("dark_background")
    plt.grid(visible=True, alpha=0.25)

    x_mid = end_date + datetime.timedelta(days=7)
    x_end = end_date + datetime.timedelta(days=14)

    tmp_max = 1000
    tmp_min = 1000
    for player in selected_players:
        if tmp_max < player.max_rating:
            tmp_max = player.max_rating
        if tmp_min > player.min_rating:
            tmp_min = player.min_rating

    g = 1
    MAX_RN = rnd(tmp_max, grain=g) 
    MIN_RN = rnd(tmp_min, up=False, grain=g)

    plt.ylim(MIN_RN - 5, MAX_RN + 5)

    Y_ENDS = np.linspace(MIN_RN, MAX_RN, num=len(selected_players))

    i = 0
    for player in selected_players:
        y_end = Y_ENDS[i]

        # Create points for dashed line
        x_start = player.rating_data_date[-1]
        y_start = player.rating_data_rating[-1]
        y_mid = player.rating_data_rating[-1]

        # Add line based on three points
        plt.plot(
            [x_start, x_mid, x_end],
            [y_start, y_mid, y_end],
            color="white",
            alpha=0.4,
            ls="dashed",
        )

        # Add Player name label
        plt.text(
            x_end,
            y_end,
            player.name,
            c=player.color,
            fontsize=12,
            weight="bold",
            va="center",
        )

        i += 1

    fig.autofmt_xdate()

    return fig

def make_an_last_n_games_graph(selected_players):
    fig = plt.figure()

    selected_players.sort(key=lambda x: x.current_gelo)

    for player in selected_players:
        plt.plot(
            [i+1 for i in range(player.n_games)],
            player.avg_net_last_n_games_array,
            "-",
            label=f"{player.name}",
            c=player.color,
        )

    plt.xlabel("N Weeks")
    plt.ylabel("Avg. Net.")
    plt.title(
        f"Avg. Net Over Last N Weeks for Selected Players"
    )

    plt.style.use("dark_background")
    plt.grid(visible=True, alpha=0.25)

    tmp_max = 0
    tmp_min = 0
    for player in selected_players:
        pmax = max(player.avg_net_last_n_games_array)
        pmin = min(player.avg_net_last_n_games_array)
        if tmp_max < pmax:
            tmp_max = pmax
        if tmp_min > pmin:
            tmp_min = pmin

    g = 1
    MAX_RN = rnd(tmp_max, grain=g) 
    MIN_RN = rnd(tmp_min, up=False, grain=g)

    plt.ylim(MIN_RN - 5, MAX_RN + 5)

    Y_ENDS = np.linspace(MIN_RN, MAX_RN, num=len(selected_players))

    i = 0
    for player in selected_players:
        y_end = Y_ENDS[i]

        # Create points for dashed line
        x_start = player.n_games
        y_start = player.avg_net_last_n_games_array[-1]
        y_mid = player.avg_net_last_n_games_array[-1]

        # import pdb; pdb.set_trace()

        # Add line based on three points
        plt.plot(
            [x_start, x_start, x_start],
            [y_start, y_mid, y_end],
            color="white",
            alpha=0.4,
            ls="dashed",
        )

        # Add Player name label
        plt.text(
            x_start,
            y_end,
            player.name,
            c=player.color,
            fontsize=12,
            weight="bold",
            va="center",
        )

        i += 1

    fig.autofmt_xdate()

    return fig