import requests


class Player:

    def __init__(self, data):
        self.steamid = data["steamid"]
        self.url = "https://steamcommunity.com/profiles/" + self.steamid
        self.avatarbig = data["avatarfull"]
        self.avatarmedium = data["avatarmedium"]
        self.avatarsmall = data["avatar"]
        self.name = data["personaname"]
        self.stats = {}

    def update_info(self, steam_api_key):

        data = requests.get(
            "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="
            + steam_api_key
            + "&steamids=" + self.steamid).json()["response"]["players"]

        player_pop_list = []

        if data["communityvisibilitystate"] != 3:
            player_pop_list.append(self.steamid)

        else:
            self.avatarbig = data["avatarfull"]
            self.avatarmedium = data["avatarmedium"]
            self.avatarsmall = data["avatar"]
            self.name = data["personaname"]

        return player_pop_list
