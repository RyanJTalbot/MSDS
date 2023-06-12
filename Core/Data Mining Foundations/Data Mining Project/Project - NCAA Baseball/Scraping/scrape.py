#!/usr/bin/env python3


"""statScraper.py: scrapes baseball-reference.com for a large number of statistics and stores them in a database for local use"""

import sys
from SQLController import SQLController
import requests
import re
from Player import Player
from bs4 import BeautifulSoup
import argparse


def iint(string):
    """Tries to interpret input string as integer using builtin 'int' function. If it cannot, returns 0"""
    try:
        return int(string.strip())
    except:
        return 0


def ffloat(string):
    """Tries to interpret input string as floating point number using builtin 'float' function. If it cannot, returns 0"""
    try:
        return float(string.strip())
    except:
        return 0


def parsePlayerProfile(path, args):
    """Creates Player object from stats on the player's profile page on baseball-reference.com"""
    soup = BeautifulSoup(requests.get(
        "{domain}/{pathStr}".format(domain=args.domain[0], pathStr=path)).text, "html.parser")

    playerPathName = re.split("/|\.", path.lower())[-2]
    # set up so a=11, b=12, etc, then joins the values together
    playerID = "".join([char if char.isdigit() else str(
        ord(char) % 86) for char in playerPathName])
    birthday = soup.find("span", id="necro-birth").get("data-birth")
    hasDebuted = soup.find("a", string="Debut")
    debut = isRetired.get("href") if hasDebuted else None
    isRetired = soup.find("a", string="Last Game")
    retired = isRetired.get("href") if isRetired else None

    player = parseProfileHeader(soup, playerID, birthday, debut, retired, args)

    positionTable = soup.find("table", id="standard_fielding")
    positions = parsePositionInfo(positionTable, args)
    player.addPositions(positions)

    hittingTable = soup.find("table", id="batting_standard")
    hittingStats = parseBattingTable(hittingTable, args)
    player.addStats(hittingStats, "batting")

    pitchingTable = soup.find("table", id="pitching_standard")
    advancedPathTag = soup.find("a", href=re.compile(
        r"-pitch.shtml"), string="More Stats")
    pitchingStats = parsePitchingTables(pitchingTable, advancedPathTag, args)
    player.addStats(pitchingStats, "pitching")

    return player


def parseProfileHeader(soup, playerID, birthday, debut, retired, args):
    """Grabs the information to create a basic Player object from a player's baseball-reference.com profile page"""
    nameTag = soup.find("span", id="player_name")
    rosterName = nameTag.string.strip()
    fullName = nameTag.find_parent(
        "div").find_next_sibling("p").strong.string.strip()
    player = Player(playerID, fullName, rosterName, birthday, debut, retired)
    playerString = "Made player profile for {player}".format(
        player=player) if args.verbose else "Starting processing {name}".format(name=rosterName)
    print(playerString)

    return player


def parsePositionInfo(fieldingTable, args):
    """Parses the standard fielding table from baseball-reference.com. Records:
        Year played
        Level played during the year
        Positions played during the year
        Number of games played at each position"""
    if not fieldingTable:
        return {}
    fieldingStats = {}
    fieldingTable = fieldingTable.tbody.find_all(
        "tr", class_=re.compile(r"full"))

    if args.verbose:
        print("Processing {season} seasons of major league fielding stats".format(
            season=len(fieldingTable)))

    for row in fieldingTable:
        seasonStats = {}
        stats = row.find_all("td")
        year = iint(stats[0].find(string=True))
        level = "mlb"
        position = stats[4].string.strip()

        if position == "OF":
            continue

        seasonStats["year"] = year
        seasonStats["age"] = iint(stats[3].find(string=True))
        seasonStats["level"] = level
        seasonStats[position] = {
            "games":   iint(stats[5].find(string=True)),
            "started": iint(stats[6].find(string=True))
        }

        if year not in fieldingStats.keys():
            fieldingStats[year] = {}
        if level not in fieldingStats[year].keys():
            fieldingStats[year][level] = {}
        for key in seasonStats.keys():
            fieldingStats[year][level][key] = seasonStats[key]

    lastYear = sorted(fieldingStats.keys())[-1]
    lastLevel = sorted(fieldingStats[lastYear].keys())[-1]
    if args.verbose:
        print("Processed positions {positions}".format(
            positions=fieldingStats))
    if args.verbose:
        print("Most recent year fielding: {recent}".format(
            recent=fieldingStats[lastYear][lastLevel]))

    finalizedStats = cleanFieldingDict(fieldingStats)

    return finalizedStats


