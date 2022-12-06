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
            "Metal Ore Harvested" varchar(15),
            "Stone Harvested" varchar(15),
            "Wood Harvested" varchar(15),
            "Scrap Acquired" varchar(15),
            "Cloth Harvested" varchar(15),
            "Lowgrade Acquired" varchar(15),
            "Leather Harvested" varchar(15),
            "Barrels Broken" varchar(15),
            "Animals Killed" varchar(15),
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
            "Time Cold" varchar(15),
            "Time Hot" varchar(15),
            "Time on Roads" varchar(15),
            "Distance on Horses" varchar(15),
            "Blueprints Learnt" varchar(15),
            "Times Waved" varchar(15),
            "Food Eaten" varchar(15),
            "Water Drunk" varchar(15),
            "Time Speaking (s)" varchar(15),
            "Notes Played" varchar(15),
            "Scientists Killed" varchar(15),
            "Deaths by AI" varchar(15),
            "Helipad Landings" varchar(15),
            "Cargo Bridge Visits" varchar(15),
            "Deaths by Animals" varchar(15),
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

        if len(player.stats) > 0:

            cur.execute(
                """
                REPLACE INTO Stats
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
        else:
            print(
                "\n\n\nSomething went wrong with player "
                + player.name
            )

    db.commit()

    print(
        "Finished updating database\n (took "
        + str((datetime.now() - start_time)) + ").\n"
    )
