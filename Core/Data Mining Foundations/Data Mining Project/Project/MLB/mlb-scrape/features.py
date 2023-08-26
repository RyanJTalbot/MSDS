import pandas as pd
import numpy as np

import re
from scipy.stats import skew
from trueskill import rate_1vs1, Rating


def game_stats(games, df):
    '''
    adds season to date stats from rolling through dataframe
    '''
    # make sure we have the same games in the same order in both df's
    games = games.sort_values(by=['date', 'game_id']).reset_index(drop=True)
    df = df.sort_values(by=['date', 'game_id']).reset_index(drop=True)
    # assert all(games['game_id']==df['game_id'])

    df['home_team_season'] = df['home_team_abbr'] + \
        '_' + df['season'].astype('str')
    df['away_team_season'] = df['away_team_abbr'] + \
        '_' + df['season'].astype('str')

    # normalize spread for each team
    games['home_team_spread'] = games['spread']
    games['away_team_spread'] = -games['spread']

    names = ['home_team_errors_mean', 'home_team_errors_stdev', 'home_team_errors_skew',
             'away_team_errors_mean', 'away_team_errors_stdev', 'away_team_errors_skew',
             'home_team_spread_mean', 'home_team_spread_stdev', 'home_team_spread_skew',
             'away_team_spread_mean', 'away_team_spread_stdev', 'away_team_spread_skew',
             'home_team_wins_mean', 'home_team_wins_stdev', 'home_team_wins_skew',
             'away_team_wins_mean', 'away_team_wins_stdev', 'away_team_wins_skew'
             ]
    lists = {}
    for n in names:
        lists[n] = []

    # intitialize game stat lists
    errors = {}
    spread = {}
    wins = {}
    for t in df['home_team_season'].unique():
        errors[t] = []
        spread[t] = []
        wins[t] = []
    for t in df['away_team_season'].unique():
        errors[t] = []
        spread[t] = []
        wins[t] = []

    for i, r in df.iterrows():
        m, s, sk = get_stats_from_dist(errors[r.home_team_season])
        lists['home_team_errors_mean'].append(m)
        lists['home_team_errors_stdev'].append(s)
        lists['home_team_errors_skew'].append(sk)
        m, s, sk = get_stats_from_dist(errors[r.away_team_season])
        lists['away_team_errors_mean'].append(m)
        lists['away_team_errors_stdev'].append(s)
        lists['away_team_errors_skew'].append(sk)
        m, s, sk = get_stats_from_dist(spread[r.home_team_season])
        lists['home_team_spread_mean'].append(m)
        lists['home_team_spread_stdev'].append(s)
        lists['home_team_spread_skew'].append(sk)
        m, s, sk = get_stats_from_dist(spread[r.away_team_season])
        lists['away_team_spread_mean'].append(m)
        lists['away_team_spread_stdev'].append(s)
        lists['away_team_spread_skew'].append(sk)
        m, s, sk = get_stats_from_dist(wins[r.home_team_season])
        lists['home_team_wins_mean'].append(m)
        lists['home_team_wins_stdev'].append(s)
        lists['home_team_wins_skew'].append(sk)
        m, s, sk = get_stats_from_dist(wins[r.away_team_season])
        lists['away_team_wins_mean'].append(m)
        lists['away_team_wins_stdev'].append(s)
        lists['away_team_wins_skew'].append(sk)

        # update dict with latest game
        if r.game_id in list(games.game_id):
            g = games.iloc[games[games.game_id ==
                                 r.game_id].first_valid_index()]
            errors[r['home_team_season']].append(g['home_team_errors'])
            errors[r['away_team_season']].append(g['away_team_errors'])
            spread[r['home_team_season']].append(g['home_team_spread'])
            spread[r['away_team_season']].append(g['away_team_spread'])
            wins[r['home_team_season']].append(
                g['home_team_runs'] > g['away_team_runs'])
            wins[r['away_team_season']].append(
                g['home_team_runs'] < g['away_team_runs'])

    # get differences
    error_diff = np.array(lists['home_team_errors_mean']) - \
        np.array(lists['away_team_errors_mean'])
    spread_diff = np.array(lists['home_team_spread_mean']) - \
        np.array(lists['away_team_spread_mean'])
    wins_diff = np.array(lists['home_team_wins_mean']) - \
        np.array(lists['away_team_wins_mean'])

    # add created rows into df
    for n in names:
        df[n] = lists[n]
    df['error_diff'] = error_diff
    df['spread_diff'] = spread_diff
    df['wins_diff'] = wins_diff

    df = df.sort_values(by='date').reset_index(drop=True)
    return df


