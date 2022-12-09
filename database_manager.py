import sqlite3
from datetime import datetime


def init_database():

    print("Initialising the database...")
    db_raw = connect_database()
    db = db_raw[0]
    cur = db_raw[1]

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        Stats(
            "Steam ID" char(17) PRIMARY KEY,
            "Name" varchar(32),
            "Metal Ore Harvested" int,
            "Stone Harvested" int,
            "Wood Harvested" int,
            "Scrap Acquired" int,
            "Cloth Harvested" int,
            "Lowgrade Acquired" int,
            "Leather Harvested" int,
            "Barrels Broken" int,
            "Animals Killed" int,
            "Players Killed" int,
            "Headshots Hit" int,
            "Bullets Fired" int,
            "Bullets Hit" int,
            "Deaths" int,
            "Accuracy" float,
            "K/D Ratio" float,
            "Rockets Fired" int,
            "Grenades Thrown" int,
            "Arrows Shot" int,
            "Arrows Hit" int,
            "Shotguns Fired" int,
            "Wounded" int,
            "Been Picked Up" int,
            "Picked up Other" int,
            "Suicides" int,
            "Builds Placed" int,
            "Builds Upgraded" int,
            "Time Cold" int,
            "Time Hot" int,
            "Time on Roads" int,
            "Distance on Horses" int,
            "Blueprints Learnt" int,
            "Times Waved" int,
            "Food Eaten" int,
            "Water Drunk" int,
            "Time Speaking (s)" int,
            "Notes Played" int,
            "Scientists Killed" int,
            "Deaths by AI" int,
            "Helipad Landings" int,
            "Cargo Bridge Visits" int,
            "Deaths by Animals" int,
            "Avatar (32x32)" varchar(120),
            "Avatar (64x64)" varchar(120),
            "Avatar (184x184)" varchar(120)


        )""")

    db.commit()

    print("Database initialised.\n")


def connect_database():
    db = sqlite3.connect("Database.db")
    cur = db.cursor()
    return db, cur


def update_players(players):

    print("Updating the database...")
    start_time = datetime.now()

    db_raw = connect_database()
    db = db_raw[0]
    cur = db_raw[1]

    for player in players.values():

        cur.execute(
            """
            REPLACE INTO Stats
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                player.steamid,
                player.name,
                player.stats["Metal Ore Harvested"],
                player.stats["Stone Harvested"],
                player.stats["Wood Harvested"],
                player.stats["Scrap Acquired"],
                player.stats["Cloth Harvested"],
                player.stats["Lowgrade Acquired"],
                player.stats["Leather Harvested"],
                player.stats["Barrels Broken"],
                player.stats["Animals Killed"],
                player.stats["Players Killed"],
                player.stats["Headshots Hit"],
                player.stats["Bullets Fired"],
                player.stats["Bullets Hit"],
                player.stats["Deaths"],
                player.stats["Accuracy"],
                player.stats["K/D Ratio"],
                player.stats["Rockets Fired"],
                player.stats["Grenades Thrown"],
                player.stats["Arrows Shot"],
                player.stats["Arrows Hit"],
                player.stats["Shotguns Fired"],
                player.stats["Wounded"],
                player.stats["Been Picked Up"],
                player.stats["Picked up Other"],
                player.stats["Suicides"],
                player.stats["Builds Placed"],
                player.stats["Builds Upgraded"],
                player.stats["Time Cold"],
                player.stats["Time Hot"],
                player.stats["Time on Roads"],
                player.stats["Distance on Horses"],
                player.stats["Blueprints Learnt"],
                player.stats["Times Waved"],
                player.stats["Food Eaten"],
                player.stats["Water Drunk"],
                player.stats["Time Speaking (s)"],
                player.stats["Notes Played"],
                player.stats["Scientists Killed"],
                player.stats["Deaths by AI"],
                player.stats["Helipad Landings"],
                player.stats["Cargo Bridge Visits"],
                player.stats["Deaths by Animals"],
                player.avatarmedium,
                player.avatarsmall,
                player.avatarbig
            )
        )

    db.commit()

    print(
        "Finished updating database (took "
        + str((datetime.now() - start_time)) + ").\n"
    )
