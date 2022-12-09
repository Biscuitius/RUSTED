import os
from datetime import datetime
import config as cfg
import web
import examples as eg
import database_manager as db

start_time = datetime.now()

os.chdir("OneDrive\\Coding\\Rust-Advanced-Tracking-System")


def gather_players(user, session):

    print("Searching for players...")

    players = {}
    players.update(web.scan_recent_players(user, session, cfg.steam_api_key))

    return players


def discard_privates(players):

    print("Discarding private profiles...")

    pop_list = []

    for player in players.values():
        if len(player.stats) == 0:
            pop_list.append(player.steamid)

    for player in pop_list:
        players.pop(player)

    print(
        str(len(pop_list))
        + " profiles have hidden stats and were discarded.\n"
    )


def update_players(players, steam_api_key):

    print("Updating player stats...\n")

    web.update_player_stats(players, steam_api_key)
    discard_privates(players)
    db.update_players(players)

    print("Finished updating player stats.\n")


web_auth = web.login(cfg.username, cfg.password)
user = web_auth[0]
session = web_auth[1]

db.init_database()

players = gather_players(user, session)
# players = eg.players

update_players(players, cfg.steam_api_key)

print(
    "App initialisation finished (took "
    + str((datetime.now() - start_time)) + ").\n"
)
