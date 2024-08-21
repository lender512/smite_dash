from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep
import pandas as pd

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

    def get_player(self, player):
        self.driver.get(
            f'https://smite.guru/profile/{player.id}_{player.name}')
        sleep(5)

        # find class="widget tsw"
        stats = self.driver.find_element(
            By.CLASS_NAME, 'widget.tsw').text.split('\n')
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
    
    for player in players:
        scraper.get_player(player)
        
    df = load_data(players)
    df.to_csv(f'{data_path}/players.csv', index=False)
        
    
    
