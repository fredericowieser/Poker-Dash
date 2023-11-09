from dataclasses import dataclass
from typing import List
from src.lib import avg_gbp_in_per_cap, color_red_green_nums
from src.colorhash import ColorHash
from src.lib import encode_str_2_rgb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# import squarify
import datetime

# Graph Running Net vs Time vertical height
Y_LIMS = 45


@dataclass
class Game:
    logs: np.ndarray
    game_num: int
    date: str  # Reformat Date

    def __post_init__(self):
        if self.logs is not None:
            self.name: str = f"Game {self.game_num}, {self.date.strftime('%d %B %Y')}"
            self.points_in_buyins: int = self.logs[:, 4][0]
            self.value_of_points: float = self.logs[:, 5][0]
            self.n_players: int = len(self.logs)
            self.n_buyins: float = np.sum(self.logs[:, 2])
            self.invested_cash: float = (
                self.n_buyins * self.points_in_buyins * self.value_of_points
            )

            # Net
            self.net: np.ndarray = self.logs[:, 5][0] * (
                self.logs[:, 3] - self.logs[:, 4][0] * self.logs[:, 2]
            )

            # Change Date format

            self.datestr = datetime.datetime.strptime(
                str(self.date), "%Y-%m-%d"
            ).strftime("%d %b %y")

            # import ipdb; ipdb.set_trace()

    @property
    def scoreboard_df(self) -> pd.DataFrame:
        df = pd.DataFrame(
            data=["{0:.2f}".format(net) for net in self.net],
            index=self.logs[:, 0],
            columns=["Net (£GBP)"],
        )

        df = df.style.applymap(color_red_green_nums)

        return df

    @property
    def winners(self) -> np.ndarray:
        return

    @property
    def losers(self) -> np.ndarray:
        return

    @property
    def pot_tree_map(self):
        pass

    @property
    def stats_df(self) -> pd.DataFrame:
        data = [
            ["No. Players", "{0:.0f}".format(self.n_players)],
            ["Points in 1 Buy-In", "{0:.0f}".format(self.points_in_buyins)],
            ["Value of 1 Point", "{0:.2f}".format(self.value_of_points)],
            ["Total Buy-Ins", "{0:.0f}".format(self.n_buyins)],
            ["Total Cash in Game", "{0:.0f}".format(self.invested_cash)],
        ]

        df = pd.DataFrame(data, columns=["Stat", "Value"])
        df = df.set_index(df.columns[0])
        # df = df.style.applymap(color_red_green_nums)

        return df


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
                self.logs[:, 3] - self.logs[:, 2] * self.logs[:, 4]
            ) * self.logs[:, 5]
            self.avg_net_cash: float = np.average(self.np_net_cash)
            self.std_dev_net_cash: float = np.std(self.np_net_cash)
            self.avg_win: float = np.average(self.np_net_cash[(self.np_net_cash > 0)])
            self.avg_loss: float = np.average(self.np_net_cash[(self.np_net_cash < 0)])
            self.n_wins: int = len(self.np_net_cash[(self.np_net_cash > 0)])
            self.n_losses: int = len(self.np_net_cash[(self.np_net_cash < 0)])
            self.win_loss_ratio: dict = {"W": self.n_wins, "L": self.n_losses}
            self.avg_n_buyins: float = np.average(self.logs[:, 2])
            self.std_dev_n_buyins: float = np.std(self.logs[:, 2])
            self.avg_net_w_multi_buyin: float = np.average(
                self.np_net_cash[(self.logs[:, 2] > 1)]
            )
            self.dates: np.ndarray = self.logs[:, 1]

            self.current_net = np.sum(self.np_net_cash)

            self.points_in_buyins: int = self.logs[:, 4][0]
            self.value_of_points: float = self.logs[:, 5][0]
            self.n_buyins: float = np.sum(self.logs[:, 2])
            self.invested_cash: float = (
                self.n_buyins * self.points_in_buyins * self.value_of_points
            )

    @property
    def running_net(self) -> np.ndarray:
        l = len(self.np_net_cash)
        rolling_cash = np.zeros(l)
        rolling_cash[0] = self.np_net_cash[0]
        for i in range(1, l):
            rolling_cash[i] = rolling_cash[i - 1] + self.np_net_cash[i]

        # Create Max/Min Running Net
        self.max_rn = np.max(rolling_cash)
        self.min_rn = np.min(rolling_cash)

        return rolling_cash

    @property
    def st_cash_v_time(self) -> np.ndarray:
        # TODO:
        # - Make grid lines more gray and dimmer
        # - Add highlighted are underneath curve to x axis
        # -
        fig, ax = plt.subplots()
        ax.plot(self.dates, self.running_net, "o-", label="Running")
        ax.set_xlabel("Dates")  # Add an x-label to the axes.
        ax.set_ylabel("Cash (£GBP)")  # Add a y-label to the axes.
        ax.set_ylim([-Y_LIMS, Y_LIMS])
        ax.tick_params(axis="x", labelrotation=45)
        ax.set_title(f"Running Net for {self.name}")  # Add a title to the axes.
        ax.grid()
        return fig

    def net_last_n_games(self, n: int) -> np.ndarray:
        l = len(self.np_net_cash)
        if n <= l:
            return self.np_net_cash[self.n_games - n :]
        else:
            return np.nan

    @property
    def stats_df(self) -> pd.DataFrame:
        data = [
            ["No. Games", "{0:.0f}".format(self.n_games)],
            ["No. Wins", "{0:.0f}".format(self.n_wins)],
            ["No. Losses", "{0:.0f}".format(self.n_losses)],
            ["First Game", f"{self.dates[0]}"],
            ["Most Recent Game", f"{self.dates[-1]}"],
            ["Avg. No. Buy-Ins", "{0:.2f}".format(self.avg_n_buyins)],
        ]

        df = pd.DataFrame(data, columns=["Stat", "Value"])
        df = df.set_index(df.columns[0])
        # df = df.style.applymap(color_red_green_nums)

        return df

    @property
    def net_cash_df(self) -> pd.DataFrame:
        data = [
            ["Current Net", "{0:.2f}".format(float(self.current_net))],
            ["Avg. Weekly Net (AWN)", "{0:.2f}".format(self.avg_net_cash)],
            ["St.Dev. Weekly Net", "{0:.2f}".format(self.std_dev_net_cash)],
            ["Biggest Win", "{0:.2f}".format(np.max(self.np_net_cash))],
            ["Biggest Loss", "{0:.2f}".format(np.min(self.np_net_cash))],
            ["AWN Winning", "{0:.2f}".format(self.avg_win)],
            ["AWN Lossing", "{0:.2f}".format(self.avg_loss)],
            ["AWN w/ Extra Buy-Ins", "{0:.2f}".format(self.avg_net_w_multi_buyin)],
            [
                "AWN Last 3 Games",
                "{0:.2f}".format(np.average(self.net_last_n_games(n=3))),
            ],
            [
                "AWN Last 5 Games",
                "{0:.2f}".format(np.average(self.net_last_n_games(n=5))),
            ],
            [
                "AWN Last 8 Games",
                "{0:.2f}".format(np.average(self.net_last_n_games(n=8))),
            ],
        ]

        df = pd.DataFrame(data, columns=["Weekly Net", "Cash (£GBP)"])
        df = df.set_index(df.columns[0])
        df = df.style.applymap(color_red_green_nums)

        return df

    @property
    def color(self) -> str:
        # chex = ColorHash(self.name).hex
        # crgb = ( int(chex[1:3], 16), int(chex[3:5], 16), int(chex[5:], 16) )
        # crgb_anti = ( abs(crgb[i]-255) for i in range(len(crgb)) )
        # chex_anti = '#%02x%02x%02x' % tuple(crgb_anti)

        # if sum(crgb) % 2 == 0:
        #     return chex
        # else:
        #     return chex_anti
        return encode_str_2_rgb(self.name)


