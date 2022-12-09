import requests
import asyncio
import aiohttp
from classes import Player
from bs4 import BeautifulSoup
from steam import webauth


def login(username, password):
    print("Connecting to Steam website...")
    user = webauth.WebAuth(username)
    session = user.cli_login(password)
    print("\nSuccessfully logged in.\n")
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
        "Found "
        + str(id_counter)
        + " raw IDs and "
        + str(url_counter)
        + " vanity URLs.\n")

    print("Converting URLs to SteamIDs...")

    def get_tasks(url_list, session, steam_api_key):

        tasks = []

        for URL in url_list:
            tasks.append(asyncio.create_task(session.get(
                "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steam_api_key + "&vanityurl=" + URL)))

        print(
            "Converted "
            + str(len(url_list))
            + " URLs to SteamIDs.\n")

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

        for profile in players:
            if profile["communityvisibilitystate"] == 3:
                player_summaries.append(profile)

        counter += 100
        old_counter += 100

    players = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_api_key +
                           "&steamids=" + ','. join(map(str, recent_players_id_list[old_counter:counter]))).json()["response"]["players"]

    for profile in players:
        if profile["communityvisibilitystate"] == 3:
            player_summaries.append(profile)

    print(
        "Gathered "
        + str(len(recent_players_id_list))
        + " profiles, "
        + str((len(recent_players_id_list) - len(player_summaries)))
        + " are private and "
        + str(len(player_summaries))
        + " are public.\n"
        + "Private profiles are discarded.\n"
    )

    for profile in player_summaries:

        recent_players[profile["steamid"]] = Player(profile)

    return recent_players


def update_player_stats(players, steam_api_key):

    def get_tasks(players, session, steam_api_key):

        tasks = []

        for player in players:
            tasks.append(asyncio.create_task(session.get(
                "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key="
                + steam_api_key
                + "&steamid="
                + player)))

        return tasks

    stat_responses = []

    async def get_stats(players):
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(players, session, steam_api_key)
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for response in responses:
                stat_responses.append(await response.json())

    asyncio.run(get_stats(players))

    raw_stats = {}

    for response in stat_responses:

        if response and "playerstats" in response:

            for stat in response["playerstats"]["stats"]:
                raw_stats[stat["name"]] = stat["value"]

            players[response["playerstats"]["steamID"]].stats = {}

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Metal Ore Harvested"] = int(raw_stats["acquired_metal.ore"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Metal Ore Harvested"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Stone Harvested"] = int(raw_stats["harvested_stones"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Stone Harvested"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Wood Harvested"] = int(raw_stats["harvested_wood"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Wood Harvested"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Scrap Acquired"] = int(raw_stats["acquired_scrap"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Scrap Acquired"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Cloth Harvested"] = int(raw_stats["harvested_cloth"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Cloth Harvested"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Lowgrade Acquired"] = int(raw_stats["acquired_lowgradefuel"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Lowgrade Acquired"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Leather Harvested"] = int(raw_stats["harvested_leather"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Leather Harvested"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Barrels Broken"] = int(raw_stats["destroyed_barrels"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Barrels Broken"] = 0

            try:
                players[response["playerstats"]["steamID"]].stats["Animals Killed"] = (
                    + int(raw_stats["kill_bear"])
                    + int(raw_stats["kill_boar"])
                    + int(raw_stats["kill_stag"])
                    + int(raw_stats["kill_chicken"])
                    + int(raw_stats["kill_wolf"]))
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Animals Killed"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Players Killed"] = int(raw_stats["kill_player"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Players Killed"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Headshots Hit"] = int(raw_stats["headshot"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Headshots Hit"] = 0

            try:
                players[response["playerstats"]["steamID"]].stats["Bullets Fired"] = int(
                    raw_stats["bullet_fired"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Bullets Fired"] = 0

            try:
                players[response["playerstats"]["steamID"]].stats["Bullets Hit"] = (
                    + int(raw_stats["bullet_hit_player"])
                    + int(raw_stats["bullet_hit_boar"])
                    + int(raw_stats["bullet_hit_bear"])
                    + int(raw_stats["bullet_hit_wolf"])
                    + int(raw_stats["bullet_hit_stag"])
                    + int(raw_stats["bullet_hit_entity"]))
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Bullets Hit"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Deaths"] = int(raw_stats["deaths"])
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Deaths"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Rockets Fired"] = int(raw_stats["rocket_fired"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Rockets Fired"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Grenades Thrown"] = int(raw_stats["grenades_thrown"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Grenades Thrown"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Arrows Shot"] = int(raw_stats["arrows_shot"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Arrows Shot"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Arrows Hit"] = (
                    + int(raw_stats["arrow_hit_player"])
                    + int(raw_stats["arrow_hit_boar"])
                    + int(raw_stats["arrow_hit_bear"])
                    + int(raw_stats["arrow_hit_wolf"])
                    + int(raw_stats["arrow_hit_stag"])
                    + int(raw_stats["arrow_hit_chicken"])
                    + int(raw_stats["arrow_hit_entity"]))
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Arrows Hit"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Shotguns Fired"] = int(raw_stats["shotgun_fired"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Shotguns Fired"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Wounded"] = int(raw_stats["wounded"])
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Wounded"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Been Picked Up"] = int(raw_stats["wounded_assisted"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Been Picked Up"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Picked up Other"] = int(raw_stats["wounded_healed"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Picked up Other"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Suicides"] = int(raw_stats["death_suicide"])
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Suicides"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Builds Placed"] = int(raw_stats["placed_blocks"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Builds Placed"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Builds Upgraded"] = int(raw_stats["upgraded_blocks"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Builds Upgraded"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Time Cold"] = int(raw_stats["cold_exposure_duration"])
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Time Cold"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Time Hot"] = int(raw_stats["hot_exposure_duration"])
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Time Hot"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Time on Roads"] = int(raw_stats["topology_road_duration"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Time on Roads"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Distance on Horses"] = int(raw_stats["horse_distance_ridden_km"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Distance on Horses"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Blueprints Learnt"] = int(raw_stats["blueprint_studied"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Blueprints Learnt"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Times Waved"] = int(raw_stats["gesture_wave_count"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Times Waved"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Food Eaten"] = int(raw_stats["calories_consumed"])
            except KeyError:
                players[response["playerstats"]
                        ["steamID"]].stats["Food Eaten"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Water Drunk"] = int(raw_stats["water_consumed"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Water Drunk"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Time Speaking (s)"] = int(raw_stats["seconds_speaking"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Time Speaking (s)"] = 0

            try:
                players[response["playerstats"]["steamID"]].stats["Notes Played"] = (
                    + int(raw_stats["InstrumentNotesPlayed"])
                    + int(raw_stats["InstrumentNotesPlayedBinds"]))
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Notes Played"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Scientists Killed"] = int(raw_stats["kill_scientist"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Scientists Killed"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Deaths by AI"] = int(raw_stats["death_entity"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Deaths by AI"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Helipad Landings"] = int(raw_stats["helipad_landings"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Helipad Landings"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Cargo Bridge Visits"] = int(raw_stats["cargoship_bridge_visits"])
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Cargo Bridge Visits"] = 0

            try:
                players[response["playerstats"]["steamID"]
                        ].stats["Deaths by Animals"] = (
                            + int(raw_stats["death_wolf"])
                            + int(raw_stats["death_bear"]))
            except KeyError:
                players[response["playerstats"]["steamID"]
                        ].stats["Deaths by Animals"] = 0
