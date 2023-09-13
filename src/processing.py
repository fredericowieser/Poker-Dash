import datetime
import numpy as np
import pandas as pd
from src.objects import Game, Player, PlayerGroup, GameGroup
from src.rating import get_rating_arr_for_game, get_game_rating
from typing import List


def get_games(logs: np.ndarray) -> List[Game]:
    """Takes in the main logs_np array and produces a List of all Game
    objects which can be made from the Logs data.
    
    Args:
        logs (np.ndarray): _description_
        
    Returns:
        List[Game]: _description_
    """
    game_dates = np.unique(logs[:,1])
    n_games = len(game_dates)
    n_rows = len(logs)
    
    game_objs = []
    for i in range(n_games):
        date = game_dates[i]
        tmp_game_logs = []
        
        for j in range(n_rows):
            if logs[j,1] == date: tmp_game_logs.append(logs[j])
        
        # Create Game object
        game_logs_np = np.array(tmp_game_logs)
        game_objs.append(Game(
            logs=game_logs_np,
            game_num=i+1,
            date=date,
        ))
    
    return game_objs
    
def get_players(logs: np.ndarray) -> List[Player]:
    """Takes in the main logs_np array and produces a List of all Player
    objects which can be made from the Logs data.
    
    Args:
        logs (np.ndarray): _description_
        
    Returns:
        List[Player]: _description_
    """
    game_names = np.unique(logs[:,0])
    n_players = len(game_names)
    n_rows = len(logs)
    
    player_objs = []
    for i in range(n_players):
        player = game_names[i]
        tmp_player_logs = []
        
        for j in range(n_rows):
            if logs[j,0] == player: tmp_player_logs.append(logs[j])
        
        # Create Player object
        player_logs_np = np.array(tmp_player_logs)
        player_objs.append(Player(
            logs=player_logs_np,
            name=player,
        ))
    
    return player_objs

def get_player_ratings(logs: np.ndarray):
    rating_dict = {"date": datetime.date(2023, 2, 8)}
    game_numbers = {}
    game_names = np.unique(logs[:,0])
    n_players = len(game_names)
    for i in range(n_players):
        rating_dict.update({game_names[i]: 1000})
        game_numbers.update({game_names[i]: 0})
    
    game_dates = np.unique(logs[:,1])
    n_games = len(game_dates)
    n_rows = len(logs)
    rating_objs = [rating_dict]
    for i in range(n_games):
        tmp_game_log = [] # [datetime, ...[...{name, net}]]
        for j in range(n_rows):
            if logs[j,1] == game_dates[i]: tmp_game_log.append(logs[j]) 
        rating_arr = get_rating_arr_for_game(tmp_game_log)
        rating_after_game = get_game_rating(rating_arr, rating_objs[-1].copy(), game_numbers, game_dates[i])
        rating_objs.append(rating_after_game)
    return [rating_objs,game_numbers]
    

def get_player_group(players: List[Player]):
    """_summary_

    Args:
        players (List[Player]): _description_
    """
    pass


def get_game_group(games: List[Game]):
    """_summary_

    Args:
        games (List[Games]): _description_
    """
    pass