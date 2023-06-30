import tomllib
from src.collection import get_sheet
from src.processing import process
from src.streamlit import make_gui


# Load environment variables
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
    
    
def main():
    SHEETS_ID = config.get('SHEETS_ID')
    LOG_SHEET_NAME = config.get('LOG_SHEET_NAME')
    
    log_df = get_sheet(SHEETS_ID, LOG_SHEET_NAME)
    
    #import ipdb; ipdb.set_trace()
    
    log_np = log_df.to_numpy()
    
    make_gui(log_df)
    
    
    
    
    
if __name__=="__main__":
    main()