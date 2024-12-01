"""
Place summary/quick description of project and file right here

@authors: Jacob Esteves
"""

import pandas as pd

swimming_data = pd.read_csv('Olympic_Swimming_Results_1912to2020.csv')


"""
* Initial Data Inspection
"""

# What are the data types of each column listed?
data_types = swimming_data.dtypes
# Integers: Year, Relay, Rank
# Strings/Objects: Location, Distance, Stroke, Gender, Team, Athlete, Results

# How many rows and columns are in the dataset?
num_columns = len(swimming_data.columns)
num_rows = len(swimming_data.index) 
# There are 10 columns and 4359 rows

# What are the names of the columns?
column_names = swimming_data.columns
# Names: Location, Year, Distance (in meters), Stroker, Relay?, Gender, Team, Athlete, Results, Rank

# Does the set contain null values? If there are null values, where are they located? 
null_values = swimming_data.isnull().sum()
# There are 14 null values in the Athlete column, and 28 null values in the Results column
null_athlete_values = swimming_data.loc[swimming_data['Athlete'].isnull()]
null_result_values = swimming_data.loc[swimming_data['Results'].isnull()]
# Displays the actual rows that contain null values -> displayed as 'nan' 

# How many unique values are in the data set
unique_values = swimming_data.nunique()
# Unique Values: 22 locations, 25 years, 8 distances, 6 strokes, 2 Relay? column, 2 unique genders, 87 teams, 2,821 athletes, 3,635 results, and 6 ranks.

# What are the first 5 rows of this Olympic swimming dataset?
head_values = swimming_data.head()
# Results from the men's 100 meter backstroke in Tokyo at the 2020 Olympics.

# How many different Countries have medals?
medal_list = [1,2,3]
unique_teams = swimming_data[swimming_data['Rank'].isin(medal_list)]
num_unique_medals = medals['Team'].nunique()
# There are 60 Countries with medals in the dataset.

# What are the number of male athletes in the dataset?
male_athletes = swimming_data[swimming_data['Gender'] == 'Men']
unique_male_athletes = male_athletes['Athlete'].nunique()
# There are 1504 male athletes in this dataset

"""
* Data Cleanup 
"""

"""
Switch the rows with Rank 0 to 5 and Rank 5 to 6. New correlations are shown below
1 -> Gold
2 -> Silver
3 -> Bronze
4 -> No Medal
5 -> DNS/DNF or Disqualified
6 -> No Data
"""
swimming_data.loc[swimming_data['Rank'] == 5, 'Rank'] = 6
swimming_data.loc[swimming_data['Rank'] == 0, 'Rank'] = 5

# Rename the Team column to 'Country' in order for clarification
swimming_data.rename(columns={"Team": "Country"}, inplace=True)

# TODO: FIX NULL VALUES HERE NEED MORE INFO

# Add a string version of 'Rank' column in order for data to be more readable
rank_medal_mapping = {
    1: 'Gold',
    2: 'Silver',
    3: 'Bronze',
    4: 'No Medal',
    5: 'DNS/DNF or Disqualified',
    6: 'No Data'
    }

swimming_data['Medal?'] = swimming_data['Rank'].map(rank_medal_mapping)
            
# Swap the Relay column with string values instead of boolean logic; Makes it more readable again
relay_mapping = {
    0: 'Individual',
    1: 'Relay'
    }

title_switch_mapping = {
    'Relay?': 'Race Format'
    }

swimming_data['Relay?'] = swimming_data['Relay?'].map(relay_mapping)
swimming_data.rename(columns=title_switch_mapping, inplace=True)

# Creates Event column to potray proper swimming terminology and allows for data anaylsis techniques

# Convert Distance column into an integer column to allow calculations
def convert_values(distance):
    """ if the distance contains x, split the string and mutiply the values to return the total distance for relays
        otherwise, eliminate the character m at the end of every indivudal event """
        
    if 'x' in distance:
        parts = distance.split('x')
        if len(parts) == 2:
            num1, num2 = parts
            return int(num1) * int(num2)
    else:
        return int(distance.replace("m", ""))
        
swimming_data['Distance (in meters)'] = swimming_data['Distance (in meters)'].apply(convert_values)
swimming_data.rename(columns={'Distance (in meters)': 'Distance (m)'}, inplace=True)

# Identify for that each row, is the swimmer a winner -> Rank = 0
def calculate_winner(rank):
    not_winner = [2, 3, 4, 5]
    if rank == 1:
        return "True"
    elif rank in not_winner:
        return "False"
    else:
        return "No Data"
    
swimming_data['Winner?'] = swimming_data['Rank'].apply(calculate_winner)


# The default data type for the results currently are objects. In order to perform data anaylsis techniques on the set, we must convert this column to floating point numbers
#TODO KINDA COMPLICATED WITH MINUTES ALSO


"""
* Slicing and Dicing the Data
"""

# What is the minimum time at the men's 200 individual medley at the 2016 Olympics (1st place winner)
filtered_data = swimming_data[
    (swimming_data["Year"] == 2016) & 
    (swimming_data["Distance (m)"] == 200) &
    (swimming_data['Gender'] == 'Men') &
    (swimming_data["Stroke"] == "Individual medley")
]

min_two_hundred_time = filtered_data["Results"].min()
# The minimum time, or the time of the first place winner is 1:54.6600

# Group all participating countries by most silver medals
silver_medals = swimming_data[swimming_data["Medal?"] == "Silver"]
silver_medal_counts = silver_medals.groupby("Country").size()
silver_medal_counts = silver_medal_counts.sort_values(ascending=False)
# USA has the most silver medals with 171, followed by Australia with 67

# Group all male swimmers by most gold medals
male_gold_medals = swimming_data[
    (swimming_data["Gender"] == "Men") & 
    (swimming_data["Medal?"] == "Gold")
]
gold_medals_by_swimmer = male_gold_medals.groupby("Athlete").size()
gold_medals_by_swimmer = gold_medals_by_swimmer.sort_values(ascending=False)
# Micheal Phelps has the most gold medals in the dataset with 13, followed by Mark Spitz with 4


"""
 Make a function that creates a new column 'Race Type' depending on how long the race is.  

 length < 100: Sprint
 200 <= length <= 500: Middle-Distance
 length > 500: Distance
"""
def classify_race_type(length):
    if length <= 100:
        return "Sprint"
    elif 200 <= length <= 500:
        return "Middle-Distance"
    elif length > 500:
        return "Distance"
    else:
        return "Unknown"

swimming_data['Race Type'] = swimming_data['Distance (m)'].apply(classify_race_type)












