import battlemetrics as bm
import database_manager as dbman
import examples as eg
import web
import config as cfg

from datetime import datetime


def gather_players(user, session):

    print("Gathering available players...")
    players = {}
    players.update(web.scan_recent_players(user, session, steam_api_key))
    print("Finished gathering players\n")
    return players


def update_bmids(players, server):

    print("Updating player BMIDs...")
    for player in players:
        players[player].bmid = bm.search_for_player(
            players[player].name, server)
    print("Finished updating player BMIDs\n")
    return players


def update_player_stats(players, steam_api_key):

    print("Updating player stats...")
    start_time = datetime.now()
    for player in players:
        if players[player].visibility == 3:
            players[player].update_stats(steam_api_key)
    time_taken = datetime.now() - start_time
    print(f"Finished updating player stats\n (took {time_taken})")
    return players


web_auth = web.login(cfg.username, cfg.password)
user = web_auth[0]
session = web_auth[1]

players = gather_players(user, session)
players = eg.players

update_player_stats(players, cfg.steam_api_key)
update_bmids(players, cfg.server)
