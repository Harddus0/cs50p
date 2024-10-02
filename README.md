# Budgetpy: Construction budgeting with SINAPI

### Video Demo:  <(https://youtu.be/dzZb62XehV8)>

### Description
Budgetpy is a Python application designed to help construction professionals easily calculate project costs using data from the SINAPI (Brazil's National System of Costs and Indexes of Construction). The application allows users to look up unit prices and compositions from the SINAPI table, download and extract the latest SINAPI data, and calculate the total cost of a project using a budget file.

## Features
### SINAPI Lookup:
- Search for values in the SINAPI table by composition code or by using a sequence of description keywords.
- Lookup exact matches or keyword-based searches within the SINAPI descriptions to get detailed information on construction items.
    
### Download Latest SINAPI Table:
- Automatically download the latest SINAPI table for any Brazilian state, with the option to specify if the table should include the "desonerado" attribute (tax relief applied or not).

### Project Cost Calculation:
- Submit a CSV file containing your project's budget, and the application will compute the total costs based on the SINAPI table.
- Generate a new CSV file with the calculated costs per row, ready for download.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Harddus0/cs50p.git
```

2. Navigate to the project directory:
`cd cs50p`

3. Create virtual enviroment:
`python3 -m venv venv`
`source venv/bin/activate`  # For Windows: venv\Scripts\activate

4. Install dependencies:
`pip install -r requirements.txt`

## Usage

### Running the Program
1. Start the Application:

- To run the program without any command-line arguments:
```bash
python project.py
```
- You will be asked if you want to download the latest SINAPI table. Answer with "yes" or "no".
    - If you choose "yes", you'll be prompted to select the Brazilian state and whether it is "desonerado" or not (tax relief status). The file will then be downloaded.
    - If the download fails or you selected "no", you will be asked to manually provide the file path of an existing SINAPI table.
2. Run the Program with a Pre-Selected File:

- If you already have the SINAPI file and prefer to specify it via command-line:
```bash
python project.py SINAPI_Custo_Ref_Composicoes_Sintetico_sc_202408_NaoDesonerado.xlsx
```
### Main Menu Options
Once the SINAPI table is loaded, you are directed to the main menu, where you can select from the following commands:

- [1] Lookup:
    - Search for items in the SINAPI table by composition code or keywords.

- [2] Calculate:
    - Calculate the total cost of your project based on your budget file.

- ['help']:
    - Displays available commands.

- ['exit']:
    - Quits the program.

### Detailed Menus
Lookup Menu ([1]):

- You will have two search options:

    - Lookup from Keywords: Enter a sequence of words to search within SINAPI descriptions. Matching composition codes and descriptions will be displayed.
    - Lookup from Exact Code: Enter a composition code to search for an exact match. If found, detailed information about the composition will be shown in a table.
- ['Help']: Displays available commands for the lookup menu.

- ['Exit']: Returns to the main menu.

Calculate Menu ([2]):

- You will be prompted to provide the file name or path for the budget CSV file.
- Afterward, you’ll be asked to enter the column indexes for the composition code and quantities. The program will then compute the total and average cost of the project.
- You will be given the option to download the results in a new CSV file by answering "yes" or "no".

### Help Commands
- Help is always available in every menu by typing 'help'.
- Exit each menu and return to the previous one or quit the program by typing 'exit'.

### Example Usage
To calculate the total cost for a project:

Run the Program:
```bash
python project.py
```
Download SINAPI Table or Load an Existing One:

You can choose to download the latest SINAPI data or provide an existing file path.
Use Lookup or Calculate:

Use the lookup feature to find specific SINAPI items, or calculate the total project cost by providing a CSV budget file.
Output:

The program outputs the total and average cost, and you can choose to export the results to a CSV file.

## project structure
```
cs50p/
    ├── request.py          # Handles downloading and extraction of SINAPI tables
    ├── budget.py           # Manages loading and processing of the budget CSV file
    ├── project.py          # Main application: coordinates the user interface and logic flow
    ├── test_project.py     # Contains test cases for core functions (using pytest)
    ├── requirements.txt    # List of required dependencies for the project
    └── README.md           # Project documentation
```

### `request.py` functions
- `download_sinapi_table()`:
    - downloads and extracts SINAPI table via request given inputs. It was noticed that "https://www.caixa.gov.br/" may block these requests, returning status 403 or 429. If it happens, the user needs to maually download the file. 
    Downloads and extracts the SINAPI table via HTTP request based on user inputs.
    - Note: The request to the URL "https://www.caixa.gov.br/" may return HTTP status codes like 403 (Forbidden) or 429 (Too Many Requests), which can block downloads. If this occurs, the user will need to manually download the SINAPI table.
- `get_state()`:
    - Prompts the user for the Brazilian state to filter the SINAPI table.
- `get_desonerado()`:
    - Asks the user if they want the "desonerado" version of the SINAPI table, which refers to the taxation-free version.
- `get_date(month_count=0)`:
    - Returns a string of the form `'%Y%m'` (year and month) for the SINAPI table. By default, it returns the current month, but month_count can adjust the date to previous months. 

### `budget.py` functions
- `detect_encoding_and_separator(csv_filename):`
    - Detects the encoding and delimiter used in the budget CSV file (important for correctly loading the data).
- `load_budget_file():`
    - Prompts the user to input the name or path of the budget CSV file and returns it as a pandas DataFrame for further processing.

### `project.py` Overview
This is the core of the application, responsible for running the interactive budget management and cost calculation processes.

- `main()`:
    - Entry point of the application, handling the loading of the SINAPI table and displaying the main menu for user interaction. 
- `load_sinapi_table()`:
    - Loads and returns the SINAPI table as a pandas DataFrame for manipulation throughout the program. 
- `filename_add_extension(filename)`:
    - Adds the `.xlsx` extension to the filename if it is missing, ensuring proper file handling. 
- `display_main_menu()`:
    - Displays the main menu using the `rich` library for a more interactive and styled terminal interface.
- `display_lookup_menu()`: 
    - Displays the lookup menu for searching compositions within the SINAPI table.
- `lookup_composition_table(df)`: 
    - Handles user input in the lookup menu, routing commands to either keyword-based search or code-based search functions.
- `filter(keywords, df)`: 
    - Filters the SINAPI table for descriptions containing user-provided keywords, returning matching rows.
- `lookup_composition_table_keyword(df)`: 
    - Prompts the user for keywords and searches the SINAPI table for matching descriptions.
- `lookup_composition_table_code(df)`: 
    - Prompts the user for an exact SINAPI composition code and displays the matching composition information.
- `calculate_total_cost(df)`:
    - Calculates the total cost of the project by joining the budget file and SINAPI table based on the composition code and quantities.
    - After calculating the total cost and average cost per item, it offers the user the option to export the results as a CSV file. 
- `get_composition_index(budget_cols)`:
    - Prompts the user to input the column index for the composition codes in the budget file.
- `get_quantities_index(budget_cols)`:
    - Prompts the user to input the column index for the quantities in the budget file. 

## `test_project.py` functions
Tests for the key functions are written using `pytest` to ensure that the logic and functionality of the program are reliable.

- `test_filename_add_extension()`:
    - Tests the `filename_add_extension()` function for different inputs, ensuring that filenames are properly handled, whether the extension is missing or already present. 
- `test_filter()`: 
    - Tests the `filter()` function to verify that it correctly accepts one or more keywords, returning the expected list of matching rows. Also checks if an empty list is returned when no matches are found. 
- `test_get_quantities_index_valid()`:
    - Verifies that `get_quantities_index()` correctly handles both valid and invalid user inputs, ensuring that only valid column indexes within the range are accepted. 
- `test_get_composition_index_valid()`:
    - Similar to the quantities index test, this ensures that `get_composition_index()` properly validates user input and restricts it to valid column indexes.

## Running Tests
To run the tests for the project, ensure you have pytest installed and then execute:
```bash
pytest test_project.py
```
For more detailed output, use:
```bash
pytest test_project.py -v
```
Make sure that all tests pass before making changes or contributions to the project to maintain the reliability and functionality of the application.

