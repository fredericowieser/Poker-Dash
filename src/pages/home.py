import datetime
from math import ceil, floor

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.lib import color_red_green_nums


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
    fig = make_main_page_graph(selected_players, end_date, selected_n_games)
    st.pyplot(fig)

    # Main Rankings
    data = []
    for player in selected_players:
        data.append(
            [
                player.name,
                player.current_net,
                player.n_games,
                player.n_wins,
                player.avg_n_buyins,
                player.invested_cash,
                player.avg_net_cash,
                player.std_dev_net_cash,
                np.average(player.net_last_n_games(3)),
                player.win_loss_ratio,
            ]
        )

    all_time_net_df = pd.DataFrame(
        data,
        columns=[
            "Weekly Net (WN)",
            "Cash (£)",
            "No. Games",
            "Wins",
            "Avg. Buy-Ins",
            "Invested (£)",
            "Avg. WN (£)",
            "Std. Dev. WN (£)",
            "Avg. WN Last 3 Games (£)",
            "Win-Loss Ratio"
        ],
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
                "Avg. Buy-Ins",
                "Invested (£)",
                "Avg. WN (£)",
                "Std. Dev. WN (£)",
                "Avg. WN Last 3 Games (£)"
            ], formatter="{:.2f}"
        ).applymap(color_red_green_nums),
        use_container_width=True,
        height=39*len(selected_players),
    )


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