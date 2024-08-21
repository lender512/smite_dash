import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_csv('data/raw/players.csv')

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
                'damage_taken': 'Damage taken'}

st.title('SMITE: Smoteros players stats')

match_columns = ['matches_played', 'matches_won', 'matches_lost']
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
    st.write(df[['name'] + grids[grid]].rename(columns=rename_dic), hide_index=True)
