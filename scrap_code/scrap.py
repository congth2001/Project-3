import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlencode

urlId=320
def preSeason(url):
  params = {'api_key': '2ce05fd4c124e722ab8ba3c0f1019289', 'url': url}
  data = requests.get('http://api.scraperapi.com/', params=urlencode(params))
  soup = BeautifulSoup(data.text, 'html.parser')
  for href in soup.find_all("a"):
    if href.text == "Previous Season" or href.text == "Previous Competition":
      preSs = href
      break

  return "https://fbref.com" + preSs.get('href')

def scrapOverview(url):
  
  pass

def scrapTournament(url):
  id = 1
  params = {'api_key': '2ce05fd4c124e722ab8ba3c0f1019289', 'url': url}
  data = requests.get('http://api.scraperapi.com/', params=urlencode(params))
  soup = BeautifulSoup(data.text, 'html.parser')
  #matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
  
  table = soup.find_all("table")[0]
  links = table.find_all("a")
  print(len(links))
  matchReports = []
  for link in links: 
    if link.text == "Match Report":
      matchReports.append(link)
  matchReportLinks = ["https://fbref.com" + l.get("href") for l in matchReports]
  global urlId
  matchReportLinks = matchReportLinks[urlId+1:]

  shots_all = None
  playerStats_all = None
  passingStats_all = None
  passTypeStats_all = None
  defensiveStats_all = None
  possessionStats_all = None
  miscellaneousStats_all = None
  gkStats_all = None
  teamStats_all = None
  extraStats_all = None

  for url in matchReportLinks:
    urlId+=1
    params = {'api_key': '2ce05fd4c124e722ab8ba3c0f1019289', 'url': url}
    data = requests.get('http://api.scraperapi.com/', params=urlencode(params))
    soup = BeautifulSoup(data.text, 'html.parser')
    matchID = url.split("/")[-2]
    
    try:
      dataPD = pd.read_html(data.text)
    except:
      urlId-=1
    
    table = soup.select("table.stats_table")
    tourName = soup.select("#content a")[0].text
    if len(dataPD) < 18:
      continue
    extraPD = 20 - len(dataPD)
    print(tourName, matchID, urlId)


    # shots
    shots = dataPD[extraPD-3]
    shots.insert(0 ,"Match ID", matchID, True)
    shots.insert(0 ,"Tournament", tourName, True)
    shots_all = pd.concat([shots_all, shots])

    # playerStats
    links = table[0].find_all('a')
    links = [l.get("href") for l in links]
    playersID1 = []
    for link in links:
      if link.split("/")[2] == "players":
        playersID1.append(link.split("/")[-2])

    links = table[7].find_all('a')
    links = [l.get("href") for l in links]
    playersID2 = []
    for link in links:
      if link.split("/")[2] == "players":
        playersID2.append(link.split("/")[-2])

    playerStats1 = dataPD[extraPD-17]
    playerStats1 = playerStats1.drop([playerStats1.shape[0]-1])
    playerStats1.insert(0 ,"Player ID", playersID1, True)

    playerStats2 = dataPD[extraPD-10]
    playerStats2 = playerStats2.drop([playerStats2.shape[0]-1])
    playerStats2.insert(0 ,"Player ID", playersID2, True)

    playerStats = pd.concat([playerStats1, playerStats2])
    playerStats.insert(0 ,"Match ID", matchID, True)
    playerStats.insert(0 ,"Tournament", tourName, True)
    playerStats_all = pd.concat([playerStats_all, playerStats])


    passingStats1 = dataPD[extraPD-16]
    passingStats1 = passingStats1.drop([passingStats1.shape[0]-1])
    passingStats1.insert(0 ,"Player ID", playersID1, True)

    passingStats2 = dataPD[extraPD-9]
    passingStats2 = passingStats2.drop([passingStats2.shape[0]-1])
    passingStats2.insert(0 ,"Player ID", playersID2, True)

    passingStats = pd.concat([passingStats1, passingStats2])
    passingStats.insert(0 ,"Match ID", matchID, True)
    passingStats.insert(0 ,"Tournament", tourName, True)
    passingStats_all = pd.concat([passingStats_all, passingStats])


    passTypeStats1 = dataPD[extraPD-15]
    passTypeStats1 = passTypeStats1.drop([passTypeStats1.shape[0]-1])
    passTypeStats1.insert(0 ,"Player ID", playersID1, True)

    passTypeStats2 = dataPD[extraPD-8]
    passTypeStats2 = passTypeStats2.drop([passTypeStats2.shape[0]-1])
    passTypeStats2.insert(0 ,"Player ID", playersID2, True)

    passTypeStats = pd.concat([passTypeStats1, passTypeStats2])
    passTypeStats.insert(0 ,"Match ID", matchID, True)
    passTypeStats.insert(0 ,"Tournament", tourName, True)
    passTypeStats_all = pd.concat([passTypeStats_all, passTypeStats])


    defensiveStats1 = dataPD[extraPD-14]
    defensiveStats1 = defensiveStats1.drop([defensiveStats1.shape[0]-1])
    defensiveStats1.insert(0 ,"Player ID", playersID1, True)

    defensiveStats2 = dataPD[extraPD-7]
    defensiveStats2 = defensiveStats2.drop([defensiveStats2.shape[0]-1])
    defensiveStats2.insert(0 ,"Player ID", playersID2, True)

    defensiveStats = pd.concat([defensiveStats1, defensiveStats2])
    defensiveStats.insert(0 ,"Match ID", matchID, True)
    defensiveStats.insert(0 ,"Tournament", tourName, True)
    defensiveStats_all = pd.concat([defensiveStats_all, defensiveStats])


    possessionStats1 = dataPD[extraPD-13]
    possessionStats1 = possessionStats1.drop([possessionStats1.shape[0]-1])
    possessionStats1.insert(0 ,"Player ID", playersID1, True)

    possessionStats2 = dataPD[extraPD-6]
    possessionStats2 = possessionStats2.drop([possessionStats2.shape[0]-1])
    possessionStats2.insert(0 ,"Player ID", playersID2, True)

    possessionStats = pd.concat([possessionStats1, possessionStats2])
    possessionStats.insert(0 ,"Match ID", matchID, True)
    possessionStats.insert(0 ,"Tournament", tourName, True)
    possessionStats_all = pd.concat([possessionStats_all, possessionStats])


    miscellaneousStats1 = dataPD[extraPD-13]
    miscellaneousStats1 = miscellaneousStats1.drop([miscellaneousStats1.shape[0]-1])
    miscellaneousStats1.insert(0 ,"Player ID", playersID1, True)

    miscellaneousStats2 = dataPD[extraPD-6]
    miscellaneousStats2 = miscellaneousStats2.drop([miscellaneousStats2.shape[0]-1])
    miscellaneousStats2.insert(0 ,"Player ID", playersID2, True)

    miscellaneousStats = pd.concat([miscellaneousStats1, miscellaneousStats2])
    miscellaneousStats.insert(0 ,"Match ID", matchID, True)
    miscellaneousStats.insert(0 ,"Tournament", tourName, True)
    miscellaneousStats_all = pd.concat([miscellaneousStats_all, miscellaneousStats])

    # gkStats
    gkStats1 = dataPD[extraPD-11]
    links = table[6].find_all('a')
    links = [l.get("href") for l in links]
    playersID = []
    for link in links:
      if link.split("/")[-3] == "players":
        playersID.append(link.split("/")[-2])
    gkStats1.insert(0 ,"Player ID", playersID, True)

    gkStats2 = dataPD[extraPD-4]
    links = table[13].find_all('a')
    links = [l.get("href") for l in links]
    playersID = []
    for link in links:
      if link.split("/")[-3] == "players":
        playersID.append(link.split("/")[-2])
    gkStats2.insert(0 ,"Player ID", playersID, True)

    gkStats = pd.concat([gkStats1, gkStats2])
    gkStats.insert(0 ,"Match ID", matchID, True)
    gkStats.insert(0 ,"Tournament", tourName, True)
    gkStats_all = pd.concat([gkStats_all, gkStats])

    stats = soup.select(".score")
    scores = []
    for score in stats:
      scores.append(score.text)

    stats = soup.select("#team_stats")[0].find_all("tr")
    teams = []
    for th in stats[0]:
      if not th.text == "\n":
        teams.append(th.text.replace("\n","").replace("\t","").replace(" ",""))

    dataframe = {}
    for index in range(2, len(stats)-2, 2):
      dataframe[stats[index-1].text] = []
    for index in range(2, len(stats)-2, 2):
      for td in stats[index].find_all("td"):
        dataframe[stats[index-1].text].append(td.text.replace("\n","").replace("\xa0",""))

    dataframe[stats[len(stats)-2].text] = []
    for td in stats[-1].find_all("td"):
      dataframe[stats[len(stats)-2].text].append({"Yellow Card":len(td.select(".yellow_card")), "Red Card":len(td.select(".red_card"))})

    teamStats = pd.DataFrame(dataframe)
    teamStats.insert(0 ,"Squad", teams, True)
    teamStats.insert(0 ,"Score", scores, True)
    teamStats.insert(0 ,"Match ID", matchID, True)
    teamStats.insert(0 ,"Tournament", tourName, True)
    teamStats_all = pd.concat([teamStats_all, teamStats])

    extras = soup.select("#team_stats_extra>div")
    dataframe = {}
    for extra in extras:
      extra = extra.find_all("div")
      for index in range(3, len(extra), 3):
        dataframe[extra[index+1].text] = []
      for index in range(3, len(extra), 3):
        dataframe[extra[index+1].text].append(extra[index].text)
        dataframe[extra[index+1].text].append(extra[index+2].text)

    extraStats = pd.DataFrame(dataframe)
    extraStats_all = pd.concat([extraStats_all, extraStats])
    teamStats = pd.concat([teamStats, extraStats], axis=1)

    all = [shots, playerStats, passingStats, passTypeStats, defensiveStats, possessionStats, miscellaneousStats, gkStats, teamStats]
    index=1
    for stat in all:
      df = pd.DataFrame(stat)
      df.to_csv("stat_1{stat}.csv".format(stat=index), index=False, header=False, mode="a")
      index+=1
    print("Read to csv file completed")
    id+=1

  # teamStats_all = pd.concat([teamStats_all, extraStats_all], axis=1)
  # return shots_all, playerStats_all, passingStats_all, passTypeStats_all, defensiveStats_all, possessionStats_all, miscellaneousStats_all, gkStats_all, teamStats_all

