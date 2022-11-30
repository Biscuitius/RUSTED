# R.A.T.S

Track player and server statistics on Rust by utilising APIs provided by Steam, Battlemetrics and RustMaps

## Introduction

A warm hello to you, friend. This is my first ever GitHub project - my first project ever uploaded to the internet, in fact.
I'm using this project as a means to explore the programming world and learn new concepts - so constructive criticism is much appreciated :)

The app is built in Python, using tkinter for the GUI and a mix of web scraping, steam web authentication and API get requests for retrieving all the information from the web. All information gathered is publicly accessible and cannot be used to determine a person's real-life identity without their consent.

## Feature List

So, enough about all that - what can the app actually do?
Well, the app works by trawling through your Recent Players & Current Players list, reported by Steam based on whatever servers you have recently or are currently connected to. There's quite a lot of useful information that we can gather about a player, but we can track some players better than others. 

This information we can always gather:
  • Username
  • Username Changes
  • SteamID
  • Profile URL
  • Avatar
  • Profile Visibility

This information we can only gather if the user's Steam profile is set to public:
  • Persona State (whether the user is currently online or offline)
  • Total Hours in Rust
  • Rust Stats (see below "Trackable Stats" for a full rundown)

This information we MIGHT be able to gather, but will fail if there is more than one player on the server with the same username:
  • BattleMetrics ID
  • Previous Play Sessions
  • Average Online Timeframe

## Trackable Stats

Now, looking up a player's Rust stats has always been available via API calls made by discord bots and such, but what really makes RATS special is that we can track all these stats, filter them within a timeframe (e.g. since wipe day), put them in a leaderboard and update them regularly. This opens up an infinite number of possibilities and gameplay strategies that were previously impossible or based purely on guesswork.

Here's the stats we can track:
  • Metal Ore Harvested
  • Stone Harvested
  • Wood Harvested
  • Scrap Acquired
  • Cloth Harvested
  • Lowgrade Acquired
  • Leather Harvested
  • Barrels Broken
  • Animals Killed
  • Players Killed
  • Headshots Hit
  • Bullets Fired
  • Bullets Hit
  • Deaths
  • Rockets Fired
  • Grenades Thrown
  • Arrows Shot
  • Arrows Hit
  • Shotguns Fired
  • Wounded
  • Been Picked Up
  • Picked up Other
  • Suicides
  • Builds Placed
  • Builds Upgraded
  • Time Spent Cold
  • Time Spent Hot
  • Time Spent on Roads
  • Distance on Horses
  • Blueprints Learnt
  • Times Waved
  • Food Eaten
  • Water Drunk
  • Time Spent Speaking (sec)
  • Instrument Notes Played
  • Scientists Killed
  • Deaths by AI
  • Helipad Landings
  • Cargo Bridge Visits
  • Deaths by Animals

Now, imagine this scenario: You're looking for a fun online raid target, you've got the explosives, but your team is demotivated and desperately in need of a big win. What's worse, your huge metal base hasn't got any upkeep left and nobody wants to farm for it. So, you open up RATS and check out the leaderboard. Sort by Metal Ore Harvested and filter to players with less hours than you (ez). A perfect candidate - let's call him Sal. Sal's stats sure do smell like free loot, but where does he live? You haven't seen him all wipe. So, you take a look at Sal's personal stats, and see that his Time Spent Hot is notably high, as are his Food Eaten and Water Drunk stats. His Cloth Harvested stat is unusually low this wipe, though. So, where on the map is very hot, with a lot of food and water, but no cloth? You take a look at the map, and behold - a hot desert where no cloth grows, but within, a river where food and water is plentiful. This must be where Sal lives.

Now, in that made-up and self-gratifying story, we've managed to find an ideal raid target with the precise loot we want, and even identify where he lives - just by using RATS (yes, I chose that acronym on purpose). 

Oh and by the way, the ending to that story is that Sal lived exactly right there, and he was indeed an ez online with endless metal overflowing from his boxes. Everything that once belonged to Sal is now yours, making him this wipe's biggest loser.
