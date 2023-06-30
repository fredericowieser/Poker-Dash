import pandas as pd


def col_gbp_to_float(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    for i in range(df.shape[0]):
        value = df.at[i, col_name].replace('£', '')
        df.at[i, col_name] = float(value)
    return df


def hash_player_col(df: pd.DataFrame) -> pd.DataFrame:
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
    

def get_sheet(sheets_id: str, sheet_name: str) -> pd.DataFrame:
    url = f'https://docs.google.com/spreadsheets/d/{sheets_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    df = col_gbp_to_float(df, 'Net (Sterling)')
    df = col_gbp_to_float(df, 'Value of 1 Point')
    df = hash_player_col(df)
    
    #import ipdb; ipdb.set_trace()
    
    return df