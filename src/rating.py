import numpy as np
import copy

def get_rating_arr_for_game(game: np.ndarray):
    n_players = len(game)
    rating_arr = []
    for i in range(n_players):
        player = game[i]
        player_net = calc_player_net(player)
        rating_arr.append({"name": player[0], "net": player_net})
    return rating_arr

def calc_player_net(player: np.ndarray):
    values = player[-4:]
    buy_ins, end_game, base_chips, chip_value = values 
    return round(chip_value * (end_game - (base_chips * buy_ins)), 2)

def get_game_rating(game_players: np.ndarray, current_ratings, game_numbers, date):
    pot_total = calc_pot_total(game_players)
    n_players = len(game_players)

    for i in range(n_players):
        game_player = game_players[i]
        player_name = game_player["name"]
        player_net = game_player["net"]
        player = current_ratings[player_name]
        n_player_games = game_numbers[player_name]
    
        rating_sum = 0
        for j in range(n_players):
            if (i == j): continue
            comp_player_name = game_players[j]["name"]
            comp_player_net = game_players[j]["net"]
            comp_player = current_ratings[comp_player_name]
            comp_player_games = game_numbers[comp_player_name]
            net_diff = player_net - comp_player_net

            rating_sum += calc_comp_rating_sum(net_diff, pot_total, player, comp_player, comp_player_games)

        player_game_multi = (n_player_games+1)/(n_player_games+2)
        game_player["new_rating"] = player + (20-n_players) * rating_sum * player_game_multi
    return get_all_new_ratings(current_ratings,game_players,game_numbers,date)

def calc_pot_total(game: np.ndarray):
    pot_total = 0
    for n in game:
        pot_total += abs(n["net"])
    return round(pot_total/2, 2)

def calc_comp_rating_sum(net, pot, player, competitor, n_competitor_games):
    s_value, winner_rating, loser_rating = calc_s_winner_loser_values(net, player, competitor)

    margin = margin_of_victory_multiplier(net, pot, winner_rating, loser_rating)
    comp_game_multi = (n_competitor_games+1)/(n_competitor_games+2)
    elo_equation = (s_value - 1/(1+10**((competitor-player)/1000)))

    return margin * comp_game_multi * elo_equation

def calc_s_winner_loser_values(net, player, competitor):
    if (net > 0): return 1, player, competitor
    if (net == 0): return 0.5, 0, 0
    if (net < 0): return 0, competitor, player
    

def margin_of_victory_multiplier(net, pot, winner, loser):
    return (np.log(abs(net/pot) + 1)*(5.2/((winner-loser)*0.0005+5.2)))     

def get_all_new_ratings(current, game_players, n_games, date):
    new_ratings = copy.deepcopy(current)
    for player in game_players:
        rating = player["new_rating"]
        n_games[player['name']] +=1
        new_ratings[player['name']] = rating
    new_ratings["date"] = date
    return new_ratings