def add_rest_durations(df):
    '''
    adds columns with days since pitcher and team started games
    '''
    df.date = pd.to_datetime(df.date)

    # initalize rest dictionary
    rest = {}
    for x in df.home_team_abbr.unique():
        rest[x] = pd.to_datetime('12-31-2009')
    for x in df.away_team_abbr.unique():
        rest[x] = pd.to_datetime('12-31-2009')
    for x in df.home_pitcher.unique():
        rest[x] = pd.to_datetime('12-31-2009')
    for x in df.away_pitcher.unique():
        rest[x] = pd.to_datetime('12-31-2009')

    # lists to temporairily hold results
    home_team_rest = []
    away_team_rest = []
    home_pitch_rest = []
    away_pitch_rest = []

    for i, r in df.iterrows():
        # get pre-match trueskill ratings from dict
        home_team_rest.append(r.date - rest[r.home_team_abbr])
        away_team_rest.append(r.date - rest[r.away_team_abbr])
        home_pitch_rest.append(r.date - rest[r.home_pitcher])
        away_pitch_rest.append(r.date - rest[r.away_pitcher])

        # update ratings dictionary with post-match ratings
        if r.date < df.date.max():
            # doubleheaders get screwed up if we do this on current day
            rest[r.home_team_abbr] = r.date
            rest[r.away_team_abbr] = r.date
            rest[r.home_pitcher] = r.date
            rest[r.away_pitcher] = r.date

    # add results to df
    df['home_team_rest'] = home_team_rest
    df['away_team_rest'] = away_team_rest
    df['home_pitcher_rest'] = home_pitch_rest
    df['away_pitcher_rest'] = away_pitch_rest

    for x in ['home_team_rest', 'away_team_rest', 'home_pitcher_rest', 'away_pitcher_rest']:
        df[x] = df[x].dt.days
        df[x] = df[x].clip(1, 30)   # rest doesn't matter for large values

    # match comparisons
    df['team_rest_diff'] = df.home_team_rest - df.away_team_rest
    df['pitcher_rest_diff'] = df.home_pitcher_rest - df.away_pitcher_rest

    return df


def add_trueskill_ratings(df):
    '''
    adds columns with trueskill ratings to df
    https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/
    '''
    ratings = {}
    for x in df.home_team_abbr.unique():
        ratings[x] = 25
    for x in df.away_team_abbr.unique():
        ratings[x] = 25

    home_trueskill_pre = []
    away_trueskill_pre = []
    for i, r in df.iterrows():
        # get pre-match trueskill ratings from dict
        home_trueskill_pre.append(ratings[r.home_team_abbr])
        away_trueskill_pre.append(ratings[r.away_team_abbr])

        if r.date < df.date.max():
            # doubleheaders get screwed up if we do this on current day
            # update ratings dictionary with post-match ratings
            ts1 = Rating(ratings[r.home_team_abbr])
            ts2 = Rating(ratings[r.away_team_abbr])
            if r.home_team_win == 1:
                ts1, ts2 = rate_1vs1(ts1, ts2)
            else:
                ts2, ts1 = rate_1vs1(ts2, ts1)
            ratings[r.home_team_abbr] = ts1.mu
            ratings[r.away_team_abbr] = ts2.mu

    df['home_trueskill_pre'] = home_trueskill_pre
    df['away_trueskill_pre'] = away_trueskill_pre
    df['ts_diff'] = df.home_trueskill_pre-df.away_trueskill_pre

    df.replace({np.inf: 0}, inplace=True)
    return df


def get_game_df():
    '''
    gets base dataframe of historical data that matches data
    that can be scraped for current day.

    Plus target column: 'home_team_win'
    '''
    games = get_games()
    df = games[['game_id', 'home_team_abbr',
                'away_team_abbr', 'date', 'is_night_game']]
    df['home_team_win'] = games.home_team_runs.astype(
        'int') > games.away_team_runs

    pitchers = get_pitchers()
    home_pitchers = pitchers[['name', 'game_id']].where(
        (pitchers.is_home_team) & (pitchers.is_starting_pitcher)).dropna()
    home_pitchers['home_pitcher'] = home_pitchers['name']
    home_pitchers = home_pitchers.groupby('game_id')['home_pitcher'].first()
    df = pd.merge(left=df, right=home_pitchers, on='game_id', how='left')

    away_pitchers = pitchers[['name', 'game_id']].where(
        (~pitchers.is_home_team) & (pitchers.is_starting_pitcher)).dropna()
    away_pitchers['away_pitcher'] = away_pitchers['name']
    away_pitchers = away_pitchers.groupby('game_id')['away_pitcher'].first()
    df = pd.merge(left=df, right=away_pitchers, on='game_id', how='left')

    df = df.sort_values(by='date').reset_index(drop=True)
    return df


