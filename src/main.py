import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_csv('data/players.csv')
df['win_rate'] = df['matches_won'] / df['matches_played']
seasonal_df = pd.read_csv('data/players_season.csv')
seasonal_df['win_rate'] = seasonal_df['matches_won'] / seasonal_df['matches_played']

# name,id,matches_played,matches_won,matches_lost,player_kills_kda,player_kills_kills,player_kills_deaths,player_kills_assists,farming_gpm,farming_gold,farming_minion_damage,farming_minion_kills,damage_player,damage_team_healing,damage_self_healing,damage_inhand,damage_mitigated,damage_taken

rename_dic = {  'name': 'Player name',
                'matches_played': 'Matches played',
                'matches_won': 'Matches won',
                'matches_lost': 'Matches lost',
                'player_kills_kda': 'KDA',
                'player_kills_kills': 'kills',
                'player_kills_deaths': 'deaths',
                'player_kills_assists': 'assists',
                'farming_gpm': 'GPM',
                'farming_gold': 'Gold',
                'farming_minion_damage': 'Minion damage',
                'farming_minion_kills': 'Minion kills',
                'damage_player': 'Player damage',
                'damage_team_healing': 'Team healing',
                'damage_self_healing': 'Self healing',
                'damage_inhand': 'Inhand damage',
                'damage_mitigated': 'Mitigated damage',
                'damage_taken': 'Damage taken',
                'win_rate': 'Win rate'
                }

st.title('SMITE: Smoteros players stats')


match_columns = ['matches_played', 'matches_won', 'matches_lost', 'win_rate']
kda_columns = ['player_kills_kda', 'player_kills_kills', 'player_kills_deaths', 'player_kills_assists']
farming_columns = ['farming_gpm', 'farming_gold', 'farming_minion_damage', 'farming_minion_kills']
damage_columns = ['damage_player', 'damage_team_healing', 'damage_self_healing', 'damage_inhand', 'damage_mitigated', 'damage_taken']

grids = {
    'Matches ⚔️': match_columns,
    'KDA 💀': kda_columns,
    'Farming 🧑‍🌾': farming_columns,
    'Damage 🩸': damage_columns
}

for grid in grids:
    st.subheader(grid)
    st.write(df[['name'] + grids[grid]].rename(columns=rename_dic).set_index(rename_dic['name']), hide_index=True)


    stat = st.selectbox('Select a stat', grids[grid], format_func=lambda x: rename_dic[x])

    temp_df = seasonal_df[['name', 'season', stat]].groupby(['season', 'name']).sum().unstack().fillna(0)
    #flatten the columns
    temp_df.columns = temp_df.columns.get_level_values(1)
    st.line_chart(temp_df)