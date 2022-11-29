class Player:
    def __init__(self, steamid, profileurl, avatarbig, avatarmedium, avatarsmall, personaname, communityvisibilitystate, personastate, bmid, statnum):
        self.steamid = steamid
        self.url = profileurl
        self.avatarbig = avatarbig
        self.avatarmedium = avatarmedium
        self.avatarsmall = avatarsmall
        self.name = personaname
        self.visibility = communityvisibilitystate
        self.onlinestate = personastate
        self.bmid = bmid
        self.stats = {
            "Metal Ore Harvested": 0,
            "Stone Harvested": 0,
            "Wood Harvested": 0,
            "Scrap Acquired": 0,
            "Cloth Harvested": 0,
            "Lowgrade Acquired": 0,
            "Leather Harvested": 0,
            "Barrels Broken": 0,
            "Animals Killed": 0,
            "Players Killed": 0,
            "Headshots Hit": 0,
            "Bullets Fired": 0,
            "Bullets Hit": 0,
            "Deaths": 0,
            "Rockets Fired": 0,
            "Grenades Thrown": 0,
            "Arrows Shot": 0,
            "Arrows Hit": 0,
            "Shotguns Fired": 0,
            "Wounded": 0,
            "Been Picked Up": 0,
            "Picked up Other": 0,
            "Suicides": 0,
            "Builds Placed": 0,
            "Builds Upgraded": 0,
            "Time Spent Cold": 0,
            "Time Spent Hot": 0,
            "Time Spent on Roads": 0,
            "Distance on Horses": 0,
            "Blueprints Learnt": 0,
            "Times Waved": 0,
            "Food Eaten": 0,
            "Water Drunk": 0,
            "Time Spent Speaking (sec)": 0,
            "Instrument Notes Played": 0,
            "Scientists Killed": 0,
            "Deaths by AI": 0,
            "Helipad Landings": 0,
            "Cargo Bridge Visits": 0,
            "Deaths by Animals": 0
        }

        for stat in self.stats:
            self.stats[stat] = statnum


tyler = Player(
    steamid="***REMOVED***",
    profileurl="https://steamcommunity.com/profiles/***REMOVED***",
    avatarbig="https://avatars.akamai.steamstatic.com/91676da7339ec158aca893c508649349c23fe68f_full.jpg",
    avatarmedium="https://avatars.akamai.steamstatic.com/91676da7339ec158aca893c508649349c23fe68f_medium.jpg",
    avatarsmall="https://avatars.akamai.steamstatic.com/91676da7339ec158aca893c508649349c23fe68f.jpg",
    personaname="***REMOVED*** ***REMOVED***",
    communityvisibilitystate="3",
    personastate="0",
    bmid="905276997",
    statnum="696969")

matt = Player(
    steamid="***REMOVED***",
    profileurl="https://steamcommunity.com/profiles/***REMOVED***",
    avatarbig="https://avatars.akamai.steamstatic.com/a54691bf0c929c45939967378514191bfb3ac7f7_full.jpg",
    avatarmedium="https://avatars.akamai.steamstatic.com/a54691bf0c929c45939967378514191bfb3ac7f7_medium.jpg",
    avatarsmall="https://avatars.akamai.steamstatic.com/a54691bf0c929c45939967378514191bfb3ac7f7.jpg",
    personaname="***REMOVED***",
    communityvisibilitystate="3",
    personastate="3",
    bmid="905276997",
    statnum="696969")