def scrap(urls):
   for url in urls:
    for i in range(1):
      url = preSeason(url)
      scrapTournament(url)

if __name__ == "__main__":
  #url1 = 'https://fbref.com/en/comps/882/schedule/Europa-Conference-League-Scores-and-Fixtures'
  #url3 = 'https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures'
  #url2 = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
  #url4 = 'https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures'
  #url6 = 'https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures'
  #url8 = 'https://fbref.com/en/comps/10/schedule/Championship-Scores-and-Fixtures'
  #url5 = 'https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures'
  #url10 = 'https://fbref.com/en/comps/14/schedule/Copa-Libertadores-Scores-and-Fixtures'
  #url12 = 'https://fbref.com/en/comps/19/schedule/Europa-League-Scores-and-Fixtures'
  #url11 = 'https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures'
  # url7 = 'https://fbref.com/en/comps/22/schedule/Major-League-Soccer-Scores-and-Fixtures'
  # url13 = 'https://fbref.com/en/comps/23/schedule/Eredivisie-Scores-and-Fixtures'
  # url9 = 'https://fbref.com/en/comps/24/schedule/Serie-A-Scores-and-Fixtures'
  # url14 = 'https://fbref.com/en/comps/31/schedule/Liga-MX-Scores-and-Fixtures'
  # url15 = 'https://fbref.com/en/comps/32/schedule/Primeira-Liga-Scores-and-Fixtures'
  # url16 = 'https://fbref.com/en/comps/676/schedule/European-Championship-Scores-and-Fixtures'
  #url17 = 'https://fbref.com/en/comps/1/schedule/World-Cup-Scores-and-Fixtures'
  #urls = [url10, url12, url11, url7, url13, url9, url14, url15, url16, url17]
  #stats = scrapTournament(url6)
  # index=1
  # for stat in stats:
  #   df = pd.DataFrame(stat)
  #   df.to_csv("stat_{stat}.csv".format(stat=index), index=False)
  #   index+=1
  
  # for i in range(5):
  #   index=1
  #   url = preSeason(url6)
  #   stats = scrapTournament(url6)
  #   for stat in stats:
  #     df = pd.DataFrame(stat)
  #     df.to_csv("stat_{stat}.csv".format(stat=index), index=False, header=False, mode="a")
  #     index+=1
  # scrapTournament('https://fbref.com/en/comps/31/2017-2018/schedule/2017-2018-Liga-MX-Scores-and-Fixtures')
  # scrapTournament('https://fbref.com/en/comps/11/2018-2019/schedule/2018-2019-Serie-A-Scores-and-Fixtures')
  u = 'https://fbref.com/en/comps/11/2017-2018/schedule/2017-2018-Serie-A-Scores-and-Fixtures'

  
  urlId=-1  
  while 1:
    try:
      scrapTournament(u)
      break
    except:
      continue