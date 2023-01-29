import datetime
import os
import time
import requests
from bs4 import BeautifulSoup
import tweepy
import shutil
import random
from icrawler.builtin import GoogleImageCrawler
import config

# TWEEPY
# ----------------------------------------------------------------
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)
# ----------------------------------------------------------------

response = requests.get('https://www.cbssports.com/nba/stats/leaders/live/?sortcol=pts&sortdir=descending')

soup = BeautifulSoup(response.text, "html.parser")

player_list = soup.find_all("span", {"class": "CellPlayerName--long"})
players_list = [player.text.split('\n')[0] for player in player_list]

score_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
scores_list = [score.text.split('\n')[7].strip(' ') for score in score_list]

minute_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
minutes_list = [score.text.split('\n')[6].strip(' ') for score in score_list]

rebound_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
rebounds_list = [score.text.split('\n')[8].strip(' ') for score in score_list]

assist_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
assists_list = [score.text.split('\n')[9].strip(' ') for score in score_list]

game_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
games_list = [score.text.split('\n')[4].strip(' ') for score in score_list]

steal_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
steals_list = [score.text.split('\n')[11].strip(' ') for score in score_list]

block_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
blocks_list = [score.text.split('\n')[12].strip(' ') for score in score_list]

turnover_list = soup.find_all('tr', {"class": 'TableBase-bodyTr'})
turnovers_list = [score.text.split('\n')[13].strip(' ') for score in score_list]

res = []
j = 0
for i in range(len(scores_list)):
    if float(scores_list[i]) >= 27:
        res.append([players_list[i]])
        res[j].append(scores_list[i])
        res[j].append(minutes_list[i])
        res[j].append(rebounds_list[i])
        res[j].append(assists_list[i])
        res[j].append(games_list[i])
        res[j].append(steals_list[i])
        res[j].append(blocks_list[i])
        res[j].append(turnovers_list[i])
        j += 1

def nba_scores():
    for data in range(len(res)):
        hashtag = res[data][0].replace(' ', '').replace("'", "")
        store = f"#{hashtag} has scored {int(float(res[data][1]))} points, {res[data][3]} rebounds, {res[data][4]} assists, with {res[data][6]} steals, {res[data][7]} blocks, and {res[data][8]} turnovers within {res[data][2]} Minutes today."
        if '-' in res[data][5]:
            if os.path.exists('nba_scores.txt'):
                nba_file = open("nba_scores.txt", "r")
            else:
                nba_file = open("nba_scores.txt", "w")
                nba_file = open("nba_scores.txt", "r")
            if store in nba_file.read():
                continue
            else:
                print(store)
                google_crawler = GoogleImageCrawler(storage={'root_dir': 'images'})
                google_crawler.crawl(keyword=f'{res[data][0]} nba', max_num=5)
                files = os.listdir('images')
                index = random.randint(0, len(files) - 1)
                fil = (files[index])
                media = api.media_upload(f'images/{fil}')
                api.update_status(status=store, media_ids=[media.media_id_string])
                nba_file = open("nba_scores.txt", "a")
                nba_file.write(store + '\n')
                shutil.rmtree('images')
                time.sleep(10)


check = soup.find('h6', class_='NoRecords-header')
startTime = '13:00'
endtime = '04:00'
currentTime = datetime.datetime.now().time().strftime("%H:%M")

if check == None:
    if not startTime < currentTime < endtime:
        nba_scores()
else:
    if not startTime < currentTime < endtime:
        file = open("nba_scores.txt", "w")
        file.truncate()
        nba_scores()