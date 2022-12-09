# R.U.S.T.E.D
## Rust User Statistics Tracker & Evaluation Database
#### Track player statistics on Rust by utilising web auth, webscraping and Steam APIs

----

## Introduction
A warm hello to you, friend. This is my first ever GitHub project - my first project ever uploaded to the internet, in fact.
I'm using this project as a means to explore the programming world and learn new concepts - so constructive criticism is much appreciated :)

The app is built in Python, using tkinter for the GUI and a mix of web scraping, steam web authentication and API get requests for retrieving all the information from the web. All information gathered is publicly accessible and cannot be used to determine a person's real-life identity without their consent.


## Feature List
So, enough about all that - what can the app actually do?
Well, the app works by trawling through your Recent Players & Current Players list, reported by Steam based on whatever servers you have recently or are currently connected to. There's quite a lot of useful information that we can gather about a player - as long as they haven't opted out of sharing this information via their Steam profile.

#### Here's the basic stats we gather for user identification:
* Username
* SteamID
* Profile URL
* Avatar

### Trackable Stats
Now, looking up a player's Rust stats has always been available via API calls made by discord bots and such, but what really makes RATS special is that we can track all these stats, filter them within a timeframe, put them in a leaderboard, and update them regularly. This opens up entire gameplay strategies that were previously impossible or based on guesswork.


| Resource Stats      | Base/Roleplay Stats     | PvP Stats
|---------------------|-------------------------|--------
| Metal Ore Harvested | Builds Placed           | Players Killed
| Stone Harvested     | Builds Upgraded         | Headshots Hit
| Wood Harvested      | Time Spent Cold         | Bullets Fired
| Scrap Acquired      | Time Spent Hot          | Bullets Hit
| Cloth Harvested     | Time Spent on Roads     | Deaths
| Lowgrade Acquired   | Distance on Horses      | Accuracy
| Leather Harvested   | Blueprints Learnt       | K/D Ratio
| Barrels Broken      | Food Eaten              | Rockets Fired
| Animals Killed      | Water Drunk             | Grenades Thrown
| Scientists Killed   | Times Waved             | Shotguns Fired
| Cargo Bridge Visits | Time Spent Speaking (s) | Wounded
| Helipad Landings    | Instrument Notes Played | Been Picked Up
|                     | Deaths by AI            | Picked up Other
|                     | Deaths by Animals       | Suicides
|                     |                         | Arrows Shot
|                     |                         | Arrows Hit

### What can I do with it?

#### Well, allow me to invent a completely hypothetical and self-gratifying story in which we manage to find an ideal raid target with the precise loot we want, and even identify where he lives - just by using RATS (yes, I chose that acronym on purpose). 

Imagine this scenario: You're looking for a fun online raid target, you've got the explosives, but your team is demotivated and desperately in need of a big win. What's worse, your huge metal base hasn't got any upkeep left and nobody wants to farm for it. So, you open up RATS and check out the leaderboard. Sort by ***Metal Ore Harvested*** and filter to players with the lowest K/D ratio (ez). A perfect candidate - let's call him [Sal](https://tinyurl.com/2e95md6d). Now, farmer [Sal](https://tinyurl.com/2e95md6d)'s stats sure do smell like free loot, but where does he live? You haven't seen him all wipe. So, you take a look at [Sal](https://tinyurl.com/2e95md6d)'s personal stats, and see that his ***Time Spent Hot*** is notably high, as are his ***Food Eaten** and ***Water Drunk*** stats. His **Cloth Harvested*** stat is unusually low this wipe, though. So, where on the map is very hot, with a lot of food and water, but no cloth? You take a look at the map, and behold - a hot desert where no cloth grows, but within, a river where food and water is plentiful. This must be where [Sal](https://tinyurl.com/2e95md6d) lives.

#### The obvious ending to that story is that [Sal](https://tinyurl.com/2e95md6d) lived exactly right there, and he was indeed an ez online with endless metal overflowing from his boxes. Your wipe was saved, and your entire team awarded you with a special mug that says "Best Player" on it. That's nice. 

#### As for [Sal](https://tinyurl.com/2e95md6d), he lost everything - making him this wipe's biggest loser.
