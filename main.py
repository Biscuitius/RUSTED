import database_manager as db
import examples as eg
import web
import config as cfg
from datetime import datetime
import os

os.chdir("OneDrive\\Coding\\Rust-Advanced-Tracking-System")


def gather_players(user, session):

    print("Searching for players...")

    players = {}
    players.update(web.scan_recent_players(user, session, cfg.steam_api_key))

    return players


def update_player_stats(players, steam_api_key):

    print("Updating player stats...")
    start_time = datetime.now()

    player_pop_list = []

    for player in players.values():
        player_pop_list.extend(player.update_stats(steam_api_key))

    for player in player_pop_list:
        players.pop(player, None)

    print(
        "Finished updating player stats\n (took "
        + str((datetime.now() - start_time)) + ").\n"
    )

    db.update_players(players)


def update_player(steamid):
    update_player_stats(
        {"Player": players[steamid]},
        cfg.steam_api_key)


web_auth = web.login(cfg.username, cfg.password)
user = web_auth[0]
session = web_auth[1]

db.init_database()

players = gather_players(user, session)
# players = eg.players

update_player_stats(players, cfg.steam_api_key)
