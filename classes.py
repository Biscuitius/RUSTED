import requests


class Player:

    def __init__(self, data):
        self.id = data["steamid"]
        self.url = data["profileurl"]
        self.avatarbig = data["avatarfull"]
        self.avatarmedium = data["avatarmedium"]
        self.avatarsmall = data["avatar"]
        self.name = data["personaname"]
        self.visibility = data["communityvisibilitystate"]
        self.onlinestate = data["personastate"]
        self.bmid = None
        self.stats = {}

    def update_stats(self, steam_api_key):

        stats_response = requests.get(
            f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key={steam_api_key}&steamid={self.id}")
        raw_stats = {}

        if stats_response:

            for stat in stats_response.json()["playerstats"]["stats"]:
                raw_stats[stat["name"]] = stat["value"]

            self.stats = {}

            try:
                self.stats["Metal Ore Harvested"] = raw_stats["acquired_metal.ore"]
            except KeyError:
                self.stats["Metal Ore Harvested"] = "0"

            try:
                self.stats["Stone Harvested"] = raw_stats["harvested_stones"]
            except KeyError:
                self.stats["Stone Harvested"] = "0"

            try:
                self.stats["Wood Harvested"] = raw_stats["harvested_wood"]
            except KeyError:
                self.stats["Wood Harvested"] = "0"

            try:
                self.stats["Scrap Acquired"] = raw_stats["acquired_scrap"]
            except KeyError:
                self.stats["Scrap Acquired"] = "0"

            try:
                self.stats["Cloth Harvested"] = raw_stats["harvested_cloth"]
            except KeyError:
                self.stats["Cloth Harvested"] = "0"

            try:
                self.stats["Lowgrade Acquired"] = raw_stats["acquired_lowgradefuel"]
            except KeyError:
                self.stats["Lowgrade Acquired"] = "0"

            try:
                self.stats["Leather Harvested"] = raw_stats["harvested_leather"]
            except KeyError:
                self.stats["Leather Harvested"] = "0"

            try:
                self.stats["Barrels Broken"] = raw_stats["destroyed_barrels"]
            except KeyError:
                self.stats["Barrels Broken"] = "0"

            try:
                self.stats["Animals Killed"] = str(
                    + int(raw_stats["kill_bear"])
                    + int(raw_stats["kill_boar"])
                    + int(raw_stats["kill_stag"])
                    + int(raw_stats["kill_chicken"])
                    + int(raw_stats["kill_wolf"]))
            except KeyError:
                self.stats["Animals Killed"] = "0"

            try:
                self.stats["Players Killed"] = raw_stats["kill_player"]
            except KeyError:
                self.stats["Players Killed"] = "0"

            try:
                self.stats["Headshots Hit"] = raw_stats["headshot"]
            except KeyError:
                self.stats["Headshots Hit"] = "0"

            try:
                self.stats["Bullets Fired"] = raw_stats["bullet_fired"]
            except KeyError:
                self.stats["Bullets Fired"] = "0"

            try:
                self.stats["Bullets Hit"] = str(
                    + int(raw_stats["bullet_hit_player"])
                    + int(raw_stats["bullet_hit_boar"])
                    + int(raw_stats["bullet_hit_bear"])
                    + int(raw_stats["bullet_hit_wolf"])
                    + int(raw_stats["bullet_hit_stag"])
                    + int(raw_stats["bullet_hit_entity"]))
            except KeyError:
                self.stats["Bullets Hit"] = "0"

            try:
                self.stats["Deaths"] = raw_stats["deaths"]
            except KeyError:
                self.stats["Deaths"] = "0"

            try:
                self.stats["Rockets Fired"] = raw_stats["rocket_fired"]
            except KeyError:
                self.stats["Rockets Fired"] = "0"

            try:
                self.stats["Grenades Thrown"] = raw_stats["grenades_thrown"]
            except KeyError:
                self.stats["Grenades Thrown"] = "0"

            try:
                self.stats["Arrows Shot"] = raw_stats["arrows_shot"]
            except KeyError:
                self.stats["Arrows Shot"] = "0"

            try:
                self.stats["Arrows Hit"] = str(
                    + int(raw_stats["arrow_hit_player"])
                    + int(raw_stats["arrow_hit_boar"])
                    + int(raw_stats["arrow_hit_bear"])
                    + int(raw_stats["arrow_hit_wolf"])
                    + int(raw_stats["arrow_hit_stag"])
                    + int(raw_stats["arrow_hit_chicken"])
                    + int(raw_stats["arrow_hit_entity"]))
            except KeyError:
                self.stats["Arrows Hit"] = "0"

            try:
                self.stats["Shotguns Fired"] = raw_stats["shotgun_fired"]
            except KeyError:
                self.stats["Shotguns Fired"] = "0"

            try:
                self.stats["Wounded"] = raw_stats["wounded"]
            except KeyError:
                self.stats["Wounded"] = "0"

            try:
                self.stats["Been Picked Up"] = raw_stats["wounded_assisted"]
            except KeyError:
                self.stats["Been Picked Up"] = "0"

            try:
                self.stats["Picked up Other"] = raw_stats["wounded_healed"]
            except KeyError:
                self.stats["Picked up Other"] = "0"

            try:
                self.stats["Suicides"] = raw_stats["death_suicide"]
            except KeyError:
                self.stats["Suicides"] = "0"

            try:
                self.stats["Builds Placed"] = raw_stats["placed_blocks"]
            except KeyError:
                self.stats["Builds Placed"] = "0"

            try:
                self.stats["Builds Upgraded"] = raw_stats["upgraded_blocks"]
            except KeyError:
                self.stats["Builds Upgraded"] = "0"

            try:
                self.stats["Time Spent Cold"] = raw_stats["cold_exposure_duration"]
            except KeyError:
                self.stats["Time Spent Cold"] = "0"

            try:
                self.stats["Time Spent Hot"] = raw_stats["hot_exposure_duration"]
            except KeyError:
                self.stats["Time Spent Hot"] = "0"

            try:
                self.stats["Time Spent on Roads"] = raw_stats["topology_road_duration"]
            except KeyError:
                self.stats["Time Spent on Roads"] = "0"

            try:
                self.stats["Distance on Horses"] = raw_stats["horse_distance_ridden_km"]
            except KeyError:
                self.stats["Distance on Horses"] = "0"

            try:
                self.stats["Blueprints Learnt"] = raw_stats["blueprint_studied"]
            except KeyError:
                self.stats["Blueprints Learnt"] = "0"

            try:
                self.stats["Times Waved"] = raw_stats["gesture_wave_count"]
            except KeyError:
                self.stats["Times Waved"] = "0"

            try:
                self.stats["Food Eaten"] = raw_stats["calories_consumed"]
            except KeyError:
                self.stats["Food Eaten"] = "0"

            try:
                self.stats["Water Drunk"] = raw_stats["water_consumed"]
            except KeyError:
                self.stats["Water Drunk"] = "0"

            try:
                self.stats["Time Speaking (s)"] = raw_stats["seconds_speaking"]
            except KeyError:
                self.stats["Time Speaking (s)"] = "0"

            try:
                self.stats["Notes Played"] = str(
                    + int(raw_stats["InstrumentNotesPlayed"])
                    + int(raw_stats["InstrumentNotesPlayedBinds"]))
            except KeyError:
                self.stats["Notes Played"] = "0"

            try:
                self.stats["Scientists Killed"] = raw_stats["kill_scientist"]
            except KeyError:
                self.stats["Scientists Killed"] = "0"

            try:
                self.stats["Deaths by AI"] = raw_stats["death_entity"]
            except KeyError:
                self.stats["Deaths by AI"] = "0"

            try:
                self.stats["Helipad Landings"] = raw_stats["helipad_landings"]
            except KeyError:
                self.stats["Helipad Landings"] = "0"

            try:
                self.stats["Cargo Bridge Visits"] = raw_stats["cargoship_bridge_visits"]
            except KeyError:
                self.stats["Cargo Bridge Visits"] = "0"

            try:
                self.stats["Deaths by Animals"] = str(
                    + int(raw_stats["death_wolf"])
                    + int(raw_stats["death_bear"]))
            except KeyError:
                self.stats["Deaths by Animals"] = "0"
