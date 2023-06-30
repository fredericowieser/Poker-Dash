import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def make_gui(df):
    
    # Add a title and intro text
    st.title('Poker Dashboard')
    st.text('This is a web app to allow exploration of our weekly Poker games, I hope you enjoy!')
    
    # Create a section for the dataframe statistics
    st.header('Statistics of Dataframe')
    st.write(df.describe())
    
    # Create a section for the dataframe header
    st.header('Header of Dataframe')
    st.write(df.head())
