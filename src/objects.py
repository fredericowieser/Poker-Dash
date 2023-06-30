from dataclasses import dataclass
from typing import List

import pandas as pd
import numpy as np

@dataclass
class Game:
    data : pd.Dataframe
    data_np : np.array
    
    
@dataclass
class Player:

@dataclass
class PlayerGroups:
    players: List[Player]
    average_gbp_per_cap: float = 1
        
    
@dataclass
class GameGroups:
    """
    GameGroups take in data from certain games which we choose to make this
    larger structure. With this data we then instantiate other classes above.
    Many of the following classes will be created:
    
    Player -> Single Player Data and Stats
    Game -> Single Game Data and Stats
    PlayerGroup -> Many Groups of Players with Data and Stats
    """
    
    data : pd.Dataframe
    data_np : np.array
    
    
