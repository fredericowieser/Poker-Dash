import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go

def make_gui(df):
    
    # Add a title and intro text
    st.title('Poker Dashboard')
    st.text('This is a web app to allow exploration of our weekly Poker games, I hope you enjoy!')
    
    # Create a section for the dataframe header
    # st.header('Header of Dataframe')
    # st.write(df.head())
    
    names = get_player_names(df)
    player_logs = get_player_logs(df, names)
    figs = running_total(player_logs, names)
    
    st.plotly_chart(figs, theme="streamlit", use_container_width=True)


def get_player_names(df : pd.DataFrame) -> pd.DataFrame:
    names = df['Name'].unique()
    return names


def get_player_logs(df, names):
    """
    Returns a list of dates with the players corresponding
    game data where we have colums 'Name' and 'Sterling'
    """
    n = len(names)
    player_logs = []
    
    for i in range(n):
        player_log = df[df["Name"] == names[i]]
        player_log.index = range(len(player_log.index))
        player_logs.append(player_log)
        print(player_log.head)
        
    return player_logs


def running_total(player_logs, names):
    figs = []
    for i in range(len(player_logs)):
        player_log = player_logs[i]
        
        running_totals = []
        rt_temp = 0
        
        test = player_log["Net (Sterling)"]
        for j in range(player_log.shape[0]):
            temp = player_log.at[j, "Net (Sterling)"]
            rt_temp = rt_temp + temp
            running_totals.append(rt_temp)
            
        
        player_log.insert(1, 'Running Total', running_totals)                
        
        # Line plot of Apple stock price
        fig_temp = go.Scatter(
            x = player_log['Date'],
            y = player_log['Running Total'],
            #name = player_logs[i].at[0, 'Name'],
            name = names[i]
        )
        
        figs.append(fig_temp)
        
    return figs
        