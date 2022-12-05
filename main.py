import database_manager as db
import examples as eg
import web
import config as cfg
from datetime import datetime


# def gather_players(user, session):

#     print("Gathering available players...")
#     players = {}
#     players.update(web.scan_recent_players(user, session, cfg.steam_api_key))
#     print("Finished gathering players\n")
#     return players


def update_player_stats(players, steam_api_key):

    print("Updating player stats...")
    start_time = datetime.now()

    for player in players:
        players[player].update_stats(steam_api_key)
    db.update_player_stats(players)

    print(
        "Finished updating player stats\n (took "
        + str((datetime.now() - start_time)) + ")"
    )

    return players


# web_auth = web.login(cfg.username, cfg.password)
# user = web_auth[0]
# session = web_auth[1]

# players = gather_players(user, session)
players = eg.players

db.init_database()
update_player_stats(players, cfg.steam_api_key)
