import datetime
import numpy as np

class PlayerRating:
    def __init__(self, name):
        self.name = name
        self.rating_data_date = [datetime.date(2023, 2, 8)]
        self.rating_data_rating = [1000]
        self.n_games = 0
    
    def new_game(self, date, net):
        self.n_games +=1
        self.new_game_data_date = date
        self.new_game_data_rating = self.current_rating()
        self.new_game_data_net = net
    
    def current_rating(self):
        return self.rating_data_rating[-1]
    
    def set_new_rating(self):
        self.rating_data_date.append(self.new_game_data_date)
        self.rating_data_rating.append(self.new_game_data_rating)

class GameRating:
    def __init__(self, player, player_rating):
        self.name = player[0]
        self.net = self.calc_player_net(player)
        self.player_rating = player_rating
    
    def calc_player_net(_,player):
        buy_ins, end_game, base_chips, chip_value = player[-4:]
        return round(chip_value * (end_game - (base_chips * buy_ins)), 2)

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
        if name == ratings[i].name: return ratings[i]

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
            if (i == j): continue
            comp_player = new_ratings[j]
            net_diff = player.new_game_data_net - comp_player.new_game_data_net
            rating_sum += calc_comp_rating_sum(net_diff, pot_total, player, comp_player)

        player_game_multi = (player.n_games)/(player.n_games+1)
        player.new_game_data_rating = player.current_rating() + (40-n_players) * rating_sum * player_game_multi

    for player in game_players:
        player.player_rating.set_new_rating()

def calc_pot_total(game: np.ndarray):
    pot_total = 0
    for n in game:
        pot_total += abs(n.net)
    return round(pot_total/2, 2)

def calc_comp_rating_sum(net, pot, player, competitor):
    s_value, winner_rating, loser_rating = calc_s_winner_loser_values(net, player, competitor)

    margin = margin_of_victory_multiplier(net, pot, winner_rating, loser_rating)
    comp_game_multi = (competitor.n_games)/(competitor.n_games+1)
    elo_equation = (s_value - 1/(1+10**((competitor.current_rating()-player.current_rating())/1000)))

    return (margin) * (comp_game_multi) * (elo_equation)

def calc_s_winner_loser_values(net, player, competitor):
    if (net > 0): return 1, player.current_rating(), competitor.current_rating()
    if (net == 0): return 0.5, 0, 0
    if (net < 0): return 0, competitor.current_rating(), player.current_rating()
    

def margin_of_victory_multiplier(net, pot, winner, loser):
    return (np.log(abs(net/pot) + 1)*(4.4/((winner-loser)*0.001+4.4)))     
