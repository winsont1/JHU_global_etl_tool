import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np


def authenticate():
     # Authenticate Google Drive credentials to access the Covid-19 data Gspreadsheet
     scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
     creds = ServiceAccountCredentials.from_json_keyfile_name('new_credentials.json', scope)
     client = gspread.authorize(creds)
     return client


def get_dataframes_list():
  # Download daily deaths, confirmed and recovered per country from JHU Github repo raw csv file url and save to Pandas dataframe
  url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
  url2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
  url3 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

  deaths_df = [pd.read_csv(url, error_bad_lines=False),'deaths']
  confirmed_df = [pd.read_csv(url2, error_bad_lines=False), 'confirmed']
  recovered_df = [pd.read_csv(url3, error_bad_lines=False), 'recovered']

  list_of_dataframes = [deaths_df, confirmed_df, recovered_df]
  return list_of_dataframes


# ## 2. Create functions to unpivot and prepare data for the 3 dataframes

# ### 2. (a) Aggregate state data for countries which have negligible data & unpivot

# In[60]:


def agg_countries_and_unpivot(dataframe):

    list_countries_with_state_info = [] # To consider for removal: Used to handle countries with state data (not used)

    df_countries_without_state_info = dataframe[~dataframe['Country/Region'].isin(list_countries_with_state_info)]

    # Aggregate (squash) data of countries with negligible state Info (A)
    df_countries_without_state_info = df_countries_without_state_info.groupby('Country/Region').sum()
    df_countries_without_state_info = df_countries_without_state_info.reset_index()
    df_countries_without_state_info.insert(1, 'Province/State',np.nan)

    # Get dataframe of Countries with State Info (B)
    df_countries_with_state_info = dataframe[dataframe['Country/Region'].isin(list_countries_with_state_info)] # To consider for removal: State data (not used)

    # Append aggregated Countries (A) with (B) dataframes
    combined_df = df_countries_with_state_info.append(df_countries_without_state_info)
    combined_df = combined_df.drop(["Lat", "Long"], axis=1)

    # Get date headers
    date_headers = list(combined_df.columns[2:].values)

    long_df = pd.melt(combined_df, id_vars= ['Country/Region','Province/State'], value_vars= date_headers)
    return long_df


# ### 2. (b) Rename columns & add change column

# In[61]:


def rename_add_change_column(dataframe, dict_key):
    header_total_dictionary = {'deaths': 'total_deaths', 'confirmed': 'total_confirmed', 'recovered': 'total_recovered' }
    header_change_dictionary = {'deaths': 'deaths_change', 'confirmed': 'confirmed_change','recovered': 'recovered_change' }

    # Rename Columns
    renamed_df = dataframe.rename(columns={"Country/Region": "country", "Province/State": "state","variable": "date", "value": header_total_dictionary[dict_key]}, errors="raise")

    # Change date column type
    renamed_df['date'] = pd.to_datetime(renamed_df['date'])

    # Include change column
    renamed_df.insert(4, header_change_dictionary[dict_key],0)
    return renamed_df


# ### 2. (c) Calculate daily change for each country (and for state, if applicable)

# In[62]:


# Calculate daily change (deaths, confirmed, recovered) for each country in 'countries' list in new columns

# Get list of unique country names
def calc_daily_change_column(dataframe, dict_key):
    list_countries_with_state_info = [] # To consider for removal: State data (not used)
    header_total_dictionary = {'deaths': 'total_deaths', 'confirmed': 'total_confirmed', 'recovered': 'total_recovered' }

    copy_of_dataframe = dataframe

    full_country_list = list(copy_of_dataframe['country'].unique())

    for country in full_country_list:

        if ( country not in list_countries_with_state_info ):

            # Set temporary df for country
            temp_df = copy_of_dataframe.loc[copy_of_dataframe['country'] == country]

            # Find difference between rows (returns difference results dataframe)
            diff = temp_df[header_total_dictionary[dict_key]].diff()

            # Apply difference calculation to original copy_of_dataframe according to index
            copy_of_dataframe.iloc[diff.index,4] = diff

        else:
            # To consider for removal: State data (not used)
            # Set temporary df for country
            temp_country_df = copy_of_dataframe.loc[copy_of_dataframe['country'] == country]

            # Get unique list of states
            states_list = list(temp_country_df['state'].unique())

            for state in states_list:
                temp_state_df = temp_country_df.loc[copy_of_dataframe['state'] == state]

                diff = temp_state_df[header_total_dictionary[dict_key]].diff()

                copy_of_dataframe.iloc[diff.index,4] = diff

    # Remove NaN values from dataframe
    copy_of_dataframe = copy_of_dataframe.fillna(0)

    return copy_of_dataframe


# In[63]:


def scheduled_job(event, context):
  # 'scheduled_job' is Google Cloud Functions entry point
  # Run calculations for all 3 dataframes with defined functions above
  list_of_dataframes = get_dataframes_list()

  for dataframe in list_of_dataframes:
      unpivoted_df = agg_countries_and_unpivot(dataframe[0])
      renamed_unpivoted_df = rename_add_change_column(unpivoted_df, dataframe[1])
      calculated_df = calc_daily_change_column(renamed_unpivoted_df, dataframe[1])
      if dataframe[1] == 'deaths':
          calculated_deaths_df = calculated_df
      elif dataframe[1] == 'confirmed':
          calculated_confirmed_df = calculated_df
      elif dataframe[1] == 'recovered':
          calculated_recovered_df = calculated_df


  # Join deaths, confirmed & recovered results
  interim_result = pd.merge(calculated_deaths_df, calculated_confirmed_df, on=['country', 'state','date'])
  final_result = pd.merge(interim_result, calculated_recovered_df, on=['country', 'state','date'])
  final_result['total_active']=final_result['total_confirmed']-final_result['total_deaths']-final_result['total_recovered']

  # Replace incorrect negative 'total_active' values with 0
  final_result.loc[(final_result.total_active<0), 'total_active'] = 0
  final_result = final_result.drop(['state'], axis=1)

  final_result['date'] = final_result['date'].astype(str)

  # Write to covid-19_datasheet_JHU_CSSE Google Sheet
  client = authenticate()
  worksheet = client.open('[REPLACE_WITH_TITLE_OF_YOUR_GOOGLE_WORKBOOK]').sheet1
  worksheet.update([final_result.columns.values.tolist()] + final_result.values.tolist())

  # To Do: Write daily deaths dataframe to CSV file - for back up in Google drive

