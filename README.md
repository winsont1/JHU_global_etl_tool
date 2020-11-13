# John Hopkins University CSSE Covid-19 Dataset - ETL Tool to Google Sheets

This Python ETL tool was created to ingest daily-updated Covid-19 time-series data from [JHU CSSE's Github repo](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series), and then to populate a Google Sheets worksheet.

The objective of this tool is to allow users (targeted at researchers) the flexibility to conduct your own custom analyses of live Covid data.

Alternatively, here's a link to a live [Google Sheet implementation](https://docs.google.com/spreadsheets/d/1Fk3r4bwZIxQpB-4u7l8Qj4cKTauRLIQX0ISfiLYdxuY/edit?usp=sharing) of this tool.
You may also choose to just use this Google Sheet data source for your analyses instead of deploying your own ETL tool.

## Available Data Columns
- Country
- State  *(needs some configuration)*
- Date
- Total Confirmed
- Total Deaths
- Total Recovered
- Total Active*
- Deaths Change
- Confirmed Change
- Recovered Change

*Note: Total Active = Total Confirmed - Total Deaths - Total Recovered*

## How To Deploy
There are 3 files you will need to deploy in Google Cloud Platform Functions, the main ETL code being 'main.py.

- main.py
- new_credentials.json
- requirements.txt

Please refer to https://cloud.google.com/functions on how to deploy your own GCP function using this code.

Please also refer to this [link](https://developers.google.com/sheets/api/quickstart/python) to set up your own Google Sheet workbook to write to. You will need to replace the name of the workbook in the 'main.py' file.

You may choose to extend the code or change the target to a database other than Google Sheets to meet your needs. Kindly adjust the write portion for the 'final_result' dataframe of the 'main.py' code accordingly.

## Language
The language you will need to deploy it in GCP Functions is Python. I used Python 3.7 for my implementation.

## Terms of Use
The code in this repository is open-source, and is free to use without restriction.

Please however, kindly read JHU's Terms of Use for this dataset on their [page](https://github.com/CSSEGISandData/COVID-19).

Thanks! :)
