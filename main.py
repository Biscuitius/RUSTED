import sqlite3
from examples import ***REMOVED***, ***REMOVED***

from web import login
from web import scan_recent_players
from battlemetrics import search_for_player
from datetime import datetime

example_player = ***REMOVED***.steamid
example_server = "***REMOVED***"

steam_api_key = "***REMOVED***"
app_id = "252490"
username = "***REMOVED***"
password = "***REMOVED***"


def open_database(path):

    db = sqlite3.connect(path)
    cur = db.cursor()

    try:
        cur.execute("""CREATE TABLE Players (
            "Steam ID" char(17) PRIMARY KEY, 
            "Profile URL" varchar(67), 
            "Avatar Large" varchar(120), 
            "Avatar Medium" varchar(120), 
            "Avatar Small" varchar(120), 
            "Name" varchar(32), 
            "Visibility" char(1), 
            "Online State" char(1), 
            "BMID" varchar(12)
            )""")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("""CREATE TABLE Stats (
            "Steam ID" char(17),
            "Name" varchar(32),
            "Metal Ore Harvested" varchar(15),
            "Stone Harvested" varchar(15),
            "Wood Harvested" varchar(15),
            "Scrap Acquired" varchar(15),
            "Cloth Harvested" varchar(15),
            "Lowgrade Acquired" varchar(15),
            "Leather Harvested" varchar(15),
            "Barrels Broken" varchar(15),
            "Players Killed" varchar(15),
            "Headshots Hit" varchar(15),
            "Bullets Fired" varchar(15),
            "Bullets Hit" varchar(15),
            "Deaths" varchar(15),
            "Rockets Fired" varchar(15),
            "Grenades Thrown" varchar(15),
            "Arrows Shot" varchar(15),
            "Arrows Hit" varchar(15),
            "Shotguns Fired" varchar(15),
            "Wounded" varchar(15),
            "Been Picked Up" varchar(15),
            "Picked up Other" varchar(15),
            "Suicides" varchar(15),
            "Builds Placed" varchar(15),
            "Builds Upgraded" varchar(15),
            "Time Spent Cold" varchar(15),
            "Time Spent Hot" varchar(15),
            "Time Spent on Roads" varchar(15),
            "Distance Ridden on Horses (km)" varchar(15),
            "Blueprints Learnt" varchar(15),
            "Times Waved" varchar(15),
            "Food Eaten" varchar(15),
            "Water Drunk" varchar(15),
            "Time Spent Speaking (sec)" varchar(15),
            "Instrument Notes Played" varchar(15),
            "Scientists Killed" varchar(15),
            "Deaths by AI" varchar(15),
            "Helipad Landings" varchar(15),
            "Cargo Bridge Visits" varchar(15),
            "Deaths by Animals" varchar(15),
            )""")
    except sqlite3.OperationalError:
        pass

    return db, cur


def gather_players(user, session):

    print("Gathering available players...")
    players = {}
    players.update(scan_recent_players(user, session, steam_api_key))
    print("Finished gathering players\n")
    return players


def update_bmids(players, example_server):

    print("Updating player BMIDs...")
    for player in players:
        players[player].bmid = search_for_player(
            players[player].name, example_server)
    print("Finished updating player BMIDs\n")
    return players


def update_player_stats(players, app_id, steam_api_key):

    print("Updating player stats...")
    start_time = datetime.now()
    for player in players:
        if players[player].visibility == 3:
            players[player].update_stats(app_id, steam_api_key)
    time_taken = datetime.now() - start_time
    print(f"Finished updating player stats\n (took {time_taken})")
    return players


web_auth = login(username, password)
user = web_auth[0]
session = web_auth[1]

players = gather_players(user, session)
update_player_stats(players, app_id, steam_api_key)
# update_bmids()

db_raw = open_database("Database.db")
db = db_raw[0]
cur = db_raw[1]

