import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# Define the scope and credentials for Google Sheets API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('global_population_growth_2024')


def get_population_data():
    """
    Retrieves the population data from the 'statistics' worksheet.
    """
    print("Fetching population data...\n")
    statistics = SHEET.worksheet('statistics')
    data = statistics.get_all_values()

    # Debugging print to check headers
    headers = data[0]
    print("Headers:", headers)

    # Convert to a list of dictionaries
    data_dict = [dict(zip(headers, row)) for row in data[1:]]

    # Convert 2023 and 2024 population fields to integers
    for entry in data_dict:
        if 'Population 2023' in entry and 'Population 2024' in entry:
            entry['Population 2023'] = int(entry['Population 2023'])
            entry['Population 2024'] = int(entry['Population 2024'])
        else:
            print(f"Missing population data in entry: {entry}")

    return data_dict
