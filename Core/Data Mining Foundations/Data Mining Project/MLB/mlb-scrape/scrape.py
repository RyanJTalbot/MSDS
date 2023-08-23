import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import threading


def get_today_games():
    '''
    pulls down today's games from https://www.baseball-reference.com/previews/
    returns dataframe
    '''
    games = []
    url = 'https://www.baseball-reference.com/previews/'
    page = requests.get(url).text
    soup = bs(page, 'lxml')
    summaries = soup.findAll('div', {'class': 'game_summary'})
    for s in summaries:
        game = {}
        cells = s.findAll('table')[0].findAll('td')
        try:
            team_links = s.findAll('a')
            game['away_team_abbr'] = team_links[0]['href'].split('/')[2]
            game['home_team_abbr'] = team_links[2]['href'].split('/')[2]
        except Exception as e:
            # just all star games trigger this, I think
            print(team_links)
            continue

        # get time
        game['time'] = s.find('table', {'class': 'teams'}).find(
            'tbody').findAll('tr')[1].findAll('td')[2].text.strip()
        # get pitchers
        try:
            cells = s.findAll('table')[1].findAll('td')
            game['away_pitcher'] = cells[1].find(
                'a')['href'].split('/')[-1][:-6].strip()
            game['home_pitcher'] = cells[3].find(
                'a')['href'].split('/')[-1][:-6].strip()
        except Exception as e:
            print("no pitcher", game)
        games.append(game)
    test_df = pd.DataFrame(games)
    test_df['date'] = pd.datetime.now().date()
    return test_df


def process_link(link, lock=None):
    '''
    takes link from get_game_links and processes the games
    into csv files
    '''

    if lock == None:
        lock = threading.Lock()

    url = f'https://www.baseball-reference.com{link}'
    html = requests.get(url).text

    game_id = url.split('/')[-1][:-6]
    game_id

    uncommented_html = ''
    for h in html.split('\n'):
        if '<!--     <div' in h:
            continue
        if h.strip() == '<!--':
            continue
        if h.strip() == '-->':
            continue
        uncommented_html += h + '\n'
    soup = bs(uncommented_html)

    game_summary = get_game_summary(soup)
    home_batting, away_batting = get_batting_data(soup)
    home_pitching, away_pitching = get_pitching_data(soup)
    home_pitchers, away_pitchers = get_pitcher_data(soup)

    game_summary['game_id'] = game_id
    for x in [home_batting, home_pitching]:
        x['team'] = game_summary['home_team_abbr']
        x['game_id'] = game_id
    for x in home_pitchers:
        x['team'] = game_summary['home_team_abbr']
        x['game_id'] = game_id
    for x in [away_batting, away_pitching]:
        x['team'] = game_summary['away_team_abbr']
        x['game_id'] = game_id
    for x in away_pitchers:
        x['team'] = game_summary['away_team_abbr']
        x['game_id'] = game_id

    lock.acquire()
    with open('../data/game_summaries.csv', 'a') as f:
        df = pd.DataFrame([game_summary])
        df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
    with open('../data/pitching.csv', 'a') as f:
        df = pd.DataFrame([home_pitching, away_pitching])
        df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
    away_pitchers.extend(home_pitchers)
    with open('../data/pitchers.csv', 'a') as f:
        df = pd.DataFrame(away_pitchers)
        df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
    with open('../data/batting.csv', 'a') as f:
        df = pd.DataFrame([home_batting, away_batting])
        df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
    lock.release()

    print(game_id, 'done')


def get_pitcher_data(soup):
    '''
    gets idivdual pitching information from beautifuls soup generated from pages like
    https://www.baseball-reference.com/boxes/BOS/BOS201004040.shtml

    params:
    soup: beautifulsoup object
    '''

    home_pitchers = []
    away_pitchers = []

    stats_tables = soup.findAll('table', {'class': 'stats_table'})
    away = stats_tables[3].find('tbody')
    home = stats_tables[4].find('tbody')

    stats = ['IP', 'H', 'R', 'ER', 'BB', 'SO', 'H', 'HR', 'earned_run_avg',
             'batters_faced', 'pitches', 'strikes_total', 'strikes_contact',
             'strikes_swinging', 'strikes_looking', 'inplay_gb_total', 'inplay_fb_total',
             'inplay_ld', 'inplay_unk', 'game_score', 'inherited_runners',
             'inherited_score', 'wpa_def', 'leverage_index_avg', 're24_def']
    for r in away.findAll('tr'):
        away_pitcher = {}
        away_pitcher['home_away'] = 'away'
        away_pitcher['name'] = r.find(
            'th', {'data-stat': 'player'}).find('a')['href'].split('/')[-1][:-6].strip()
        for s in stats:
            away_pitcher[s] = r.find('td', {'data-stat': s}).text.strip()
        away_pitchers.append(away_pitcher)
    for r in home.findAll('tr'):
        home_pitcher = {}
        home_pitcher['home_away'] = 'home'
        home_pitcher['name'] = r.find(
            'th', {'data-stat': 'player'}).find('a')['href'].split('/')[-1][:-6].strip()
        for s in stats:
            home_pitcher[s] = r.find('td', {'data-stat': s}).text.strip()
        home_pitchers.append(home_pitcher)

    return home_pitchers, away_pitchers


