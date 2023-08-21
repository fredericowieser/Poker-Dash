import pandas as pd
from datetime import date


def col_gbp_to_float(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Transforms a column in df from being a string representation of the GBP 
    value into a float.

    Args:
        df (pd.DataFrame): _description_
        col_name (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    for i in range(df.shape[0]):
        value = df.at[i, col_name].replace('£', '')
        df.at[i, col_name] = float(value)
    return df

def col_datestr_to_dateobj(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Transforms a column in df from being a string representation of the date 
    value into a datetime object.

    Args:
        df (pd.DataFrame): _description_
        col_name (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    for i in range(df.shape[0]):
        value = df.at[i, col_name]
        ddmmyyyy = value.split('/')
        
        dd = int(value.split('/')[0])
        mm = int(value.split('/')[1])
        yyyy = int(f"20{value.split('/')[2]}")
                
        df.at[i, col_name] = date(yyyy, mm, dd)
    return df


def add_hash_player_col(df: pd.DataFrame) -> pd.DataFrame:
    names = df['Name'].unique()
    
    # Get name hashes
    players_hash = {}
    for name in names:
        players_hash[name] = hash(name)
    
    # Replace original names with hashes
    for i in range(df.shape[0]):
        name = df.at[i, 'Name']
        df.at[i, 'Name'] = players_hash[name]
    
    return df


def validate_logs_table(df: pd.DataFrame) -> pd.DataFrame:
    """Looks at the Dataframe created from our Google Sheet document and checks
    to see if the profit calculated on the sheet is the same as the profit 
    calculated by this Python program.
    
    We also check if the properties in certain games all match...
    - No name duplicates in one game (a game being all collected entries 1 day)
    - More than 1 player in a game
    - Profits - Losses = 0 in a game
    - 1 unique value for 'Points in 1 Buy-In' of a game
    - 1 unique value for 'Values of 1 Point' of a game
    
    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    
    
    
    
    
def clean_logs_table(df: pd.DataFrame) -> pd.DataFrame:
    """To clean our given table we are going to be removing all rows which are
    unnecessary for creating a full view of what happened in all the games.
    
    The unnecessary table columns for logs are...
    - 'Starting Pot'
    - 'Net (Points)'
    - 'Net (Sterling)' 

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    df = df.drop([
        'Starting Pot',
        'Net (Points)',
        'Net (Sterling)',
    ], axis=1)
    return df
    

def validate_logs_to_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """To checkif the aggregate
    """
    return None


def get_sheet(sheets_id: str, sheet_name: str) -> pd.DataFrame:
    url = f'https://docs.google.com/spreadsheets/d/{sheets_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    df = col_gbp_to_float(df, 'Net (Sterling)')
    df = col_gbp_to_float(df, 'Value of 1 Point')
    df = col_datestr_to_dateobj(df, 'Date')
    df = df.sort_values(by=['Date'])
    
    #validate_logs_table(df)
    #validate_logs_to_aggregate(df)
    #validate_logs_to_bonus(df)
    
    df = clean_logs_table(df)
    
    # TODO -> df = add_hash_player_col(df)
        
    return df