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
                if response:
                    stat_responses.append(await response.json())
                else:
                    print("ERROR")

    asyncio.run(get_stats(players))

    raw_stats = {}

    for response in stat_responses:

        if response and "playerstats" in response:

            steamid = response["playerstats"]["steamID"]

            for stat in response["playerstats"]["stats"]:
                raw_stats[stat["name"]] = stat["value"]

            players[steamid].stats = {}

            try:
                players[steamid].stats["Metal Ore Harvested"] = int(
                    raw_stats["acquired_metal.ore"])
            except KeyError:
                players[steamid].stats["Metal Ore Harvested"] = 0

            try:
                players[steamid].stats["Stone Harvested"] = int(
                    raw_stats["harvested_stones"])
            except KeyError:
                players[steamid].stats["Stone Harvested"] = 0

            try:
                players[steamid].stats["Wood Harvested"] = int(
                    raw_stats["harvested_wood"])
            except KeyError:
                players[steamid].stats["Wood Harvested"] = 0

            try:
                players[steamid].stats["Scrap Acquired"] = int(
                    raw_stats["acquired_scrap"])
            except KeyError:
                players[steamid].stats["Scrap Acquired"] = 0

            try:
                players[steamid].stats["Cloth Harvested"] = int(
                    raw_stats["harvested_cloth"])
            except KeyError:
                players[steamid].stats["Cloth Harvested"] = 0

            try:
                players[steamid].stats["Lowgrade Acquired"] = int(
                    raw_stats["acquired_lowgradefuel"])
            except KeyError:
                players[steamid].stats["Lowgrade Acquired"] = 0

            try:
                players[steamid].stats["Leather Harvested"] = int(
                    raw_stats["harvested_leather"])
            except KeyError:
                players[steamid].stats["Leather Harvested"] = 0

            try:
                players[steamid].stats["Barrels Broken"] = int(
                    raw_stats["destroyed_barrels"])
            except KeyError:
                players[steamid].stats["Barrels Broken"] = 0

            players[steamid].stats["Animals Killed"] = 0

            for stat in [
                    "kill_bear",
                    "kill_boar",
                    "kill_stag",
                    "kill_chicken",
                    "kill_wolf"
            ]:
                try:
                    players[steamid].stats["Animals Killed"] += int(
                        raw_stats[stat])
                except KeyError:
                    pass

            try:
                players[steamid].stats["Players Killed"] = int(
                    raw_stats["kill_player"])
            except KeyError:
                players[steamid].stats["Players Killed"] = 0

            try:
                players[steamid].stats["Headshots Hit"] = int(
                    raw_stats["headshot"])
            except KeyError:
                players[steamid].stats["Headshots Hit"] = 0

            try:
                players[steamid].stats["Bullets Fired"] = int(
                    raw_stats["bullet_fired"])
            except KeyError:
                players[steamid].stats["Bullets Fired"] = 0

            players[steamid].stats["Bullets Hit"] = 0

            for stat in [
                "bullet_hit_player",
                "bullet_hit_boar",
                "bullet_hit_bear",
                "bullet_hit_wolf",
                "bullet_hit_stag",
                "bullet_hit_entity"
            ]:
                try:
                    players[steamid].stats["Bullets Hit"] += int(
                        raw_stats[stat])
                except KeyError:
                    pass

            try:
                players[steamid].stats["Deaths"] = int(
                    raw_stats["deaths"])
            except KeyError:
                players[steamid].stats["Deaths"] = 0

            try:
                players[steamid].stats["Rockets Fired"] = int(
                    raw_stats["rocket_fired"])
            except KeyError:
                players[steamid].stats["Rockets Fired"] = 0

            try:
                players[steamid].stats["Grenades Thrown"] = int(
                    raw_stats["grenades_thrown"])
            except KeyError:
                players[steamid].stats["Grenades Thrown"] = 0

            try:
                players[steamid].stats["Arrows Shot"] = int(
                    raw_stats["arrows_shot"])
            except KeyError:
                players[steamid].stats["Arrows Shot"] = 0

            players[steamid].stats["Arrows Hit"] = 0

            for stat in [
                "arrow_hit_player",
                "arrow_hit_boar",
                "arrow_hit_bear",
                "arrow_hit_wolf",
                "arrow_hit_stag",
                "arrow_hit_chicken",
                "arrow_hit_entity"
            ]:
                try:
                    players[steamid].stats["Arrows Hit"] += int(
                        raw_stats[stat])
                except KeyError:
                    pass

            try:
                players[steamid].stats["Shotguns Fired"] = int(
                    raw_stats["shotgun_fired"])
            except KeyError:
                players[steamid].stats["Shotguns Fired"] = 0

            try:
                players[steamid].stats["Wounded"] = int(
                    raw_stats["wounded"])
            except KeyError:
                players[steamid].stats["Wounded"] = 0

            try:
                players[steamid].stats["Been Picked Up"] = int(
                    raw_stats["wounded_assisted"])
            except KeyError:
                players[steamid].stats["Been Picked Up"] = 0

            try:
                players[steamid].stats["Picked up Other"] = int(
                    raw_stats["wounded_healed"])
            except KeyError:
                players[steamid].stats["Picked up Other"] = 0

            try:
                players[steamid].stats["Suicides"] = int(
                    raw_stats["death_suicide"])
            except KeyError:
                players[steamid].stats["Suicides"] = 0

            try:
                players[steamid].stats["Builds Placed"] = int(
                    raw_stats["placed_blocks"])
            except KeyError:
                players[steamid].stats["Builds Placed"] = 0

            try:
                players[steamid].stats["Builds Upgraded"] = int(
                    raw_stats["upgraded_blocks"])
            except KeyError:
                players[steamid].stats["Builds Upgraded"] = 0

            try:
                players[steamid].stats["Time Cold"] = int(
                    raw_stats["cold_exposure_duration"])
            except KeyError:
                players[steamid].stats["Time Cold"] = 0

            try:
                players[steamid].stats["Time Hot"] = int(
                    raw_stats["hot_exposure_duration"])
            except KeyError:
                players[steamid].stats["Time Hot"] = 0

            try:
                players[steamid].stats["Time on Roads"] = int(
                    raw_stats["topology_road_duration"])
            except KeyError:
                players[steamid].stats["Time on Roads"] = 0

            try:
                players[steamid].stats["Distance on Horses"] = int(
                    raw_stats["horse_distance_ridden_km"])
            except KeyError:
                players[steamid].stats["Distance on Horses"] = 0

            try:
                players[steamid].stats["Blueprints Learnt"] = int(
                    raw_stats["blueprint_studied"])
            except KeyError:
                players[steamid].stats["Blueprints Learnt"] = 0

            try:
                players[steamid].stats["Times Waved"] = int(
                    raw_stats["gesture_wave_count"])
            except KeyError:
                players[steamid].stats["Times Waved"] = 0

            try:
                players[steamid].stats["Food Eaten"] = int(
                    raw_stats["calories_consumed"])
            except KeyError:
                players[steamid].stats["Food Eaten"] = 0

            try:
                players[steamid].stats["Water Drunk"] = int(
                    raw_stats["water_consumed"])
            except KeyError:
                players[steamid].stats["Water Drunk"] = 0

            try:
                players[steamid].stats["Time Speaking (s)"] = int(
                    raw_stats["seconds_speaking"])
            except KeyError:
                players[steamid].stats["Time Speaking (s)"] = 0

            players[steamid].stats["Notes Played"] = 0

            for stat in [
                "InstrumentNotesPlayed",
                "InstrumentNotesPlayedBinds"
            ]:
                try:
                    players[steamid].stats["Notes Played"] += int(
                        raw_stats[stat])
                except KeyError:
                    pass

            try:
                players[steamid].stats["Scientists Killed"] = int(
                    raw_stats["kill_scientist"])
            except KeyError:
                players[steamid].stats["Scientists Killed"] = 0

            try:
                players[steamid].stats["Deaths by AI"] = int(
                    raw_stats["death_entity"])
            except KeyError:
                players[steamid].stats["Deaths by AI"] = 0

            try:
                players[steamid].stats["Helipad Landings"] = int(
                    raw_stats["helipad_landings"])
            except KeyError:
                players[steamid].stats["Helipad Landings"] = 0

            try:
                players[steamid].stats["Cargo Bridge Visits"] = int(
                    raw_stats["cargoship_bridge_visits"])
            except KeyError:
                players[steamid].stats["Cargo Bridge Visits"] = 0

            players[steamid].stats["Deaths by Animals"] = 0

            for stat in [
                "death_bear",
                "death_wolf"
            ]:
                try:
                    players[steamid].stats["Deaths by Animals"] += int(
                        raw_stats[stat])
                except KeyError:
                    pass

            bullet_hit_not_player = 0

            for stat in [
                "bullet_hit_building",
                "bullet_hit_sign",
                "bullet_hit_corpse",
                "bullet_hit_playercorpse",
                "bullet_hit_boar",
                "bullet_hit_bear",
                "bullet_hit_wolf",
                "bullet_hit_stag",
                "bullet_hit_entity"
            ]:
                try:
                    bullet_hit_not_player += int(raw_stats[stat])
                except KeyError:
                    pass

            try:
                players[steamid].stats["Accuracy"] = round((
                    int(raw_stats["bullet_hit_player"])
                    / (players[steamid].stats["Bullets Fired"]
                       - bullet_hit_not_player)
                ), 2)
            except KeyError:
                players[steamid].stats["Accuracy"] = 0

            death_not_by_player = 0

            for stat in [
                "deaths_suicide",
                "death_fall",
                "death_selfinflicted",
                "death_entity",
                "death_wolf",
                "death_bear"
            ]:
                try:
                    death_not_by_player += int(raw_stats[stat])
                except KeyError:
                    pass

            players[steamid].stats["K/D Ratio"] = round(
                (
                    players[steamid].stats["Players Killed"]
                    / (players[steamid].stats["Deaths"]
                       - death_not_by_player)
                ), 2)
