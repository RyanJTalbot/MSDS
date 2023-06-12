#!/usr/bin/env python3


"""Player.py: provides the framework for storing information on baseball players"""

__author__ = "Simon Swanson"
__copyright__ = "Copyright 2015, Simon Swanson"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Simon Swanson"


class Player(object):

    def __init__(self, playerID, fullName, rosterName, birthday, debut, retired):
        self.playerID = playerID
        self.name = rosterName
        self.fullName = fullName
        self.birthday = birthday
        self.debut = debut
        self.retired = retired
        self.seasons = {}
        self.rd2eligible = {"positions": []}

    def __str__(self):
        return "Player(playerID='{pid}', rosterName='{rName}', fullName='{fName}', birthday='{dob}', retired={retired}, seasons={stats})".format(
            pid=self.playerID,
            rName=self.name,
            fName=self.fullName,
            dob=self.birthday,
            retired=self.retired,
            stats=self.seasons)

    def addStats(self, seasonDict, category):
        for season in seasonDict.keys():
            self.addStat(season, seasonDict[season], category)

    def addStat(self, season, seasonStats, category):
        if category not in self.seasons.keys():
            self.seasons[category] = {}
        if year not in self.seasons[category].keys():
            self.seasons[category][year] = {}
        for stat in seasonStats.keys():
            if stat in self.seasons[category][year].keys():
                if self.seasons[category][year][stat] == seasonStats[stat]:
                    print("Replacing {season}'s {stat} value {oldValue} with {newValue}".format(season=season,
                                                                                                stat=stat,
                                                                                                oldValue=self.seasons[
                                                                                                    category][year][stat],
                                                                                                newValue=seasonStats[stat]))
            self.seasons[category][year][stat] = seasonStats[stat]

    def addPositions(self, positionDict):
        self.addStats(positionDict, "fielding")

    def addPosition(self, season, position, gamesPlayed):
        positionDict = {}
        positionDict[position] = gamesPlayed
        self.addStat(season, positionDict, "fielding")

    def clean(self):
        allStats = {
            "batting": ["1b", "2b", "3b", "bb", "cs", "g", "gdp", "hbp", "hr", "ibb", "pa", "r", "rbi", "sb", "sf", "sh", "so"],
            "pitching": ["bb", "bk", "bs", "cg", "er", "g", "gs", "h", "hb", "hld", "hr", "ibb", "ip", "l", "qs", "sho", "so", "sv", "w", "wp"],
            "fielding": ["SP", "RP", "C", "1B", "2B", "3B", "SS", "OF", "CF", "U"]
        }

        for category in self.seasons.keys():
            for year in self.seasons[category].keys():
                for level in self.seasons[category][year].keys():
                    for stat in allStats[category]:
                        if stat not in self.seasons[category][year][level].keys():
                            self.seasons[category][year][level][stat] = 0

        years = sorted(self.seasons["fielding"].keys()).reverse()
        for year in years:
            if "mlb" in self.seasons["fielding"][year].keys():
                for position in self.seasons["fielding"][year]["mlb"]:
                    games = 5 if position == "SP" else 10
                    eligible = self.seasons["fielding"][year]["mlb"][position] >= games
                    if eligible:
                        self.rd2eligible["positions"].append(position)
                if self.rd2eligible["positions"]:
                    break

        # dbEntry = [
        #     "br_player_info": (
        #             self.playerID,
        #             self.fullName,
        #             self.rosterName,
        #             self.birthday,
        #             self.retired,
        #             None
        #     ),
        #     "br_player_index": (

        #     )
        #     "pitching": [],
        #     "fielding": [],
        #     "eligibility": []
        # ]
        dbEntry = {
            "br_player_info": (
                self.playerID,
                self.fullName,
                self.rosterName,
                self.birthday,
                self.retired,
                None
            ),
            "br_player_index": (
                # Add your values here
            ),
            "pitching": [],
            "fielding": [],
            "eligibility": []
        }


def version():
    '''Print module version number'''
    print("Player ({version})".format(version=__version__))
