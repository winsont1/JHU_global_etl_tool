# John Hopkins University CSSE Covid-19 Dataset - ETL Tool to Google Sheets

This Python ETL tool was created to ingest daily-updated Covid-19 time-series data (Confirmed, Recovered, Deaths) from [JHU CSSE's Github repo](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series), and then to populate a Google Sheets worksheet.

Screenshot of JHU Raw Data: 
![JHU_raw_data](https://user-images.githubusercontent.com/16263869/99160853-f1516b80-273f-11eb-8c5b-ee7eb306e801.PNG)


The objective of this tool is to allow users (targeted at researchers) the flexibility to conduct your own custom analyses of live Covid data.

Alternatively, here's a link to a live [Google Sheet](https://docs.google.com/spreadsheets/d/1Fk3r4bwZIxQpB-4u7l8Qj4cKTauRLIQX0ISfiLYdxuY/edit?usp=sharing) implementation of this tool.
You may also choose to just use this Google Sheet data source for your analyses instead of deploying your own tool.

Screenshot of Gsheets end-result:
![Gsheets_end_result](https://user-images.githubusercontent.com/16263869/99160861-0af2b300-2740-11eb-9676-63b5c324e865.PNG)

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
There are 3 files you will need to deploy in Google Cloud Platform Functions, the main ETL code being 'main.py'.

- main.py
- new_credentials.json
- requirements.txt

Screenshot of Google Cloud Functions deployment:
![Google_Cloud](https://user-images.githubusercontent.com/16263869/99160864-15ad4800-2740-11eb-8e4f-d81f5aae27d7.PNG)


Please refer to https://cloud.google.com/functions on how to deploy your own GCP function using this code.

Please also refer to this [link](https://developers.google.com/sheets/api/quickstart/python) to set up your own Google Sheet workbook to write to. You will need to replace the name of the workbook in the 'main.py' file.

You may choose to extend the code or change the target to a database other than Google Sheets to meet your needs. Kindly adjust the write portion for the 'final_result' dataframe of the 'main.py' code accordingly.

## Language
The language you will need to deploy it in GCP Functions is Python. I used Python 3.7 for my implementation.

## Terms of Use
Please read JHU's Terms of Use for this dataset on their [page](https://github.com/CSSEGISandData/COVID-19).
The rest of the code in this repository is open-source, and is free to use.