def get_pitching_data(soup):
    '''
    gets team pitching information from beautifuls soup generated from pages like
    https://www.baseball-reference.com/boxes/BOS/BOS201004040.shtml

    params:
    soup: beautifulsoup object
    '''

    home_pitching = {}
    away_pitching = {}

    stats_tables = soup.findAll('table', {'class': 'stats_table'})
    away = stats_tables[3].find('tfoot')
    home = stats_tables[4].find('tfoot')

    stats = ['IP', 'H', 'R', 'ER', 'BB', 'SO', 'H', 'HR', 'earned_run_avg',
             'batters_faced', 'pitches', 'strikes_total', 'strikes_contact',
             'strikes_swinging', 'strikes_looking', 'inplay_gb_total', 'inplay_fb_total',
             'inplay_ld', 'inplay_unk', 'game_score', 'inherited_runners',
             'inherited_score', 'wpa_def', 'leverage_index_avg', 're24_def']
    home_pitching['home_away'] = 'home'
    away_pitching['home_away'] = 'away'
    for s in stats:
        away_pitching[s] = away.find('td', {'data-stat': s}).text.strip()
        home_pitching[s] = home.find('td', {'data-stat': s}).text.strip()

    return home_pitching, away_pitching


def get_batting_data(soup):
    '''
    gets game batting information from beautifuls soup generated from pages like
    https://www.baseball-reference.com/boxes/BOS/BOS201004040.shtml

    params:
    soup: beautifulsoup object
    '''

    home_batting = {}
    away_batting = {}

    stats_tables = soup.findAll('table', {'class': 'stats_table'})
    away = stats_tables[1].find('tfoot')
    home = stats_tables[2].find('tfoot')

    stats = ['AB', 'R', 'H', 'RBI', 'BB', 'SO', 'PA', 'batting_avg', 'onbase_perc',
             'slugging_perc', 'onbase_plus_slugging', 'pitches', 'strikes_total',
             'wpa_bat', 'leverage_index_avg', 'wpa_bat_pos', 'wpa_bat_neg',
             're24_bat', 'PO', 'A']
    home_batting['home_away'] = 'home'
    away_batting['home_away'] = 'away'
    for s in stats:
        away_batting[s] = away.find('td', {'data-stat': s}).text.strip()
        home_batting[s] = home.find('td', {'data-stat': s}).text.strip()

    return home_batting, away_batting


def get_game_summary(soup):
    '''
    gets game summary information from beautifuls soup generated from pages like
    https://www.baseball-reference.com/boxes/BOS/BOS201004040.shtml

    params:
    soup: beautifulsoup object
    '''
    game = {}
    scorebox = soup.find('div', {'class': 'scorebox'})

    teams = scorebox.findAll('a', {'itemprop': 'name'})
    game['away_team_abbr'] = teams[0]['href'].split('/')[2]
    game['home_team_abbr'] = teams[1]['href'].split('/')[2]

    meta = scorebox.find('div', {'class': 'scorebox_meta'}).findAll('div')
    game['date'] = meta[0].text.strip()
    game['start_time'] = meta[1].text[12:-6].strip()
    game['venue'] = meta[3].text[7:].strip()
    game['day_night'] = meta[5].text.split(', ')[0].strip()
    try:
        game['field_type'] = meta[5].text.split(', ')[1].strip()
    except:
        game['field_type'] = ''

    box = soup.find('table', {'class': 'linescore'})
    rows = box.findAll('tr')
    game['away_team_errors'] = rows[1].findAll('td')[-1].text.strip()
    game['home_team_errors'] = rows[2].findAll('td')[-1].text.strip()
    game['away_team_hits'] = rows[1].findAll('td')[-2].text.strip()
    game['home_team_hits'] = rows[2].findAll('td')[-2].text.strip()
    game['away_team_runs'] = rows[1].findAll('td')[-3].text.strip()
    game['home_team_runs'] = rows[2].findAll('td')[-3].text.strip()

    return game


def get_game_links(day):
    '''
    gets links to game summary pages from daily boxscore summary page

    params:
    day: day as pandas datetime object
    '''

    links = []
    url = f'https://www.baseball-reference.com/boxes/?month={day.month}&day={day.day}&year={day.year}'
    soup = bs(requests.get(url).text, 'lxml')
    summaries = soup.findAll('table', {'class': 'teams'})
    for s in summaries:
        x = s.find('td', {'class': 'gamelink'}).find('a')
        links.append(x['href'])
    return links
