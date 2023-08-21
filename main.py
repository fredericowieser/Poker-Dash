import tomli
from src.collection import get_sheet
from src.processing import get_games, get_game_group, get_players, get_player_group
from src.streamlit import make_gui


# Load environment variables
with open("config.toml", "rb") as f:
    config = tomli.load(f)
    
    
def main():
    SHEETS_ID = config.get('SHEETS_ID')
    LOG_SHEET_NAME = config.get('LOG_SHEET_NAME')
    
    logs_df = get_sheet(SHEETS_ID, LOG_SHEET_NAME)
    
    # Numpy Log Index for logs_np:
    # - logs[:,0] -> Name
    # - logs[:,1] -> Date
    # - logs[:,2] -> No. of Buy Ins
    # - logs[:,3] -> Ending Pot
    # - logs[:,4] -> Points in 1 Buy-In
    # - logs[:,5] -> Value of 1 Point
    
    logs_np = logs_df.to_numpy()
    games = get_games(logs_np)
    players = get_players(logs_np)
    
    # Make the Guests and Regulars PlayerGroups for tab:
    # A 'Guest' is defined as being someone who has
    # played less than 4 games.
    # guests = []
    # regulars = []
    # for player in players:
    #     if player.n_games < 4: 
    #         pass
    
    # Make Player groups based on the player.group attributes
    # groups = []
    # for player in players:
    #     if not player.group == 'SOLO':
    #         if player.group in groups:
    #             pass
         
    # Make Past N Game Averages
    # for 
    
    # Make Overall GameGroup Object
    # aggregate = get_game_group(games)
    
    make_gui(logs_df, players, games)
    
    
    
    
    
if __name__=="__main__":
    main()