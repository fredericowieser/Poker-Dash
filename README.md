# Poker Dash

Online poker dashboard currently available here -> 
[Poker Dash Website](https://poker-dash-t579yhkzser.streamlit.app/)

This website features a statistical visualistion of the results of our ongoing poker nights. The project is currently under development, with the aim to transition to a visually lighter yet more comprehensive model.

**Under development :**
- Historical data interface to allow for broader queries of the data
- Combined graphs and tables on the Compare Player and Games tabs 
- Machine Learning based feature to predict player returns when the model is provided with a group of opponents

### Current Features
   - Home
      - graph showing the running totals; users can alter the time range and min number of games played
	      - This graph uses the following repo for a hashing function from a player's name to a unique colour:
	        [GitHub - dimostenis/color-hash-python: Generate deterministic color from any object](https://github.com/dimostenis/color-hash-python/tree/main)
      - player's leaderboard, featuring conditional formatting
   - Compare Players
      - users select players to analyse and compare stats, with the option of default player groups:
        - The Regulars (>3 games played)
        - The Guests (<3 games played)
      - table to show player stats, history, and more indepth values (e.g. likelihood of return on the second/third buy in)
      - graph to compare trajectories of players
  - Games
      - analyse individual games from the timeline


**General :**
 - Pandas have been used to create NumPy arrays and hash tables, then used to create the main objects
 - Graphing is achieved by Matplotlib and calculations with NumPy
 - Objects use NumPy for their definitions