def cleanFieldingDict(fieldingDict):
    fieldingStats = {}
    for year in fieldingDict.keys():
        fieldingStats[year] = {}
        for level in fieldingDict[year].keys():
            fieldingStats[year][level] = {}
            outfieldCount = 0
            outfieldPos = ["CF", "OF", "LF", "RF"]

            for position in fieldingDict[year][level].keys():
                gamesPlayed = fieldingDict[year][level][position]["games"]
                gamesStarted = fieldingDict[year][level][position]["started"]

                if position == "DH":
                    position = "U"

                if position in outfieldPos:
                    outfieldCount += gamesPlayed
                    if position != "CF":
                        continue

                if position == "P":
                    position = "SP"
                    gamesPlayed = gamesPlayed - gamesStarted
                    fieldingStats[year][level][position] = gamesStarted

                    if gamesPlayed <= 0:
                        continue
                    position = "RP"

                fieldingStats[year][level][position] = gamesPlayed

            if outfieldCount > 0:
                fieldingStats[year][level]["OF"] = outfieldCount

    return fieldingStats


def parseBattingTable(battingTable, args):
    """Parses the standard batting table from baseball-reference.com. Records:
        Year played
        Age at the end of the season
        Level played during the year
        Total games played during the season
        Total plate appearances recorded during the year
        Total hits recorded during the year
        Total doubles recorded during the year
        Total triples recorded during the year
        Total home runs recorded during the year
        Total times hit by pitches during the year
        Total runs scored recorded during the year
        Total runs batted in recorded during the year
        Total stolen bases recorded during the year
        Total times caught stealing during the year
        Total times grounded into a double play during the season
        Total sacrifice flies recorded during the year
        Total sacrifice hits recorded during the year
        Total strikeouts recorded during the year
        Total walks recorded during the year
        Total intentional walks recorded during the year"""
    if not battingTable:
        return {}
    battingStats = {}
    battingTable = battingTable.tbody.select("tr.full")

    if args.verbose:
        print("Processing {season} seasons of major league batting stats".format(
            season=len(battingTable)))

    for season in battingTable:
        seasonStats = {}
        stats = season.find_all("td")
        year = iint(stats[0].find(string=True))
        level = "mlb"

        seasonStats["year"] = year
        seasonStats["age"] = iint(stats[1].find(string=True))
        seasonStats["level"] = level
        seasonStats["2b"] = iint(stats[9].find(string=True))
        seasonStats["3b"] = iint(stats[10].find(string=True))
        seasonStats["bb"] = iint(stats[15].find(string=True))
        seasonStats["cs"] = iint(stats[14].find(string=True))
        seasonStats["g"] = iint(stats[4].find(string=True))
        seasonStats["gdp"] = iint(stats[23].find(string=True))
        seasonStats["hbp"] = iint(stats[24].find(string=True))
        seasonStats["hr"] = iint(stats[11].find(string=True))
        seasonStats["ibb"] = iint(stats[27].find(string=True))
        seasonStats["pa"] = iint(stats[5].find(string=True))
        seasonStats["r"] = iint(stats[7].find(string=True))
        seasonStats["rbi"] = iint(stats[12].find(string=True))
        seasonStats["sb"] = iint(stats[13].find(string=True))
        seasonStats["sf"] = iint(stats[26].find(string=True))
        seasonStats["sh"] = iint(stats[25].find(string=True))
        seasonStats["so"] = iint(stats[16].find(string=True))

        hits = iint(stats[8].find(string=True))
        seasonStats["1b"] = hits - seasonStats["2b"] - \
            seasonStats["3b"] - seasonStats["hr"]

        if year not in battingStats.keys():
            battingStats[year] = {}
        if level not in battingStats[year].keys():
            battingStats[year][level] = seasonStats
        for key in seasonStats.keys():
            battingStats[year][level][key] = seasonStats[key]

        if args.verbose:
            print("Processed {season} from {level} level".format(
                season=year, level=level))
        if args.verbose:
            print("{stats}".format(stats=seasonStats))

    return battingStats


