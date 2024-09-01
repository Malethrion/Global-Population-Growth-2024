# Global Population Data Analysis for 2024

Welcome to the Global Population Data Analysis for 2024, a Python-based command-line application designed to manage, analyze, and display global population data. This application interacts with a Google Sheets document to fetch, update, and display population statistics by country and city. It also allows users to add new data entries, search for specific countries or cities, and view population growth rates from 2023 to 2024.

## User Experience (UX)

### First-Time User Goals
- As a first-time user, I want to understand the purpose of the application and its functionalities.
- As a first-time user, I want to be able to fetch and view population data easily.
- As a first-time user, I want to know how to add new data entries and perform searches.

### Returning User Goals
- As a returning user, I want to be able to quickly update the population data with new entries.
- As a returning user, I want to search for specific data to analyze population growth.

## Features

### Existing Features
- **Data Retrieval:** Fetches population data from a Google Sheets document.
- **Data Display:** Displays population statistics by country and city, including growth rates.
- **Data Management:** Allows users to add new country and city data, with automatic growth rate calculation.
- **Search Functionality:** Enables users to search for population data by country or city name.
- **User-Friendly Menu:** Provides a clear, menu-driven interface for user interactions.

### Features Left to Implement
- **Advanced Data Analytics:** Add more detailed analytics features for deeper insights into population trends.
- **Visualization:** Implement data visualization features, such as graphs or charts, to represent population growth.

## Technologies Used

### Languages and Libraries
- **Python**
- **gspread:** To interact with Google Sheets API.
- **google-auth:** For Google Sheets authentication.

## Testing

### Validator Testing
- **Python Code:** Ensured no significant issues were found by running the code through a linter.
- **Google Sheets Connection:** Verified that data retrieval and updates are functioning correctly.
- **User Interaction:** Tested each menu option to ensure correct behavior and error handling.

### Manual Testing Procedures
- **Data Retrieval:** Retrieved data from the Google Sheet to check the connection and data integrity.
- **Data Entry:** Added new country and city data, ensuring the growth rate calculation is accurate.
- **Search Functionality:** Searched for existing and non-existing countries/cities to validate the search logic.
- **Error Handling:** Inputted invalid data (e.g., non-numeric population) to check if the program handles errors correctly.

## Deployment

### Local Deployment

To deploy this project locally:

1. Clone the Repository:
   ```bash
   git clone https://github.com/Malethrion/Global-Population-Growth-2024.git

2. Install Dependencies:
   ```bash
   pip install gspread google-auth

3. Setup Google Sheets API: Obtain your creds.json file from Google Cloud Console and place it in the project directory.

4. Run the Application:
   ```bash
   python3 run.py

## Credits
### Content
- Data provided by Global Population Statistics.
### Acknowledgements
- Inspired by the Love Sandwiches project from Code Institute.
### Further Info About Commits
- Frequent commits with clear and concise commit messages help track changes and ensure the project’s evolution is well-documented.