import numpy as np


def fetch_medal_tally(df, year, country):
    global temp_df
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


# def data_over_time(df, col):
#     nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
#     nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
#     return nations_over_time

def data_over_time(df, col):
    # Remove duplicates based on Year and the specified column
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    
    # Rename columns to standard names
    nations_over_time.columns = ['Edition', col]
    
    # Sort values by 'Edition' (which is the year)
    nations_over_time = nations_over_time.sort_values('Edition')
    
    return nations_over_time


# def most_successful(df, sport):
#     tmp_df = df.dropna(subset=['Medal'])

#     if sport != 'Overall':
#         tmp_df = tmp_df[tmp_df['Sport'] == sport]

#     x = tmp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful(df, sport):
    tmp_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        tmp_df = tmp_df[tmp_df['Sport'] == sport]
    
    # Count medals for each athlete
    medal_counts = tmp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename columns
    
    # Select top 15 athletes
    top_athletes = medal_counts.head(15)
    
    # Merge with original DataFrame to get additional details
    x = top_athletes.merge(df[['Name', 'Sport', 'region']].drop_duplicates(), on='Name', how='left')
    
    # Ensure no duplicates and rename columns for clarity
    x = x[['Name', 'Medals', 'Sport', 'region']].drop_duplicates()
    
    return x


def yearwise_medal_tally(df,country):
    # Remove NaN from medal
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    country_df = temp_df[temp_df['region'] == country]
    final_df = country_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    country_df = temp_df[temp_df['region'] == country]
    pt = country_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(
        'int')
    return pt

# def most_successful_countrywise(df, country):
#     temp_df = df.dropna(subset=['Medal'])

#     temp_df = temp_df[temp_df['region'] == country]

#     x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Calculate top 10 successful athletes
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge to get additional details
    x = x.head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    
    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['ID'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['ID'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'ID_x': 'Male', 'ID_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