def parsePitchingTables(pitchingTable, advancedPathTag, args):
    """Parses the standard and advanced pitching tables from baseball-reference.com. Records:
        Year played
        Age at the end of the season
        Level played during the year
        Total games pitched during the season
        Total games started during the season
        Total innings pitched during the season
        Total wins recorded during the year
        Total losses recorded during the year
        Total quality starts recorded during the year
        Total complete games recorded during the year
        Total shutouts recorded during the year
        Total saves recorded during the year
        Total blown saves recorded during the year
        Total holds recorded during the year
        Total strikeouts recorded during the year
        Total walks allowed during the year
        Total intentional walks recorded during the year
        Total earned runs allowed during the year
        Total hits allowed during the year
        Total home runs allowed during the year
        Total balks recorded during the year
        Total wild pitches recorded during the year"""
    if not pitchingTable:
        return {}
    pitchingStats = {}
    pitchingTable = pitchingTable.tbody.select("tr.full")

    if args.verbose:
        print("Processing {seasons} seasons of major league pitching stats".format(
            seasons=len(pitchingTable)))

    advancedStats = parseAdvancedPitchingTable(advancedPathTag, args)

    for season in pitchingTable:
        seasonStats = {}
        stats = season.find_all("td")
        year = iint(stats[0].find(string=True))
        level = "mlb"

        seasonStats["year"] = year
        seasonStats["age"] = iint(stats[1].find(string=True))
        seasonStats["level"] = level
        seasonStats["bb"] = iint(stats[19].find(string=True))
        seasonStats["bk"] = iint(stats[23].find(string=True))
        seasonStats["cg"] = iint(stats[11].find(string=True))
        seasonStats["er"] = iint(stats[17].find(string=True))
        seasonStats["g"] = iint(stats[8].find(string=True))
        seasonStats["gs"] = iint(stats[9].find(string=True))
        seasonStats["h"] = iint(stats[15].find(string=True))
        seasonStats["hbp"] = iint(stats[22].find(string=True))
        seasonStats["hr"] = iint(stats[18].find(string=True))
        seasonStats["ibb"] = iint(stats[20].find(string=True))
        seasonStats["ip"] = ffloat(stats[14].find(string=True))
        seasonStats["l"] = iint(stats[5].find(string=True))
        seasonStats["sho"] = iint(stats[12].find(string=True))
        seasonStats["so"] = iint(stats[21].find(string=True))
        seasonStats["sv"] = iint(stats[13].find(string=True))
        seasonStats["w"] = iint(stats[4].find(string=True))
        seasonStats["wp"] = iint(stats[24].find(string=True))

        if year in advancedStats.keys() and level in advancedStats[year].keys():
            for key in advancedStats[year][level].keys():
                seasonStats[key] = advancedStats[year][level][key]

        if year not in pitchingStats.keys():
            pitchingStats[year] = {}
        if level not in pitchingStats[year].keys():
            pitchingStats[year][level] = seasonStats
        for key in seasonStats.keys():
            pitchingStats[year][level][key] = seasonStats[key]

        if args.verbose:
            print("Processed {season} from {level} level".format(
                season=year, level=level))
        if args.verbose:
            print("{stats}".format(stats=seasonStats))

    return pitchingStats


