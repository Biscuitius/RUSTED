import requests
import asyncio
import aiohttp
import time
from classes import Player
from bs4 import BeautifulSoup
from steam import webauth
from datetime import datetime, timezone, timedelta

Personal_Key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImYxMTMxMDMwMDRhOTM4ZTMiLCJpYXQiOjE2NjcyNDA0MjcsIm5iZiI6MTY2NzI0MDQyNywiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjoxOTc1NzUifQ.dWNwz8_egTs9xUY0coVtRLYdQQSL-wMycd2mYmKC1Zc"
Headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImYxMTMxMDMwMDRhOTM4ZTMiLCJpYXQiOjE2NjcyNDA0MjcsIm5iZiI6MTY2NzI0MDQyNywiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjoxOTc1NzUifQ.dWNwz8_egTs9xUY0coVtRLYdQQSL-wMycd2mYmKC1Zc"}


def login(username, password):
    print("Logging in...")
    user = webauth.WebAuth(username)
    session = user.cli_login(password)
    print("Successfully logged in\n")
    return user, session


def scan_recent_players(user, session, steam_api_key):

    page = session.get(user.steam_id.community_url +
                       "/friends/coplay?ajax=1").text
    soup = BeautifulSoup(page, "html.parser")

    recent_players_id_list = []
    url_list = []
    recent_players = {}

    counter = 0
    id_counter = 0
    url_counter = 0

    for link in soup.find_all('a', href=True):
        url = link.get("href")

        if url:

            if url.startswith("https://steamcommunity.com/profiles/"):

                counter += 1
                id_counter += 1
                recent_players_id_list.append(url[36:])

            elif url.startswith("https://steamcommunity.com/id/"):

                counter += 1
                url_counter += 1
                url_list.append(url[30:])

    print(f"Found {counter} players, of which {id_counter} are raw IDs and {url_counter} are URLS that must be converted")

    def get_tasks(url_list, session, steam_api_key):
        tasks = []
        for URL in url_list:
            tasks.append(asyncio.create_task(session.get(
                "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steam_api_key + "&vanityurl=" + URL)))
        print(f"Converted {len(url_list)} URLs to SteamIDs")
        return tasks

    resolve_url_responses = []

    async def convert_urls(url_list):
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(url_list, session, steam_api_key)
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for response in responses:
                resolve_url_responses.append(await response.json(content_type="application/json"))

    asyncio.run(convert_urls(url_list))

    for response in resolve_url_responses:
        recent_players_id_list.append(response["response"]["steamid"])

    print(f"{len(recent_players_id_list)} total profiles available")

    player_summaries = []
    old_counter = 0
    counter = 100

    while len(recent_players_id_list) / counter > 1:

        players = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_api_key +
                               "&steamids=" + ','. join(map(str, recent_players_id_list[old_counter:counter]))).json()["response"]["players"]

        for profile in players:
            player_summaries.append(profile)

        counter += 100
        old_counter += 100

    players = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_api_key +
                           "&steamids=" + ','. join(map(str, recent_players_id_list[old_counter:counter]))).json()["response"]["players"]

    for profile in players:

        player_summaries.append(profile)

    print(f"{len(player_summaries)} profiles successfully processed")

    for profile in player_summaries:

        recent_players[profile["steamid"]] = Player(profile)

    return recent_players


def get_server_info(server_bmid):

    server_data = requests.get(
        url=f"https://api.battlemetrics.com/servers/{server_bmid}?include=player,identifier", headers=headers)

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

    return server_info


def get_bm_player_info(player_bmid, server_id):

    player_data = requests.get(
        url=f"https://api.battlemetrics.com/players/{player_bmid}/relationships/sessions", headers=Headers)

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
