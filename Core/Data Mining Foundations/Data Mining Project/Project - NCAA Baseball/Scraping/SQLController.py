#!/usr/bin/env python3


"""SQLController.py: provides the framework for storing and retrieving player data from a sqlite database"""

__author__      = "Simon Swanson"
__copyright__   = "Copyright 2015, Simon Swanson"
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Simon Swanson"


from Player import Player
import sqlite3


class SQLController(object):

    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cur  = self.conn.cursor()

    def __del__(self):
        '''Exits a database connection safely'''
        self.conn.close()

    def exit(self):
        '''Exits a database connection safely'''
        del(self)

    def makeTables(self):
        '''Creates all the tables for storing player data'''
        self.run("""create table if not exists rd2_team_info(
            team_name   text not null,
            division    text not null,
            owner_name  text not null,
            owner_email text,
            owner_phone text,
            reddit_name text not null,
            primary key (team_name)
        )""")
        self.run("""create table if not exists br_player_info(
            br_id       integer not null,
            full_name   text    not null,
            roster_name text    not null,
            birthday    text    not null,
            retired     integer,
            rd2_team    text,
            foreign key (rd2_team) references rd2_team_info(team_name),
            primary key (br_id)
        )""")
        self.run("""create table if not exists br_player_index(
            br_id       integer not null,
            debut_year  integer not null,
            latest_year integer not null,
            foreign key (br_id) references br_player_info(br_id),
            primary key (br_id, debut_year)
        )""")
        self.run("""create table if not exists br_season_index(
            br_id integer not null,
            year  integer not null,
            age   integer not null,
            foreign key (br_id) references br_player_info(br_id),
            primary_key (br_id, year)
        )""")
        self.run("""create table if not exists br_batting_stats(
            br_id integer not null,
            year  integer not null,
            1b    integer not null,
            2b    integer not null,
            3b    integer not null,
            bb    integer not null,
            cs    integer not null,
            gdb   integer not null,
            g     integer not null,
            hbp   integer not null,
            hr    integer not null,
            ibb   integer not null,
            pa    integer not null,
            r     integer not null,
            rbi   integer not null,
            sb    integer not null,
            sf    integer not null,
            sh    integer not null,
            so    integer not null,
            foreign key (br_id) references br_season_index(br_id),
            foreign key (year)  references br_season_index(year),
            primary key (br_id, year)
        )""")
        self.run("""create table if not exists br_pitching_stats(
            br_id integer not null,
            year  integer not null,
            bb    integer not null,
            bk    integer not null,
            bs    integer not null,
            cg    integer not null,
            er    integer not null,
            g     integer not null,
            gs    integer not null,
            h     integer not null,
            hb    integer not null,
            hld   integer not null,
            hr    integer not null,
            ibb   integer not null,
            ip    real    not null,
            l     integer not null,
            qs    integer not null,
            sho   integer not null,
            so    integer not null,
            sv    integer not null,
            w     integer not null,
            wp    integer not null,
            foreign key (br_id) references br_season_index(br_id),
            foreign key (year)  references br_season_index(year),
            primary key (br_id, year)
        )""")
        self.run("""create table if not exists br_position_info(
            br_id integer not null,
            year  integer not null,
            sp    integer not null,
            rp    integer not null,
            c     integer not null,
            1b    integer not null,
            2b    integer not null,
            3b    integer not null,
            ss    integer not null,
            of    integer not null,
            cf    integer not null,
            u     integer not null,
            foreign key (br_id) references br_season_index(br_id),
            foreign key (year)  references br_season_index(year),
            primary key (br_id, year)
        )""")
        self.run("""create table if not exists rd2_player_info(
            br_id     integer not null,
            team_name text,
            status    text,
            grad_year integer,
            positions text,
            foreign key (br_id)     references br_player_info(br_id),
            foreign key (team_name) references rd2_team_info(name),
            primary key (br_id)
        )""", True)

    def resetDB(self):
        '''Don't use this function. This is a very dangerous operation but is possibly necessary'''
        self.cur.execute("drop table if exists br_reddit_dynasty_info")
        self.cur.execute("drop table if exists br_hitting_stats")
        self.cur.execute("drop table if exists br_pitching_stats")
        self.cur.execute("drop table if exists br_position_info")
        self.cur.execute("drop table if exists br_season_info")
        self.cur.execute("drop table if exists br_player_index")
        self.cur.execute("drop table if exists br_player_info")
        self.conn.commit()
        print("All player information removed from database")
        self.makeTables()
        print("Successfully reset database")

    def query(self, arg):
        '''Runs a query against the database and returns the result'''
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def run(self, arg, commit=False):
        '''Runs a command against the database. Commiting is optional'''
        self.cur.execute(arg)
        if commit: self.conn.commit()


def reddityDynastyOwners():
    owners = [
        ("Angels", "AL West", "Jeff Schultz", "", "", "reddit"),
        ("San Diego Padres", "National League West", "Simon Swanson", "nomiswanson@gmail.com", "971-258-0864", "badfoodman")
    ]
    return owners


def version():
    print("Player ({version})".format(version=__version__))
