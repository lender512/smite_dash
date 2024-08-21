from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import pandas as pd
from tqdm import tqdm

data_path = 'data/raw'

class Player:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.matches_played = None
        self.matches_won = None
        self.matches_lost = None
        self.player_kills_kda = None
        self.player_kills_kills = None
        self.player_kills_deaths = None
        self.player_kills_assists = None
        self.farming_gpm = None
        self.farming_gold = None
        self.farming_minion_damage = None
        self.farming_minion_kills = None
        self.damage_player = None
        self.damage_team_healing = None
        self.damage_self_healing = None
        self.damage_inhand = None
        self.damage_mitigated = None
        self.damage_taken = None

    def __str__(self):
        return f'{self.name} {self.id}'

    def __repr__(self):
        return f'{self.name} {self.id}'
    
    def to_list(self):
        return [value for value in self.__dict__.values()]


class scraper:
    def __init__(self):
        user_home_dir = os.path.expanduser("~")
        chrome_binary_path = os.path.join(
            user_home_dir, "chrome-linux64", "chrome")
        chromedriver_path = os.path.join(
            user_home_dir, "chromedriver-linux64", "chromedriver")
        options = Options()
        options.binary_location = chrome_binary_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")

        options.add_argument("--remote-debugging-port=9222")  # this
        options.add_argument("--disable-dev-shm-using")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        service = Service(chromedriver_path)

        self.driver = webdriver.Chrome(options=options, service=service)

    def get_player(self, player, season=None):
        wait = WebDriverWait(self.driver, 10)
        url = f'https://smite.guru/profile/{player.id}_{player.name}'
        self.driver.get(url)
        sleep(2)
        if season:
            #find dd with text "Season {season}"
            season_dd = wait.until(lambda driver: driver.find_element(By.XPATH, f"//a[contains(text(), 'Season {season}')]"))
            self.driver.execute_script("arguments[0].scrollIntoView();", season_dd)
            season_dd.click()
            sleep(2)
        try:
            stats = wait.until(lambda driver: driver.find_element(By.CLASS_NAME, 'widget.tsw')).text.split('\n')
        except TimeoutException:
            print(f'Error getting player {player.name} {player.id}')
            return
        ignore = ['PLAYER STATS', 'Totals']
        stats = [x for x in stats if x not in ignore]
        stats = [x.replace('GPM', 'gpm').replace('KDA', 'kda') for x in stats]
        for i in range(len(stats)):
            # check if all uppercase
            if stats[i][-1].isupper():
                subset = stats[i]
                continue
            elif stats[i][0].isnumeric():
                continue
            setattr(
                player, f"{subset.lower().replace(' ', '_')}_{stats[i].lower().replace(' ', '_')}", float(stats[i+1].replace(',', '')))
        # return player

    def close(self):
        self.driver.quit()

    def __del__(self):
        self.close()

def load_data(players):
    df = pd.DataFrame(columns=players[0].__dict__.keys())
    for player in players:
        df = pd.concat([df, pd.DataFrame([player.to_list()], columns=player.__dict__.keys())])
    return df

if __name__ == '__main__':
    players = [Player('Nutax',      '6776734'),
               Player('Juanman',    '10059110'),
               Player('lender1997', '11678813'),
               Player('DaNeis',     '6910477'),
               Player('EpZero',     '6418704')]
    scraper = scraper()
    
    # for player in players:
    #     scraper.get_player(player)
    # df = load_data(players)
    # df.to_csv(f'{data_path}/players.csv', index=False)
    
    seasons = range(3, 12)
    season_df = pd.DataFrame()
    for season in tqdm(seasons):
        for player in tqdm(players):
            scraper.get_player(player, season)
        temp_df = load_data(players)
        temp_df['season'] = season
        season_df = pd.concat([season_df, temp_df])
        
    season_df.to_csv(f'{data_path}/players_season.csv', index=False)
        
    
    