def add_season_rolling(stat_df, df, cols, team, name):
    '''
    add seasonal rolling statistical features to target dataframe

    params:
    ------
    stat_df: the dataframe with the game stats (like from batting.csv
    df: the target dataframe we're going to return with new columns
    cols: list of columns in stat_df containing the stats of interest
    team: binary whether this is a team stat (false if pitcher stat)
    name: the string appended to each feature name (like 'batting')
    '''
    stat_df['season'] = stat_df.game_id.str[3:7]
    for s in cols:
        if team:
            stat_df[s+'_mean'] = stat_df.groupby(['team', 'season'])[s].apply(
                lambda x: x.rolling(200, min_periods=1).mean())
            stat_df[s+'_stdev'] = stat_df.groupby(['team', 'season'])[s].apply(
                lambda x: x.rolling(200, min_periods=1).std())
            stat_df[s+'_skew'] = stat_df.groupby(['team', 'season'])[s].apply(
                lambda x: x.rolling(200, min_periods=1).skew())
        else:
            stat_df[s+'_mean'] = stat_df.groupby(['name', 'season'])[s].apply(
                lambda x: x.rolling(200, min_periods=1).mean())
            stat_df[s+'_stdev'] = stat_df.groupby(['name', 'season'])[s].apply(
                lambda x: x.rolling(200, min_periods=1).std())
            stat_df[s+'_skew'] = stat_df.groupby(['name', 'season'])[s].apply(
                lambda x: x.rolling(200, min_periods=1).skew())

    stat_cols = []
    for s in cols:
        stat_cols.append(s + '_mean')
        stat_cols.append(s + '_stdev')
        stat_cols.append(s + '_skew')
    stat_cols.append('game_id')

    df_len = len(df)
    b = stat_df[stat_cols][stat_df['is_home_team'] ==
                           True].groupby('game_id').first().reset_index()
    df = pd.merge(left=df, right=b, on='game_id', how='left')

    for s in stat_cols:
        if s == 'game_id':
            continue
        df['home_'+name+'_'+s] = df[s]
        df.drop(columns=s, inplace=True)
        # shift the stats to the next game, in order to convert to pre-game stats
        if team:
            df['home_'+name+'_' +
                s] = df.groupby('home_team_abbr')['home_'+name+'_'+s].shift()
        else:
            df['home_'+name+'_' +
                s] = df.groupby('home_pitcher')['home_'+name+'_'+s].shift()

    b = stat_df[stat_cols][stat_df['is_home_team'] ==
                           False].groupby('game_id').first().reset_index()
    df = pd.merge(left=df, right=b, on='game_id', how='left')

    for s in stat_cols:
        if s == 'game_id':
            continue
        df['away_'+name+'_'+s] = df[s]
        df.drop(columns=s, inplace=True)
        # shift the stats to the next game, in order to convert to pre-game stats
        if team:
            df['away_'+name+'_' +
                s] = df.groupby('away_team_abbr')['away_'+name+'_'+s].shift()
        else:
            df['away_'+name+'_' +
                s] = df.groupby('away_pitcher')['away_'+name+'_'+s].shift()

    assert df_len == len(df)

    # create diff stats
    for s in cols:
        if s == 'game_id':
            continue
        df[name+'_'+s+'_diff'] = df['home_'+name+'_' +
                                    s+'_mean']-df['away_'+name+'_'+s+'_mean']

    return df