def parseAdvancedPitchingTable(advancedPathTag, args):
    """Parses the starting pitching and reliever pitching tables from baseball-reference.com. Records:
        Year played
        Level played during the season
        Total blown saves recorded during the season
        Total holds recorded during the season
        Total quality starts recorded during the season"""
    if not advancedPathTag:
        return {}
    advancedPath = advancedPathTag.get("href")
    soup = BeautifulSoup(requests.get(
        "{domain}/{pathStr}".format(domain=args.domain[0], pathStr=advancedPath)).text, "html.parser")
    relieverTable = soup.find("table", id="pitching_reliever")
    starterTable = soup.find("table", id="pitching_starter")

    advancedStats = {}
    relieverTable = relieverTable.tbody.select(
        "tr.full") if relieverTable else []
    starterTable = starterTable.tbody.select("tr.full") if starterTable else []

    for season in relieverTable:
        seasonStats = {}
        stats = season.find_all("td")
        year = iint(stats[0].find(string=True))
        level = "mlb"

        seasonStats["year"] = year
        seasonStats["level"] = level
        seasonStats["bs"] = iint(stats[11].find(string=True))
        seasonStats["hld"] = iint(stats[14].find(string=True))

        if year not in advancedStats.keys():
            advancedStats[year] = {}
        if level not in advancedStats[year].keys():
            advancedStats[year][level] = {}
        for key in seasonStats.keys():
            advancedStats[year][level][key] = seasonStats[key]

    for season in starterTable:
        seasonStats = {}
        stats = season.find_all("td")
        year = iint(stats[0].find(string=True))
        level = "mlb"

        seasonStats["year"] = year
        seasonStats["level"] = level
        seasonStats["qs"] = iint(stats[18].find(string=True))

        if year not in advancedStats.keys():
            advancedStats[year] = {}
        if level not in advancedStats[year].keys():
            advancedStats[year][level] = {}
        for key in seasonStats.keys():
            advancedStats[year][level][key] = seasonStats[key]

    return advancedStats


def parsePlayerIndex(args):
    """Parses a list of links to indexes of player profiles from baseball-reference.com"""
    paths = []
    soup = BeautifulSoup(requests.get(
        "{domain}/players/".format(domain=args.domain[0])).text, "html.parser")

    lettersTags = soup.select("tr td.xx_large_text.bold_text a[href]")
    [paths.append(tag.get("href")) for tag in lettersTags]
    if args.verbose:
        print("Found {numPaths} last names indices to search".format(
            numPaths=len(paths)))

    return paths


def parseLetterIndex(path, args):
    """Parses a list of links of player profiles from baseball-reference.com"""
    paths = []
    soup = BeautifulSoup(requests.get(
        "{domain}/{pathStr}".format(domain=args.domain[0], pathStr=path)).text, "html.parser")

    playerTags = soup.select("blockquote pre a[href]")
    # when updating, run check aginst DB here on which players to process
    [paths.append(tag.get("href")) for tag in playerTags]
    if args.verbose:
        print("Found {numPaths} players to process".format(
            numPaths=len(paths)))

    return paths


def parseArgs(args):
    """Parses command line arguments given to the program"""
    parser = argparse.ArgumentParser(
        description="Scrapes baseball-reference.com for player statistics")

    parser.add_argument("-d", "--domain", help="domain to scrape for statistics. Default is baseball-reference.com",
                        nargs=1, default=["http://www.baseball-reference.com"])
    parser.add_argument("-f", "--filename", help="database file to store data in",
                        required=True, nargs=1, type=argparse.FileType("r+"))
    parser.add_argument(
        "-r", "--reset", help="removes database before scraping all data from baseball-reference. Conflicts with -u. One of -r and -u must be specified", action="store_true")
    parser.add_argument(
        "-u", "--update", help="scrapes baseball-reference and adds all new information to the database. Conflicts with -r. One of -r and -u must be specified", action="store_true")
    parser.add_argument(
        "--verbose", help="enables verbose output", action="store_true")
    parser.add_argument("--version", help="prints out version and exits",
                        action="version", version="%(prog)s ({version})".format(version=__version__))

    parsedArgs = parser.parse_args()

    if parsedArgs.reset == parsedArgs.update:
        parser.error(
            "-r and -u are conflicting flags. Exactly one must be specified")
        parser.print_help()

    return parsedArgs


def scrapePlayerData(args, sqlController):
    playerIDs = []
    letters = parsePlayerIndex(args)
    for letter in letters[:1]:
        profiles = parseLetterIndex(letter, args)
        for profile in profiles[:2]:
            player = parsePlayerProfile(profile, args)


def main(args):
    """Scrapes baseball-reference.com and enters player information into a database"""
    sqlController = SQLController(args.filename)
    if args.reset:
        confirm = input(
            "Are you sure you want to wipe the database? (y/N) ").lower()
        if confirm == "y" or confirm == "yes":
            print("Wiping database")
            sqlController.resetDB()
            scrapePlayerData(args, sqlController)
        else:
            print("Not wiping database. Exiting.")
    else:
        scrapePlayerData(args, sqlController)
    sqlController.exit()


if __name__ == "__main__":
    parsedArgs = parseArgs(sys.argv)
    main(parsedArgs)
