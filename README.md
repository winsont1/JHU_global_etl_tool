# John Hopkins University CSSE Covid-19 Dataset - ETL Tool

This Python ETL tool (Extract, Transform, Load) was created to ingest and populate a Google Sheets worksheet with Country-level Covid-19 time-series data collated by JHU CSSE's team.
The objective of this tool is to allow users (targeted at researchers) the flexibility to conduct your own custom analyses of live Covid data.
My personal tool of preference to perform descriptive analysis is Tableau Public, but you may use whatever you prefer.

You may extend the code or change the target to a database other than Google Sheets to meet your needs.

Link to the live data source (JHU CSSE time-series Github repo) : https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series.

Alternatively, here's a link to a live Google Sheet implementation of this tool https://docs.google.com/spreadsheets/d/1Fk3r4bwZIxQpB-4u7l8Qj4cKTauRLIQX0ISfiLYdxuY/edit?usp=sharing. You may choose to just use this Google Sheet data source for your analyses.

## Available Data Columns
- Country
- Date
- Total Confirmed
- Total Deaths
- Total Recovered
- Total Active*
- Deaths Change
- Confirmed Change
- Recovered Change

Note: Total Active = Total Confirmed - Total Deaths - Total Recovered

## How To Use
There are 3 main files you will need to deploy in Google Cloud Platform.

- main.py
- new_credentials.json
- requirements.txt

These files are meant to be deployed in GCP Functions. Please refer to https://cloud.google.com/functions for the documentation on how to deploy it in GCP Functions.
Please also refer to https://developers.google.com/sheets/api/quickstart/python to set up your own Google Sheet workbook to write to. You will need to replace the name of the workbook in the 'main.py' file.


## Language
The language you will need to deploy it in is Python. I used Python 3.7 for my implementation.

## Terms of Use
The code in this repository is open-source, and is free to use without restriction.
Please however, read JHU's Terms of Use for this dataset on their page https://github.com/CSSEGISandData/COVID-19.

Thank you :)
