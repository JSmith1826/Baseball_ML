## Compiled Python for College Baseball game data cleaning

### TAKE SCRAPPED DATA FOR COLLEGE GAMES CLEAN AND STANDARIZE, PREPARE TO GET WEATHER RESULTS FOR NO BOX SCORE GAMES

## Pathe to raw source data

path = '../data/stats/ncaa/ESPN_2016-2022_baseball_scrape.csv'

## Load Libraries
import requests
import json
import pandas as pd
import numpy as np
import datetime

from tqdm import tqdm

## Load Data
df = pd.read_csv(path)


## Write the replacements to a dictionary
replacements = {'Ole Miss': 'University of Mississippi',
                'NC State': 'North Carolina State University',
                'Miami': 'University of Miami',
                'Florida International': 'Florida International University',
                'Hawai\'i': 'University of Hawaii, Manoa',
                'UL Monroe': 'University of Louisiana Monroe',
                'SE Louisiana': 'Southeastern Louisiana University',
                'UT Rio Grande Valley': 'The University of Texas Rio Grande Valley',
                'UMass': 'University of Massachusetts, Amherst',
                'Miami (OH)': 'Miami (Ohio)'}

## Replace the names in the df_simple

df['home_team'].replace(replacements, inplace=True)
df['away_team'].replace(replacements, inplace=True)

## Find rows with empty away_team_runs and home_team_runs and drop them
df = df.dropna(subset=['away_team_runs', 'home_team_runs'])
# drop rows that have a game_id , those are covered in other dataset
df = df[df['game_id'].isna()]
# Dop the game_id column
df.drop(columns=['game_id'], inplace=True)

# for rows with empty 'game_info' copy the 'home_team' column to a new column called 'venue'
df.loc[df['game_info'].isna(), 'venue'] = df['home_team']

## Dictionary to assign locations for games at nuetral sites

neutral_site_dict = {'SOUTHERN CONF TOURNAMENT AT GREENVILLE SC': 'Fluor Field Greenville, S.C.',
                     'BIG 12 TOURNAMENT AT OKLAHOMA CITY': 'Bricktown Ballpark',
                     'SOUTHLAND TOURNAMENT AT SUGAR LAND TX': 'Constellation Field',
                     'Big 12 Tournament (2022)': 'Globe Life Field Alrlington Texas',
                     'Big 12 Tournament (2021)': 'Bricktown Ballpark'}

## Apply the dictionary to the game_info column and copy to venue column
df['n_venue'] = df['game_info'].map(neutral_site_dict).fillna(df['venue'])


import re

# Define a function to extract the city name from game_info for NCAA games

# Define a function to extract the city name from game_info for NCAA games and other specific cases
def extract_city(game_info):
    if pd.isnull(game_info):
        return None

    # If game_info contains "World Series", assign "Omaha"
    if "World Series" in game_info:
        return "Omaha"
    
    # If game_info contains "AT", extract the city name following "AT"
    if "AT" in game_info:
        match = re.search(r'AT (.+)', game_info)
        if match:
            return match.group(1).strip()

    if "NCAA" in game_info:
        # The regex pattern below assumes the city name is at the end of the string,
        # is preceded by a dash and space, and does not contain any digits
        # Also account for "Super Regional" by making " Super" optional in the pattern
        pattern = r'– ([^-0-9]+) Super? Regional'
        match = re.search(pattern, game_info)
        if match:
            return match.group(1).strip()

    return None

# Apply the function to the game_info column and update the 'n_venue' column
df['n_venue'] = df['game_info'].apply(extract_city)


venue_df = pd.read_csv('../data/stats/ncaa/NCAA_Venues_With_Coords_and_Elevation.csv')

## Do a fuzzymatch on the 'team' column to get the team name from the venue_df and the home_team column
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

## Create a list of all of the teams in the venue_df
venue_teams = list(venue_df['team'].unique())

## Create a list of all of the teams in the df_simple
simple_teams = list(df['home_team'].unique())

## Do a match and store the results in a dataframe
matches = pd.DataFrame(columns=['team', 'venue_team', 'score'])

for team in simple_teams:
    match = process.extractOne(team, venue_teams)
    new_row = pd.DataFrame({'team': [team], 'venue_team': [match[0]], 'score': [match[1]]})
    matches = pd.concat([matches, new_row], ignore_index=True)


## If the match score is 91 or graeter, merge the Stadium, City, State, Confference, Capacity, Opened columns to the df_simple

## Create a list of the teams that matched with a score of 90 or greater
matched_teams = list(matches[matches['score'] >= 91]['team'])

## Create a dataframe with a the matched teams and their data from the venue_df
matched_venues = venue_df[venue_df['team'].isin(matched_teams)]

## how many teams matched from the simple_teams list, show list of teams that did not find good match
print(f'{len(matched_teams)} of {len(simple_teams)} teams matched')

## Show the teams that did not match
print(f'Teams that did not match: {list(set(simple_teams) - set(matched_teams))}')




