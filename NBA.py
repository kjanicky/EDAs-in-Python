import pandas as pd
import matplotlib.pyplot as plt
import numpy as numpy

NBA = pd.DataFrame(pd.read_csv("all_seasons.csv"))
print(NBA.shape)
print(NBA.isnull().sum()) #checking the shape of dataframe
print(NBA.dtypes) #checking if there is some variables that I have to change their data type
def undraft_number(draft_number):
    undraft_number_dict = {
        'Undrafted': '61',
        '0': '61',
    }
    try:
        return undraft_number_dict[draft_number]
    except:
        return draft_number
NBA.draft_number = NBA.draft_number.apply(undraft_number) #cleaning the draft_number setting number to 61 if player was undrafted
NBA['draft_number'] = NBA.draft_number.astype('int64') # changing draft_number to numeric
NBA.rename(columns = {'player_height':'height', 'player_weight':'weight', 
                     'pts':'avg_pts', 'reb':'avg_reb', 'ast':'avg_ast','gp':'games_played'}, inplace = True) #renaming columns because they are averages of player's pts,reb,assists
NBA['height_in_feets'] = (NBA['height'] / 30.28).round(1)
NBA['season_start'] = NBA['season'].str[:4]
NBA['season_end'] =  NBA['season'].str[:2] + NBA['season'].str[5:] #adding columns for easier subseting

average_height = NBA['height'].mean().round(2)
median_height = NBA['height'].median()
print(f'The average height is {average_height} and median height is {median_height}')

### how height impacts draft number
draft_and_height = NBA[['height','draft_number']] \
    .groupby('draft_number') \
    .mean()\
    .sort_values('draft_number',ascending=True)\
    .head(20)\
    .round(2)
    
draft_and_height.index.name = 'Position in Draft'    
print(draft_and_height)
plt.plot(draft_and_height['height'],color = 'black')
plt.xlabel("Draft Position")
plt.ylabel("Average height in cm ")
plt.title('Draft position by Height')
plt.xticks(ticks=range(0, len(draft_and_height), 5))
plt.show()

height_across_seasons = NBA[['height','season']]\
     .groupby('season')\
     .mean()\
     .sort_values('season',ascending=True)\
     .round(2)

print(height_across_seasons)
plt.figure(figsize=(10,6))
plt.plot(height_across_seasons,color = 'green')
plt.xlabel('Season')
plt.ylabel('Average Height in cm')
plt.title('Height across the seasons')
plt.xticks(rotation = 45)
plt.show()

 

small_players = NBA[NBA['height'] <= 207.2]
big_players = NBA[NBA['height'] > 207.2]
big_players_pts_by_season = big_players[['avg_pts','season']] \
     .groupby('season')\
     .mean()\
     .sort_values('season',ascending=True)\
     .round(1)\
     
small_players_pts_by_season = small_players[['avg_pts','season']] \
     .groupby('season')\
     .mean()\
     .sort_values('season',ascending=True)\
     .round(1)\

plt.figure(figsize=(9,7))
plt.plot(big_players_pts_by_season['avg_pts'],color = 'green',label='above 6"8')
plt.plot(small_players_pts_by_season['avg_pts'],color = 'blue',label='6"8 and below')
plt.ylabel('Points per Game')
plt.xlabel('Season')
plt.title('PPG under 6"8 vs above 6"8')
plt.legend()
plt.xticks(rotation = 45)
plt.show()                        

valid_small_players = small_players[small_players['games_played'] >= 65] #subseting players that played 80% games 
valid_big_players = big_players[big_players['games_played'] >= 65]

top25_net_rating_small_players = valid_small_players[['player_name','height','net_rating','season']]\
       .sort_values('net_rating',ascending=False)\
       .head(10)

print(top25_net_rating_small_players)

top25_net_rating_big_players = valid_big_players[['player_name','height','net_rating','season']]\
        .sort_values('net_rating',ascending=False)\
        .head(10)

print(top25_net_rating_big_players)

net_rating_big = valid_big_players[['season','net_rating']].groupby('season')\
     .mean()\
     .sort_values('season',ascending=True)\
     .round(1)
net_rating_small = valid_small_players[['season','net_rating']].groupby('season')\
     .mean()\
     .sort_values('season',ascending=True)\
     .round(1)

plt.figure(figsize=(9,7))
plt.plot(net_rating_big['net_rating'],color='green',label='above 6"8')
plt.plot(net_rating_small['net_rating'],color='blue',label='6"8 and below')
plt.xlabel('Season')
plt.ylabel('Average Net Rating')
plt.title('Big vs Small player average Net Rating')
plt.legend()
plt.xticks(rotation = 45)
plt.show()
# comparing 00s and 10s
#NBA_00s = NBA[(NBA['season_start'] >= '2000') & (NBA['season_end'] <= '2010')]
#NBA_10s = NBA[(NBA['season_start'] >= '2010') & (NBA['season_end'] <= '2020')] #creating dataframe for players in 00s and 10s
#plt.hist(NBA_00s['avg_pts'],alpha = 0.5,bins = 10,color = 'green') ### creating comparison beetween 00s and 10s in points scored per game by players
#plt.hist(NBA_10s['avg_pts'],alpha = 0.3,bins = 10,color = 'blue') 
#plt.title('Points Per Game 00s vs 10s')    
#plt.xlabel('Points per Game')
#plt.ylabel('Number of Players') 
#plt.legend(['2000s','2010s'])                                        
#plt.show()
#creating height comparisons beetween 00s and 10s
#plt.hist(NBA_00s['height'],alpha = 0.4, bins = 10, color = 'blue')
#plt.hist(NBA_10s['height'],alpha = 0.6, bins = 10,color = 'red')
#plt.title('Height Across the Decades')
#plt.xlabel('Height (cm)')
#plt.ylabel('Number of Players')
#plt.legend(['2000s','2010s'])                                         
#plt.show()