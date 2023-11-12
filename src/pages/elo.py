import streamlit as st
import matplotlib.pyplot as plt

def ratings_page(ratings_arr):
    # Main Plot of Regulae
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    n_games = len(ratings_arr)

    for i in range(n_games):
        player = ratings_arr[i]
        if player.n_games > 5:
            ax.plot(
                player.rating_data_date,
                player.rating_data_rating,
                "o-",
                label=f"{player.name}",
            )

    # TODO: Add more advanced lengeding with this
    # https://python-graph-gallery.com/web-line-chart-with-labels-at-line-end/
    ax.set_xlabel("Date")  # Add an x-label to the axes.
    ax.set_ylabel("GELO rating")  # Add a y-label to the axes.
    ax.set_title(
        "Running GELO ratings for players with >4 games"
    )  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    ax.grid()
    st.pyplot(fig)