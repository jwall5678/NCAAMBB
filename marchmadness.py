''' 
Jake Wallack
Predicting NCAA Tourney Results
'''

import pandas as pd
import csv
from kenpompy.utils import login
import kenpompy.summary as kp
import kenpompy.misc
import string

# Returns an authenticated browser that can then be used to scrape pages that require authorization.
browser = login("jwall5678@outlook.com", "NCAAProject1")

# we will be using the '15-16 through 18'-19' for our initial research
years = ["2016", "2017", "2018", "2019"]
data_dict = {}

# for loop to read in various kenpom statistics (tables) and put them together in a list for each year
for year in years:
    gen_stats = get_gen_missing(browser, season = year)
    eff_stats = kp.get_efficiency(browser, season = year)
    four_factors = kp.get_fourfactors(browser, season = year)
    roster_stats = kp.get_height(browser, season = year)
    misc_stats = kp.get_teamstats(browser, season = year)
    stats = [gen_stats, eff_stats, four_factors, roster_stats, misc_stats]
    data_dict[year] = stats
    
# indices s for stat tables
gen = 0    
eff = 1
fac = 2
ros = 3
misc = 4

# reading in march tournament data
mm_data = pd.read_csv("Big_Dance_CSV.csv")
mm_16 = mm_data.loc[mm_data["Year"] == 2016]
mm_17 = mm_data.loc[mm_data["Year"] == 2017]
mm_18 = mm_data.loc[mm_data["Year"] == 2018]
mm_19 = mm_data.loc[mm_data["Year"] == 2019]

#
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
    

temp_df['Team'].values.to_list() not in gen_stats['Team'].values.to_list()


teams = []
for team in gen_stats['Team'].values.tolist():
    if (team not in temp_df['Team'].values.tolist()):
        teams.append(team)


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

import string
gen_test.dropna(inplace = True)
def strip_seed(name):
    if name[-1] in string.digits:
        return name.rstrip(string.digits)[:-1]
    else: return name
gen_test['Team'] = gen_test['Team'].apply(strip_seed)
gen_test.drop(gen_test.loc[gen_test['Team'] == 'Team'], inplace = True)
gen_test.loc[gen_test['Team'] == 'Team']
gen_test = gen_test[gen_test.Team != 'Team']

