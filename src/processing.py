import numpy as np
import pandas as pd

def process(df: pd.DataFrame) -> np.ndarray:
    """
    Takes in the a GameGroup DataFrame and creates
    the base objects we want for our dashboard to 
    display by default. These will likely be more
    general stats and information about the poker
    games and performance.
    """
    