class PlayerRating:
    def __init__(self, name):
        self.name = name
        self.rating_data_date = []
        self.rating_data_rating = []
        self.n_games = 0

    def new_game(self, date, net):
        self.n_games += 1
        self.new_game_data_date = date
        self.new_game_data_rating = self.current_rating()
        self.new_game_data_net = net

    def current_rating(self):
        return self.rating_data_rating[-1] if len(self.rating_data_rating) > 0 else 1000

    def set_new_rating(self):
        self.rating_data_date.append(self.new_game_data_date)
        self.rating_data_rating.append(self.new_game_data_rating)


class GameRating:
    def __init__(self, player, player_rating):
        self.name = player[0]
        self.net = self.calc_player_net(player)
        self.player_rating = player_rating

    def calc_player_net(_, player):
        buy_ins, end_game, base_chips, chip_value = player[-4:]
        return round(chip_value * (end_game - (base_chips * buy_ins)), 2)


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
                tmp_players.append([player.name, f"£{player.avg_net_w_multi_buyin}"])

        return np.array(tmp_players)

    @property
    def players_w_greater_l(self) -> np.ndarray:
        tmp_players = []
        for player in self.players:
            if player.win_loss_ratio["L"] == 0:
                [player.name, np.inf]
            elif player.win_loss_ratio["W"] > player.win_loss_ratio["L"]:
                [
                    player.name,
                    player.win_loss_ratio["W"] / player.win_loss_ratio["L"],
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
        pass  # self
