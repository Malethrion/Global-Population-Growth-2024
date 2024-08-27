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

    headers = data[0]
    print("Headers:", headers)

    data_dict = []
    for row in data[1:]:
        entry = dict(zip(headers, row))

        try:
            # Ensure the population data is numeric before converting
            pop_2023 = entry['Population 2023'].replace(",", "")
            pop_2024 = entry['Population 2024'].replace(",", "")
            if pop_2023.isdigit() and pop_2024.isdigit():
                entry['Population 2023'] = int(pop_2023)
                entry['Population 2024'] = int(pop_2024)
            else:
                raise ValueError("Non-numeric population data")

        except ValueError as e:
            print(f"Error converting data for {entry['Country']}: {e}")
            entry['Population 2023'] = 0
            entry['Population 2024'] = 0

        data_dict.append(entry)

    return data_dict


def calculate_growth(data_dict):
    """
    Analyzes the population data and calculates growth from 2023 to 2024.
    """
    for entry in data_dict:
        if 'Population 2023' in entry and entry['Population 2023'] > 0:
            entry['Growth Rate (%)'] = (
                (entry['Population 2024'] - entry['Population 2023']) /
                entry['Population 2023']
            ) * 100
        else:
            entry['Growth Rate (%)'] = 0  # Avoid division by zero
            print(f"Warning: Division by zero avoided for {entry['Country']}")

    print("Population Data with Growth:")
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
            f"Country: {entry['Country']}\n"
            f"2023 Population: {entry['Population 2023']}\n"
            f"2024 Population: {entry['Population 2024']}\n"
            f"Growth Rate: {entry.get('Growth Rate (%)', 'N/A')}%\n"
            "-------------------------------------------"
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


def user_meny():
    """
    Placeholder text
    """
    try:
        while True:
            choice = input('Question 1')
            if choice.isnumeric():
                if number in range (1, 2):
                print(choice) 
                return choice   
            print('1 or 2')

    except Exception as e:
        print(f"An error occurred: {e}")


def main():     
    """
    Main function to run all the steps.
    """
    try:
        population_data = get_population_data()
        population_data = handle_invalid_data(population_data)
        population_data_with_growth = calculate_growth(population_data)
        choice = user_meny()
        display_population_data(population_data_with_growth)

        # Example: Update the worksheet with new data
        # (replace with actual data)
        new_data = [
            'City', 'country', 'Population 2024', 'Growth Rate (%)'
        ]
        update_population_data(new_data)

    except Exception as e:
        print(f"An error occurred: {e}")

    


print("Welcome to Global Population Data Analysis for 2024")
main()
