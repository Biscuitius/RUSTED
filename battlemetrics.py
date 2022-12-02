import requests
import time
from datetime import datetime, timedelta
from classes import Player

personal_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImYxMTMxMDMwMDRhOTM4ZTMiLCJpYXQiOjE2NjcyNDA0MjcsIm5iZiI6MTY2NzI0MDQyNywiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjoxOTc1NzUifQ.dWNwz8_egTs9xUY0coVtRLYdQQSL-wMycd2mYmKC1Zc"
headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImYxMTMxMDMwMDRhOTM4ZTMiLCJpYXQiOjE2NjcyNDA0MjcsIm5iZiI6MTY2NzI0MDQyNywiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjoxOTc1NzUifQ.dWNwz8_egTs9xUY0coVtRLYdQQSL-wMycd2mYmKC1Zc"}


def get_server_info(server_name):

    server_data = requests.get(
        url=f"https://api.battlemetrics.com/servers/{server_name}?include=player,identifier", headers=headers)

    server_info = {
        "Name": server_data.json()["data"]["attributes"]["name"],
        "IP": str(server_data.json()["data"]["attributes"]["address"]),
        "Port": str(server_data.json()["data"]["attributes"]["port"]),
        "Players": server_data.json()["data"]["attributes"]["players"],
        "Max": server_data.json()["data"]["attributes"]["maxPlayers"],
        "Queue": server_data.json()["data"]["attributes"]["details"]["rust_queued_players"],
        "Map Size": server_data.json()["data"]["attributes"]["details"]["rust_world_size"],
        "Map Seed": server_data.json()["data"]["attributes"]["details"]["rust_world_seed"],
        "Steam ID": server_data.json()["data"]["attributes"]["details"]["serverSteamId"],
    }

    server_players = {}

    for player in server_data.json()["included"]:
        if player["type"] == "player":
            server_players[player["id"]] = player["attributes"]["name"]
        elif player["type"] == "identifier":
            server_players[player["relationships"]["player"]
                           ["data"]["id"]] = player["attributes"]["identifier"]

    return server_info, server_players


def search_for_player(player_name, server_name):
    search = requests.get(
        url=f"https://api.battlemetrics.com/players?filter%5Bsearch%5D=%22{player_name}%22&filter%5BplayerFlags%5D=&filter%5Bserver%5D%5Bsearch%5D=%22{server_name}%22&filter%5Bserver%5D%5Bgame%5D=rust&sort=-lastSeen",
        headers=headers
    ).json()
    try:
        if len(search["data"]) == 0:
            print("No matches found, aborting")
        elif len(search["data"]) > 1:
            match_list = {}
            for bm_profile in search["data"]:
                if bm_profile['attributes']['name'] == player_name:
                    match_list[bm_profile["id"]
                               ] = bm_profile["attributes"]["name"]
            if len(match_list) == 1:
                player_bmid = list(match_list.keys())[0]
                return player_bmid
            else:
                print("Multiple matches found, manual search required")
                for match in match_list:
                    print(f"{match} - {match_list[match]}")
        else:
            player_bmid = search["data"][0]["id"]
            print(f"BMID of {player_name} is {player_bmid}")
            return player_bmid
    except:
        print(search)


def get_player_info(player_bmid, server_id):

    player_data = requests.get(
        url=f"https://api.battlemetrics.com/players/{player_bmid}/relationships/sessions", headers=headers)
    found_username = False
    player_info = {"Sessions": [], "Online": False}
    previous_session_end = None

    for session in reversed(player_data.json()["data"][:5]):
        if session["relationships"]["server"]["data"]["id"] == server_id:
            if not found_username:
                player_info["Name"] = session["attributes"]["name"]
                player_info["Combat ID"] = session["relationships"]["identifiers"]["data"][0]["id"]
                player_info["BatMet ID"] = session["relationships"]["player"]["data"]["id"]
                found_username = True
            if session["attributes"]["stop"] is None:
                if previous_session_end is None:
                    player_info["Sessions"].insert(0, {
                        "Start": datetime.fromisoformat(session["attributes"]["start"][:19]) + timedelta(hours=time.localtime().tm_isdst),
                        "Stop": "Now"

                    })
                else:
                    time_since_last_session = (datetime.fromisoformat(
                        session["attributes"]["start"][:19]) + timedelta(hours=time.localtime().tm_isdst)) - previous_session_end
                    if time_since_last_session < timedelta(hours=1):
                        player_info["Sessions"][0]["Stop"] = "Now"
                    else:
                        player_info["Sessions"].insert(0, {
                            "Start": datetime.fromisoformat(session["attributes"]["start"][:19]) + timedelta(
                                hours=time.localtime().tm_isdst),
                            "Stop": "Now"
                        })
                break
            elif previous_session_end is None:
                player_info["Sessions"].insert(0, {
                    "Start": datetime.fromisoformat(session["attributes"]["start"][:19]) + timedelta(
                        hours=time.localtime().tm_isdst),
                    "Stop": datetime.fromisoformat(session["attributes"]["stop"][:19]) + timedelta(
                        hours=time.localtime().tm_isdst)
                })
                previous_session_end = player_info["Sessions"][0]["Stop"]
            else:
                time_since_last_session = (datetime.fromisoformat(
                    session["attributes"]["start"][:19]) + timedelta(hours=time.localtime().tm_isdst)) - previous_session_end
                if time_since_last_session < timedelta(hours=1):
                    player_info["Sessions"][0]["Stop"] = (
                        datetime.fromisoformat(session["attributes"]["stop"][:19]))
                else:
                    player_info["Sessions"].insert(0, {
                        "Start": datetime.fromisoformat(session["attributes"]["start"][:19]) + timedelta(hours=time.localtime().tm_isdst),
                        "Stop": datetime.fromisoformat(session["attributes"]["stop"][:19]) + timedelta(hours=time.localtime().tm_isdst)
                    })
                    previous_session_end = player_info["Sessions"][0]["Stop"]
    player_info["Last Seen"] = player_info["Sessions"][0]["Stop"]

    return player_info