for player in players:

    try:
        cur.execute(
            "INSERT OR UPDATE Players VALUES (:steamid, :url, :avatar, :name, :visibility, :onlinestate, :bmid)",
            {
                "steamid": players[player].id,
                "url": players[player].url,
                "avatarbig": players[player].avatarbig,
                "avatarmedium": players[player].avatarmedium,
                "avatarsmall": players[player].avatarsmall,
                "name": players[player].name,
                "visibility": players[player].visibility,
                "onlinestate": players[player].onlinestate,
                "bmid": players[player].bmid
            })
    except sqlite3.OperationalError:
        print("Inserting initial player info failed")

    if players[player].stats:
        try:
            cur.execute(
                "INSERT OR UPDATE Stats (:steamid, :name, :metal_ore_harvested, :stone_harvested, :wood_harvested, :scrap_acquired, :cloth_harvested, :lowgrade_acquired, :leather_harvested, :barrels_broken, :animals_killed, :players_killed, :headshots_hit, :bullets_fired, :bullets_hit, :deaths, :rockets_fired, :grenades_thrown, :arrows_shot, :arrows_hit, :shotguns_fired, :wounded, :been_picked_up, :picked_up_other, :suicides, :builds_placed, :builds_upgraded, :time_spent_cold, :time_spent_hot, :time_spent_on_roads, :distance_ridden_on_horses, :blueprints_learnt, :times_waved, :food_eaten, :water_drunk, :time_spent_speaking, :instrument_notes_played, :scientists_killed, :deaths_by_ai, :helipad_landings, :cargo_bridge_visits, :deaths_by_animals)",
                {
                    "steamid": players[player].id,
                    "name": players[player].name,
                    "metal_ore_harvested": players[player].stats["Metal Ore Harvested"],
                    "stone_harvested": players[player].stats["Stone Harvested"],
                    "wood_harvested": players[player].stats["Wood Harvested"],
                    "scrap_acquired": players[player].stats["Scrap Acquired"],
                    "cloth_harvested": players[player].stats["Cloth Harvested"],
                    "lowgrade_acquired": players[player].stats["Lowgrade Acquired"],
                    "leather_harvested": players[player].stats["Leather Harvested"],
                    "barrels_broken": players[player].stats["Barrels Broken"],
                    "animals_killed": players[player].stats["Animals Killed"],
                    "players_killed": players[player].stats["Players Killed"],
                    "headshots_hit": players[player].stats["Headshots Hit"],
                    "bullets_fired": players[player].stats["Bullets Fired"],
                    "bullets_hit": players[player].stats["Bullets Hit"],
                    "deaths": players[player].stats["Deaths"],
                    "rockets_fired": players[player].stats["Rockets Fired"],
                    "grenades_thrown": players[player].stats["Grenades Thrown"],
                    "arrows_shot": players[player].stats["Arrows Shot"],
                    "arrows_hit": players[player].stats["Arrows Hit"],
                    "shotguns_fired": players[player].stats["Shotguns Fired"],
                    "wounded": players[player].stats["Wounded"],
                    "been_picked_up": players[player].stats["Been Picked Up"],
                    "picked_up_other": players[player].stats["Picked up Other"],
                    "suicides": players[player].stats["Suicides"],
                    "builds_placed": players[player].stats["Builds Placed"],
                    "builds_upgraded": players[player].stats["Builds Upgraded"],
                    "time_spent_cold": players[player].stats["Time Spent Cold"],
                    "time_spent_hot": players[player].stats["Time Spent Hot"],
                    "time_spent_on_roads": players[player].stats["Time Spent on Roads"],
                    "distance_ridden_on_horses": players[player].stats["Distance Ridden on Horses (km)"],
                    "blueprints_learnt": players[player].stats["Blueprints Learnt"],
                    "times_waved": players[player].stats["Times Waved"],
                    "food_eaten": players[player].stats["Food Eaten"],
                    "water_drunk": players[player].stats["Water Drunk"],
                    "time_spent_speaking (sec)": players[player].stats["Time Spent Speaking (sec)"],
                    "instrument_notes_played": players[player].stats["Instrument Notes Played"],
                    "scientists_killed": players[player].stats["Scientists Killed"],
                    "deaths_by_ai": players[player].stats["Deaths by AI"],
                    "helipad_landings": players[player].stats["Helipad Landings"],
                    "cargo_bridge_visits": players[player].stats["Cargo Bridge Visits"],
                    "deaths_by_animals": players[player].stats["Deaths by Animals"]
                })
        except sqlite3.OperationalError:
            print("Inserting player stats failed")

db.commit()
