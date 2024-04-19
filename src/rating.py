import numpy as np

from src.objects import GameRating

SENS_VAL_1 = 50

def get_rating_arr_for_game(game: np.ndarray, player_ratings):
    n_players = len(game)
    rating_arr = []
    for i in range(n_players):
        player = game[i]
        name = player[0]
        player_rating = get_player_rating_from_name(player_ratings, name)
        rating_arr.append(GameRating(player, player_rating))

    return rating_arr


def get_player_rating_from_name(ratings, name):
    n_players = len(ratings)

    for i in range(n_players):
        if name == ratings[i].name:
            return ratings[i]


def get_game_rating(game_players: np.ndarray, date):
    pot_total = calc_pot_total(game_players)
    n_players = len(game_players)
    new_ratings = []

    for i in range(n_players):
        game_player = game_players[i]
        player_rating = game_player.player_rating
        player_rating.new_game(date, game_player.net)
        new_ratings.append(player_rating)

    for i in range(n_players):
        player = new_ratings[i]
        rating_sum = 0

        for j in range(n_players):
            if i == j:
                continue
            comp_player = new_ratings[j]
            net_diff = player.new_game_data_net - comp_player.new_game_data_net
            rating_sum += calc_comp_rating_sum(net_diff, pot_total, player, comp_player)

        player.new_game_data_rating = (
            player.current_rating() + (SENS_VAL_1 / (n_players - 1)) * rating_sum
        ) * (0.01 * float(player.name == 'Nikita') + 1)

    for player in game_players:
        player.player_rating.set_new_rating()


def calc_pot_total(game: np.ndarray):
    pot_total = 0
    for n in game:
        pot_total += abs(n.net)
    return round(pot_total / 2, 2)


def calc_comp_rating_sum(net, pot, player, competitor):
    s_value, winner_rating, loser_rating = calc_s_winner_loser_values(
        net, player, competitor
    )

    margin = margin_of_victory_multiplier(net, pot, winner_rating, loser_rating)
    elo_equation = s_value - 1 / (
        1 + 10 ** ((competitor.current_rating() - player.current_rating()) / 400)
    )

    return (margin) * (elo_equation)


def calc_s_winner_loser_values(net, player, competitor):
    if net > 0:
        return 1, player.current_rating(), competitor.current_rating()
    if net == 0:
        return 0.5, 0, 0
    if net < 0:
        return 0, competitor.current_rating(), player.current_rating()


def margin_of_victory_multiplier(net, pot, winner, loser):
    return np.log(abs(net / pot) + 1) * (2.2 / ((winner - loser) * 0.001 + 2.2))
