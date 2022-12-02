import requests
import asyncio
import aiohttp
from classes import Player
from bs4 import BeautifulSoup
from steam import webauth


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

    print(
        f"Found {id_counter} raw IDs and {url_counter} vanity URLs.\nNow Converting URLs to SteamIDs...")

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

    print("Scanning player profiles...")

    player_summaries = []
    old_counter = 0
    counter = 100

    while len(recent_players_id_list) / counter > 1:

        players = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_api_key +
                               "&steamids=" + ','. join(map(str, recent_players_id_list[old_counter:counter]))).json()["response"]["players"]

        print(players)

        for profile in players:
            player_summaries.append(profile)

        counter += 100
        old_counter += 100

    players = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_api_key +
                           "&steamids=" + ','. join(map(str, recent_players_id_list[old_counter:counter]))).json()["response"]["players"]

    for profile in players:

        if profile["communityvisibilitystate"] == 3:
            player_summaries.append(profile)

    print("Out of {len(recent_players_id_list)} profiles, "
          + (len(recent_players_id_list) - len(player_summaries))
          + " are private and "
          + len(player_summaries)
          + " are public.")

    for profile in player_summaries:

        recent_players[profile["steamid"]] = Player(profile)

    return recent_players
