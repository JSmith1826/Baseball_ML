# Baseball_ML
A Project to use Machine Learning to evaluate baseball fields using spatial data about the playing field, weather data and game results. In an effort to understand which parameters play large rolls in the outcome of baseball games

The first phase is focused on NCAA Division 1 baseball. 


## The Basic Outline of the Readme Code Explanation:

Data Sources:
- Game Data - ESPN.com college baseball scoreboard
	- data about games and outcomes was scraped from espn.com publically available College Baseball Scoreboard. Data was scrapped at the conclution of the 20213 College World Series. 
	- All 2023 games included links to a box score summary page for the game that was used to extract the relevant information.
		- Data targeted was runs, hits, errors, and home_runs for both the home and away teams in the contest
			- Box scores also included exact game time and location
				- could expand dataset by rescraping results to store the total instances of extra base hits (double, triples)
		- HERE for code used to scrape the site
	- PRE 2023 game data
		- same method was used to crawl espn site for days with games
		- games instances were stored with the simple stats available fromt the daily scoreboard page (runs hits errors for each team)
		- soem game instances included 'game_info' and 'game_id'
			- game_id could be used to retrieve box scores that would include venue and home run information so those rows were included witht he 2023 dataset
			- game_info almost always denoted a game played at a neutral site
			- with manueal checking and data cleaning I was able to assign specific locations to the majority of the neutral site games
		- INSERT LINK TO CODE

- NCAA Venue information - Source: Wikipedia
	- url:
		- easy, just read as table using pd 
		- ran venue names into google maps places api to return specific latitude and longitude locations for each of the NCAA home team parks
			- this is used to match with geographic data
	

- Geographic Info - self generated in google maps and earth

## ETL
- taking the raw kml file and creating the dataframe full of geospacial stats
- show scraping code used
	- describe the different between games with access to box score and those without
		- boxscore games able to get exact time home runs hit by each team and all locations are easy
	- no box score games were very sparse and alot of data needed to be massaged to create a dataframe that is nearly as ferature rich as the other
- CODE OF TRANFORMATION / CLeaning of both sets of game datasets

- Weather scraping using openweathermaps api (in it's own book) include some 
	- challenges





