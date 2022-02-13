''' 
Jake Wallack
Predicting NCAA Tourney Results
'''

import pandas as pd
import csv
from kenpompy.utils import login
import string

# Returns an authenticated browser that can then be used to scrape pages that require authorization.
browser = login("jwall5678@outlook.com", "NCAAProject1")

import kenpompy.summary as kp
import kenpompy.misc

# Returns a pandas dataframe containing the efficiency and tempo stats for the current season (https://kenpom.com/summary.php).


years = [2016, 2017, 2018, 2019]

data_dict = {}

def adjust_stat_names(df):
    '''

    Parameters
    ----------
    df : dataframe
        contains the column names A%, 3PA%, ADJOE

    Returns
    -------
    none
    
    Does
    -------
    Fixes incorrectly named columns 

    '''
    df["NST%"] = df["A%"]
    df["A%"] = df["3PA%"]
    df["3PA%"] = df["AdjOE"]

def strip_seed(name):
    '''

    Parameters
    ----------
    name : a string
        a string ending in a digit or two

    Returns
    -------
    a string
        the string no longer ends in the digits

    '''
    if name[-1] in string.digits:
        return name.rstrip(string.digits)[:-1]
    else: 
        return name
    


def get_gen_missing(browser, season=None):
    '''

    Parameters
    ----------
    browser : a function
        contains kenmpom username and password and allows us to login
    season : an int 
        the season for which we want the kenpom dataframe

    Returns
    -------
    ratings_df : a dataframe
        a dataframe of the general kenpom statistics for the year
    '''
    
    url = 'https://kenpom.com/index.php'
    if season and int(season) < 2002:
        raise ValueError("season cannot be less than 2002")
    url += '?y={}'.format(season)
    browser.open(url)
    page = browser.get_current_page()
    table = page.find_all('table')[0]
    ratings_df = pd.read_html(str(table))
    # Dataframe tidying.
    ratings_df = ratings_df[0]
    ratings_df.columns = ratings_df.columns.map(lambda x: x[1])
    ratings_df.dropna(inplace = True)
    ratings_df['Team'] = ratings_df['Team'].apply(strip_seed)
    ratings_df = ratings_df[ratings_df.Team != 'Team']
    return ratings_df
    

for year in years:
    gen_stats = get_gen_missing(browser, season = year)
    eff_stats = kp.get_efficiency(browser, season = year)
    four_factors = kp.get_fourfactors(browser, season = year)
    roster_stats = kp.get_height(browser, season = year)
    misc_stats = kp.get_teamstats(browser, season = year)
    adjust_stat_names(misc_stats)
    stats = [gen_stats, eff_stats, four_factors, roster_stats, misc_stats]
    data_dict[year] = stats
    



gen = 0    
eff = 1
fac = 2
ros = 3
misc = 4



mm_data = pd.read_csv("Big_Dance_CSV.csv")
mm_data_rec = mm_data[(mm_data.Year < 2020) & (mm_data.Year > 2015)]






final_df = pd.DataFrame()
for year in data_dict.keys():
    temp_df = data_dict[year][0]
    first_df = True
    for df in data_dict[year]:
        if (first_df):
            first_df = False
        else:
            temp_df = temp_df.merge(df, left_on = 'Team', right_on = 'Team', how = 'inner')
    temp_df['Year'] = year
    final_df = final_df.append(temp_df)
    




        



# making a copy of our dataframe with different column names
final1_df = final_df.copy()
for col in final_df.columns:
    final1_df.rename(columns = {col : col + "_1"}, inplace = True)




final_df = mm_data_rec.merge(final_df, left_on = ["Team", "Year"], right_on = ["Team", "Year"], how = "inner")
final_df = final_df.merge(final1_df, left_on = ["Team.1", "Year"], right_on = ["Team_1", "Year_1"], how = "inner")

#final_df.drop(columns = ["Conference_x", "Conference_y", "Conference_x_1", "Conference_y_1", "Year_1"])


def floatify(string):
    '''

    Parameters
    ----------
    string : a str

    Returns
    -------
    a float
        string as a float
    '''
    return float(string)


def fix_WL(string):
    '''

    Parameters
    ----------
    string : a string
        has the form of wins-losses

    Returns
    -------
    win_pct : a float
        percentage of total games which are wins

    '''
    
    record = string.split("-")
    wins = int(record[0])
    losses = int(record[1])
    win_pct = wins/(wins+losses)
    return win_pct

final_df["Win_PCT"] = final_df["W-L"]
final_df["Win_PCT"] = final_df["Win_PCT"].apply(fix_WL)
final_df.drop("W-L", axis = 1, inplace = True)

final_df["Win_PCT_1"] = final_df["W-L_1"]
final_df["Win_PCT_1"] = final_df["Win_PCT_1"].apply(fix_WL)
final_df.drop("W-L_1", axis = 1, inplace = True)



final_df.drop(columns = ["Conference_x", "Conference_y", "Conference_x_1", "Conference_y_1", "Year_1"], inplace = True)

for col in final_df.columns:
    if "Rank" in col:
        final_df.drop(col, axis = 1, inplace = True)
        


def add_win_loss(df):
    for row in df.iterrows:
        if row["Score"] - row["Score.1"] > 0:
            row["Win"] = 1
            row["Win.1"] = 0
        else:
            row["Win"] = 0
            row["Win.1"] = 1
        

for row in test.iterrows:
    print(row)    
    

# 2 Delete extra conference columns
# 3 Identify repeat columns
# 4 Floatify everything
# 5 Add Win column (denoted 1 or 0) and delete point columns


    
