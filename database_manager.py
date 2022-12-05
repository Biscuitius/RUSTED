import sqlite3


def init_database():

    db = sqlite3.connect("Database.db")
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS 
        Stats(
            "Steam ID" char(17) PRIMARY KEY,
            "Name" varchar(32),
            "Avatar (184x184)" varchar(120),
            "Avatar (64x64)" varchar(120),
            "Avatar (32x32)" varchar(120),
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
            "Deaths by Animals" varchar(15)
        )""")

    return db, cur


def update_player_stats(players):

    db_raw = init_database()
    db = db_raw[0]
    cur = db_raw[1]

    for player in players:

        print(player)

        cur.execute(
            "INSERT INTO Stats VALUES(:steamid, :name, :avatarbig, :avatarmedium, :avatarsmall, :metal_ore_harvested, :stone_harvested, :wood_harvested, :scrap_acquired, :cloth_harvested, :lowgrade_acquired, :leather_harvested, :barrels_broken, :animals_killed, :players_killed, :headshots_hit, :bullets_fired, :bullets_hit, :deaths, :rockets_fired, :grenades_thrown, :arrows_shot, :arrows_hit, :shotguns_fired, :wounded, :been_picked_up, :picked_up_other, :suicides, :builds_placed, :builds_upgraded, :time_cold, :time_hot, :time_on_roads, :distance_on_horses, :blueprints_learnt, :times_waved, :food_eaten, :water_drunk, :time_speaking, :notes_played, :scientists_killed, :deaths_by_ai, :helipad_landings, :cargo_bridge_visits, :deaths_by_animals)",
            {
                "steamid": players[player].steamid,
                "name": players[player].name,
                "avatarbig": players[player].avatarbig,
                "avatarmedium": players[player].avatarmedium,
                "avatarsmall": players[player].avatarsmall,
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
                "time_cold": players[player].stats["Time Cold"],
                "time_hot": players[player].stats["Time Hot"],
                "time_on_roads": players[player].stats["Time on Roads"],
                "distance_on_horses": players[player].stats["Distance on Horses"],
                "blueprints_learnt": players[player].stats["Blueprints Learnt"],
                "times_waved": players[player].stats["Times Waved"],
                "food_eaten": players[player].stats["Food Eaten"],
                "water_drunk": players[player].stats["Water Drunk"],
                "time_speaking": players[player].stats["Time Speaking (s)"],
                "notes_played": players[player].stats["Notes Played"],
                "scientists_killed": players[player].stats["Scientists Killed"],
                "deaths_by_ai": players[player].stats["Deaths by AI"],
                "helipad_landings": players[player].stats["Helipad Landings"],
                "cargo_bridge_visits": players[player].stats["Cargo Bridge Visits"],
                "deaths_by_animals": players[player].stats["Deaths by Animals"]
            })

    db.commit()