def add_10RA_rolling(stat_df, df, cols, team, name):
    '''
    add 10 period rolling statistical features to target dataframe

    params:
    ------
    stat_df: the dataframe with the game stats (like from batting.csv
    df: the target dataframe we're going to return with new columns
    cols: list of columns in stat_df containing the stats of interest
    team: binary whether this is a team stat (false if pitcher stat)
    name: the string appended to each feature name (like 'batting')
    '''
    # create stat
    for s in cols:
        if team:
            stat_df[s+'_10RA'] = stat_df.groupby('team')[s].apply(
                lambda x: x.rolling(10, min_periods=1).mean())
        else:
            stat_df[s+'_10RA'] = stat_df.groupby('name')[s].apply(
                lambda x: x.rolling(10, min_periods=1).mean())

    # add stat to target dataframe
    stat_cols = [x + '_10RA' for x in cols]
    stat_cols.append('game_id')

    # home team first
    df_len = len(df)
    b = stat_df[stat_cols][stat_df['is_home_team'] ==
                           True].groupby('game_id').first().reset_index()
    df = pd.merge(left=df, right=b, on='game_id', how='left')

    for s in stat_cols:
        if s == 'game_id':
            continue
        df['home_'+name+'_'+s] = df[s]
        df.drop(columns=s, inplace=True)
        # shift the stats to the next game, in order to convert to pre-game stats
        if team:
            df['home_'+name+'_' +
                s] = df.groupby('home_team_abbr')['home_'+name+'_'+s].shift()
        else:
            df['home_'+name+'_' +
                s] = df.groupby('home_pitcher')['home_'+name+'_'+s].shift()
    # now away team
    b = stat_df[stat_cols][stat_df['is_home_team'] ==
                           False].groupby('game_id').first().reset_index()
    df = pd.merge(left=df, right=b, on='game_id', how='left')

    for s in stat_cols:
        if s == 'game_id':
            continue
        df['away_'+name+'_'+s] = df[s]
        df.drop(columns=s, inplace=True)
        # shift the stats to the next game, in order to convert to pre-game stats
        if team:
            df['away_'+name+'_' +
                s] = df.groupby('away_team_abbr')['away_'+name+'_'+s].shift()
        else:
            df['away_'+name+'_' +
                s] = df.groupby('away_pitcher')['away_'+name+'_'+s].shift()

    assert df_len == len(df)

    # create diff stats
    for s in stat_cols:
        if s == 'game_id':
            continue
        df[name+'_'+s+'_diff'] = df['home_'+name+'_'+s]-df['away_'+name+'_'+s]

    return df


def get_stats_from_dist(dist):
    d = np.array(dist).astype('float')
    return d.mean(), d.std(), skew(d)

#######################
##   get/clean data  ##
#######################


def get_pitchers():
    pitchers = pd.read_csv('../data/pitchers.csv')
    pitchers.drop_duplicates()
    pitchers.to_csv('../data/pitchers.csv', index=False)

    pitchers['is_home_team'] = True
    pitchers['is_home_team'][pitchers['home_away'] == 'away'] = False
    pitchers.drop(columns='home_away', inplace=True)

    pitchers['is_starting_pitcher'] = False
    pitchers['is_starting_pitcher'][pitchers.inherited_runners.isna()] = True
    return pitchers


def get_pitching():
    pitching = pd.read_csv('../data/pitching.csv')
    pitching.drop_duplicates()
    pitching.to_csv('../data/pitching.csv', index=False)

    pitching['is_home_team'] = True
    pitching['is_home_team'][pitching['home_away'] == 'away'] = False
    pitching.drop(columns='home_away', inplace=True)
    return pitching


def get_batting():
    batting = pd.read_csv('../data/batting.csv')
    batting.drop_duplicates()
    batting.to_csv('../data/batting.csv', index=False)

    batting['is_home_team'] = True
    batting['is_home_team'][batting['home_away'] == 'away'] = False
    batting.drop(columns='home_away', inplace=True)
    return batting


def get_games():
    games = pd.read_csv('../data/game_summaries.csv')
    games.drop_duplicates()
    games.to_csv('../data/game_summaries.csv', index=False)

    games['date'] = pd.to_datetime(games.date).dt.date
    games['start_time'] = games['start_time'].apply(lambda x: start_times(x))
    games['is_night_game'] = True
    games['is_night_game'][games['day_night'].isin(['Day Game'])] = False
    games.drop(columns='day_night', inplace=True)

    games['is_grass'] = False
    games['is_grass'][games['field_type'].isin(['on grass'])] = True
    games.drop(columns='field_type', inplace=True)

    games['spread'] = games.home_team_runs.astype('int') - games.away_team_runs

    return games


def start_times(x):
    '''
    cleanup routine for start times
    '''
    x = str(x)
    if re.findall('(\d+\:\d+)', x) == []:
        return np.nan
    else:
        return re.findall('(\d+\:\d+)', x)[0]
