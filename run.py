import gspread
from google.oauth2.service_account import Credentials

# --- Constants and Configurations ---
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('global_population_growth_2024')


# --- Data Retrieval Functions ---
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
            pop_2023 = entry.get('Population 2023', '').replace(",", "")
            pop_2024 = entry.get('Population 2024', '').replace(",", "")

            if pop_2023.isdigit() and pop_2024.isdigit():
                entry['Population 2023'] = int(pop_2023)
                entry['Population 2024'] = int(pop_2024)
            else:
                raise ValueError("Non-numeric population data")

        except ValueError as e:
            print(
                "Error converting data for {}: {}".format(
                    entry.get('Country', 'Unknown'), e
                )
            )
            entry['Population 2023'] = 0
            entry['Population 2024'] = 0

        data_dict.append(entry)

    return data_dict


def update_population_data(data):
    """
    Updates the 'statistics' worksheet with new data.
    """
    print("Updating statistics worksheet...\n")
    worksheet_to_update = SHEET.worksheet('statistics')
    worksheet_to_update.append_row(data)
    print("Statistics worksheet updated successfully\n")


# --- Display Functions ---
def display_population_data(data_dict):
    """
    Displays the population data in a formatted text output.
    """
    print("\nPopulation by Country from 2023 to 2024:")
    for entry in data_dict:
        print(
            f"City: {entry.get('City', 'Unknown')}\n"
            f"Country: {entry.get('Country', 'Unknown')}\n"
            f"2023 Population: {entry.get('Population 2023', 'N/A')}\n"
            f"Growth Rate: {entry.get('Growth Rate (%)', 'N/A')}%\n"
            f"2024 Population: {entry.get('Population 2024', 'N/A')}\n"
            "-------------------------------------------"
        )


# --- Error Handling Functions ---
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


def add_country_data():
    """
    Adds new country data to the statistics worksheet.
    """
    try:
        city = input("Enter city name: ")
        country = input("Enter country name: ")
        pop_2023 = input("Enter 2023 population: ")
        pop_2024 = input("Enter 2024 population: ")

        # Validate that the population inputs are numbers
        if not pop_2023.isdigit() or not pop_2024.isdigit():
            print("Population data must be numeric.")
            return

        pop_2023 = int(pop_2023)
        pop_2024 = int(pop_2024)

        # Calculate the growth rate
        growth_rate = (
            ((pop_2024 - pop_2023) / pop_2023) * 100
            if pop_2023 > 0 else 0
        )

        # Prepare the data to be added
        new_data = [
            city,
            country,
            pop_2023,
            growth_rate,
            pop_2024
        ]

        # Append to the Google Sheet
        update_population_data(new_data)
        print(f"Data for {country} added successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


def search_country_data(data_dict):
    """
    Search for a country's data by its name.
    """
    country = input("Enter the country name to search: ").strip().lower()
    results = [
        entry for entry in data_dict
        if entry['Country'].strip().lower() == country
    ]

    if results:
        display_population_data(results)
    else:
        print(f"No data found for {country.capitalize()}.")


def search_city_data(data_dict):
    """
    Search for a city's data by its name.
    """
    city = input("Enter the city name to search: ").strip().lower()
    results = [
        entry for entry in data_dict
        if entry.get('City', '').strip().lower() == city
    ]

    if results:
        display_population_data(results)
    else:
        print(f"No data found for {city.capitalize()}.")


# --- User Interaction Functions ---
def user_menu():
    """
    Display a menu for user interaction.
    """
    try:
        while True:
            print("\nPlease choose an option:")
            print("1. Display population data")
            print("2. Add new country data")
            print("3. Search for a country")
            print("4. Search for a city")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice.isnumeric() and int(choice) in range(1, 6):
                return int(choice)
            print('Invalid choice. Please enter 1, 2, 3, 4, or 5.')
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function to run all the steps.
    """
    try:
        while True:
            choice = user_menu()
            if choice == 1:
                population_data = get_population_data()
                population_data = handle_invalid_data(population_data)
                display_population_data(population_data)
            elif choice == 2:
                add_country_data()
            elif choice == 3:
                population_data = get_population_data()
                search_country_data(population_data)
            elif choice == 4:
                population_data = get_population_data()
                search_city_data(population_data)
            elif choice == 5:
                print("Exiting the program.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")


print("Welcome to Global Population Data Analysis for 2024")
main()
