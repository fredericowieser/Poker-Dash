from dataclasses import dataclass
from typing import List
from src.lib import avg_gbp_in_per_cap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
   

@dataclass
class Game:
    logs: np.ndarray
    game_num: int
    date: str
    
    def __post_init__(self):
        if self.logs is not None:
            self.name: str = (
                f"Game {self.game_num}, {self.date.strftime('%d %B %Y')}"
            )
            self.points_in_buyins: int = self.logs[:,4][0]
            self.value_of_points: float = self.logs[:,5][0]
            self.n_players: int = len(self.logs)
            self.n_buyins: float = np.sum(self.logs[:,2])
            self.invested_cash: float = (
                self.n_buyins *
                self.points_in_buyins *
                self.value_of_points
            )

    @property
    def scoreboard_df(self) -> pd.DataFrame:
        return
    
    @property
    def winners(self) -> np.ndarray:
        return
        
    @property
    def losers(self) -> np.ndarray:
        return
    
    
@dataclass
class Player:
    logs: np.ndarray
    name: str
    # TODO: group: str
    
    def __post_init__(self):
        if self.logs is not None:
            self.n_games: int = len(self.logs)
            # self.avg_percent_of_net_poins: int = 
            # self.std_dev_net_points: float
            self.np_net_cash: np.ndarray = (
                (self.logs[:,3]-self.logs[:,2]*self.logs[:,4])*self.logs[:,5]
            )
            self.avg_net_cash: float = np.average(self.np_net_cash)
            self.std_dev_net_cash: float = np.std(self.np_net_cash)
            self.avg_win: float = np.average(self.np_net_cash[(self.np_net_cash > 0)])
            self.avg_loss: float = np.average(self.np_net_cash[(self.np_net_cash < 0)])
            self.n_wins: int = len(self.np_net_cash[(self.np_net_cash > 0)])
            self.n_losses: int = len(self.np_net_cash[(self.np_net_cash < 0)])
            self.win_loss_ratio: dict = {"W": self.n_wins, "L": self.n_losses}
            self.avg_n_buyins: float = np.average(self.logs[:,2])
            self.std_dev_n_buyins: float = np.std(self.logs[:,2])
            self.avg_net_w_multi_buyin: float = (
                np.average(self.np_net_cash[(self.logs[:,2] > 1)])
            )
            self.dates: np.ndarray = self.logs[:,1]
    
    @property
    def running_net(self) -> np.ndarray:
        # TODO: Fix bug in calculating running_net which seems to be wrong rn
        l = len(self.np_net_cash)
        rolling_cash = np.zeros(l)
        rolling_cash[0] = self.np_net_cash[0]
        for i in range(1, l):
            rolling_cash[i] = (
                rolling_cash[i-1] + self.np_net_cash[i]
            )
        #import ipdb; ipdb.set_trace()
        return rolling_cash
    
    @property
    def st_cash_v_time(self) -> np.ndarray:       
        fig, ax = plt.subplots()
        ax.plot(self.dates, self.running_net, 'o-', label='Running')
        ax.set_xlabel('Dates (DD-MM-YYYY)')  # Add an x-label to the axes.
        ax.set_ylabel('Cash (£GBP)')  # Add a y-label to the axes.
        ax.tick_params(axis='x', labelrotation=45)
        ax.set_title(f"Running Net for {self.name}")  # Add a title to the axes.
        ax.grid()
        return fig
    
    @property
    def stats_df(self) -> pd.DataFrame:
        def color_red_green_nums(val):
            if type(val) == str:
                color = ''
                try:
                    val = float(val)
                    if val < 0: color = 'red'
                    elif val > 0: color = 'green'
                    return 'background-color: %s' % color
                except:
                    return 'background-color: %s' % color
        
        data = [
            ["No, Games", '{0:.0f}'.format(self.n_games)],
            ["Avg. Weekly Net (£GBP)", '{0:.2f}'.format(self.avg_net_cash)],
            ["Biggest Win (£GBP)", '{0:.2f}'.format(np.max(self.np_net_cash))],
            ["Biggest Loss (£GBP)", '{0:.2f}'.format(np.min(self.np_net_cash))],
        ]
        
        df = pd.DataFrame(data, columns=['Stat', 'Value'])
        df = df.set_index(df.columns[0])
        s = df.style.applymap(color_red_green_nums)
        
        return s

@dataclass
class PlayerGroup:
    name: str
    players: List[Player]
    average_gbp_per_cap: float
    
    @property
    def players_w_avg_net_w_multi_buyin(self) -> np.ndarray:
        """Gives back a an arry with the cash values and names of all players
        in this group which have negative net cash averages when they buy back.
        """
        tmp_players = []
        for player in self.players:
            if player.avg_net_w_multi_buyin < 0:
                tmp_players.append(
                    [player.name, f"£{player.avg_net_w_multi_buyin}"]
                )
                
        return np.array(tmp_players)
    
    @property
    def players_w_greater_l(self) -> np.ndarray:
        tmp_players = []
        for player in self.players:
            if player.win_loss_ratio['L'] == 0:
                [player.name, np.inf]
            elif player.win_loss_ratio['W'] > player.win_loss_ratio['L']:
                [
                    player.name,
                    player.win_loss_ratio['W']/player.win_loss_ratio['L'],
                ]
        
    
@dataclass
class GameGroup:
    """
    GameGroups take in data from certain games which we choose to make this
    larger structure. With this data we then instantiate other classes above.
    Many of the following classes will be created:
    """
    games: List[Game]
    
    @property
    def groups(self):
        pass #self
    
    
