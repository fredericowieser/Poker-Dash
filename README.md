# Poker Dash

A online poker dashboard currently available here -> 
[Poker Dash Website](https://poker-dash-t579yhkzser.streamlit.app/)

This website features statistics and interesting visualistions for friends who take part in this poker game to see. 
This project will hopefully transition to something lighter very soon  and be faster with more features.
As of right now the main goal is to implement something which cna show us our historical data on an inteface which will allow for fairly comprehensive queries of the data.
With the hope in the future that we will implement some possiblt prediction features for player and player group running totals in the game.


 - [x] Use Pandas to create some basic numpy arrays and hash tables which will then be used to create the main objects.
 - [x] Convert all graphing to matplotlib and only use numpy for calculations.
 - [x] All objects only use numpy for their definitions.
 - [x] Figure out way to convert Dates to Game numbers and have a hash table for this
 - [ ] Create interface with sidebar as follows being the maind tabs
   - [x] Home, where you select the timeline you want to look at and then have the running total graph aswell as the main leaderboard with conditional formatting, as well as the Player group leaderboard.
   - [x] Players, where we have a checkbox and can then see individual player stats and and history as well as some of the more indepth values (e.g. likelihood of return on the second/third buy in)
   - [ ] Groups of Players, this is the same as players except we look at the group.
     - [ ] Hopefully the functionality will also be there to create your own group and look at that data.
     - [ ] Some of the default Player Groups would be The Regulars which would be some number of games or more have to be played to be in. The guests which is the same but on the other side of that number.
   - [x] Games, individual Games from the timeline selected at the main tab.
   - [x] Comparison, between players and or playersgroups with a graph showing those two objects with the current average of all players