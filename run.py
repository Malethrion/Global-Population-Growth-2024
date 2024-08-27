import gspread
from google.oauth2.service_account import Credentials

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


def calculate_growth(data_dict):
    """
    Analyzes the population data and calculates growth from 2023 to 2024.
    """
    for entry in data_dict:
        if 'Population 2023' in entry and 'Population 2024' in entry:
            entry['Growth Rate (%)'] = (
                (entry['Population 2024'] - entry['Population 2023']) /
                entry['Population 2023']
            ) * 100

    print("Population Data with Growth:")
    pprint(data_dict)
    return data_dict


def update_population_data(data):
    """
    Updates the 'statistics' worksheet with new data.
    """
    print("Updating statistics worksheet...\n")
    worksheet_to_update = SHEET.worksheet('statistics')
    worksheet_to_update.append_row(data)
    print("Statistics worksheet updated successfully\n")


def display_population_data(data_dict):
    """
    Displays the population data in a formatted text output.
    """
    print("\nPopulation by Country from 2023 to 2024:")
    for entry in data_dict:
        print(
            f"Country: {entry['Country']}, "
            f"2023 Population: {entry['Population 2023']}, "
            f"2024 Population: {entry['Population 2024']}, "
            f"Growth Rate: {entry.get('Growth Rate (%)', 'N/A')}%"
        )


def handle_invalid_data(data_dict):
    """
    Handle any potential invalid data in the list of dictionaries.
    """
    for entry in data_dict:
        if not entry['Population 2023']:
            print(
                f"Warning: Missing 2023 data for {entry['Country']}. "
                "Filling with zero."
            )
            entry['Population 2023'] = entry.get('Population 2023', 0)

        if not entry['Population 2024']:
            print(
                f"Warning: Missing 2024 data for {entry['Country']}. "
                "Filling with zero."
            )
            entry['Population 2024'] = entry.get('Population 2024', 0)

    return data_dict


def main():
    """
    Main function to run all the steps.
    """
    try:
        population_data = get_population_data()
        population_data = handle_invalid_data(population_data)
        population_data_with_growth = calculate_growth(population_data)
        display_population_data(population_data_with_growth)

        # Example: Update the worksheet with new data
        # (replace with actual data)
        new_data = [
            'Country', 'Population 2023', 'Population 2024', 'Growth Rate (%)'
        ]
        update_population_data(new_data)

    except Exception as e:
        print(f"An error occurred: {e}")


print("Welcome to Global Population Data Analysis for 2024")
main()
