import pandas as pd
import sys
from rich.console import Console
from rich.table import Table
from budget import load_budget_file
from request import download_sinapi_table

console = Console()

def main():
    console.rule("[bold]Starting Budgetpy")

    # load SINAPI table dataframe
    df_sinapi = load_sinapi_table()

    # Run main menu
    while True:
        display_main_menu()
        command = input("Select an option or type a command: ").lower()

        if command == '1':
            lookup_composition_table(df_sinapi)
        elif command == '2':
            calculate_total_cost(df_sinapi)
        elif command == 'help':
            console.print("Available commands: [1] Lookup, [2] Calculate, ['help'], ['exit']", style="bold yellow")
        elif command == 'exit':
            console.print("Exiting the program. Goodbye!", style="bold green")
            break
        else:
            console.print("Invalid option. Please try again.", style="bold red")


def load_sinapi_table():
    """Get pandas dataframe for the SINAPI xlsx file"""

    # Get filename from user either from sys.argv, download or input
    if len(sys.argv) > 1:
        filename = filename_add_extension(sys.argv[1])
    else:
        while True:
            request_download = input("Download sinapi file? y or n: ").strip().lower()
            if request_download in ["y", "yes"]:
                filename = download_sinapi_table()
                if not filename:
                    print("Provide your SINAPI file")
                    filename = filename_add_extension(input("Enter SINAPI file name or directory: "))
                    break
            elif request_download in ["n", "no"]:
                filename = filename_add_extension(input("Enter SINAPI file name or directory: "))
                break
            else:
                print("Invalid answer")

    # Create pandas dataframe. skip SINAPI file header rows
    try:
        df = pd.read_excel(filename, skiprows=4)
    except FileNotFoundError:
        sys.exit("Couldn't find file")

    # Remove unused columsn and empty rows
    df.dropna(subset=["DESCRICAO DA CLASSE"], inplace=True)

    df = df.drop(["VINCULO", "ORIGEM DE PREÇO", "DESCRICAO DO AGRUPADOR", "CODIGO DO AGRUPADOR"], axis=1)
    
    return df


def filename_add_extension(filename):
    """Attache XLSX file extension if none was provided"""
    
    filename = filename.strip()
    if filename.endswith(".xlsx"):
        return filename
    else:
        return filename + ".xlsx"


def display_main_menu():
    """Create and print main menu with rich"""

    table = Table(title="Main Menu")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="magenta")
    
    table.add_row("1", "Lookup Composition Tables")
    table.add_row("2", "Calculate Total Cost")
    table.add_row("help", "Show available commands")
    table.add_row("exit", "Exit the program")

    console.print(table)


def display_lookup_menu():
    """Create and print lookup menu with rich"""

    table = Table(title="Composition table lookup Menu")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="orange1")
    
    table.add_row("1", "Lookup from keywords")
    table.add_row("2", "Lookup from code")
    table.add_row("help", "Show available commands")
    table.add_row("exit", "Go to main menu")

    console.print(table)


def lookup_composition_table(df):
    """Handle lookup_menu inputs, calling functions accordingly"""

    while True:
        display_lookup_menu()
        command = input("Select an option or type a command: ").lower()

        if command == '1':
            lookup_composition_table_keyword(df)
        elif command == '2':
            lookup_composition_table_code(df)
        elif command == 'help':
            console.print("Available commands: [1] Lookup from keywords, [2] Lookup from exact code, ['help'], ['exit']", style="bold yellow")
        elif command == 'exit':
            console.print("Going back to main menu!", style="bold green")
            break
        else:
            console.print("Invalid option. Please try again.", style="bold red")


def filter(keywords, df):
    """Returns list sinapi dataframe filtered by discription keywords"""

    # Create list from description column
    descriptions = df.loc[:, "DESCRICAO DA COMPOSICAO"].to_list()

    # Filter descriptions to keep only those that match all keywords
    filtered_descriptions = [
        description for description in descriptions
        if all(keyword in description for keyword in keywords)
    ]

    return df[df["DESCRICAO DA COMPOSICAO"].isin(filtered_descriptions)]


def lookup_composition_table_keyword(df):
    """Print list of discriptions that contains list of keywords input"""

    while True:
        keywords = input("Enter description kewords: ").strip().upper().split(" ")
        
        result = filter(keywords, df)
        
        # If there are results, proceed to print
        if not result.empty:
            pd.set_option('display.max_colwidth', 110)

            console.print(result[["CODIGO  DA COMPOSICAO","DESCRICAO DA COMPOSICAO"]], style="green")

            retry = input("Search another composite table? y or n: ")
            if retry == "y" or retry == "yes":
                continue
            elif retry == "n" or retry == "no":
                return
        else:
            print(f"No composition found for keywords: {keywords}")
            retry = input("Do you want to try again? y or n: ")
            if retry == "y" or retry == "yes":
                continue
            elif retry == "n" or retry == "no":
                return


def lookup_composition_table_code(df):
    """Print composition table based on prompt"""
    
    # Filter the DataFrame based on the prompt
    while True:
        code = input("Enter the compositon table code: ")
        
        result = df[df["CODIGO  DA COMPOSICAO"] == int(code)]
        
        description = result.loc[:, "DESCRICAO DA COMPOSICAO"].to_list()[0]
        
        result = result.drop(columns="DESCRICAO DA COMPOSICAO")
        
        # If there are results, proceed to print
        if not result.empty:
            table = Table(title=f"Composition Details for Code {code}")

            # Add columns to the table
            for column in result.columns:
                table.add_column(column)

            # Add row to the table (convert the result to a list of strings)
            table.add_row(*[str(value) for value in result.iloc[0].tolist()])

            # Print the table
            console.print(table)
            console.print(f"Decription: {description}", style="green")
            retry = input("Search another composite table? y or n: ")
            if retry == "y" or retry == "yes":
                continue
            elif retry == "n" or retry == "no":
                return
        else:
            print(f"No composition found for code {code}")
            retry = input("Do you want to try again? y or n: ")
            if retry == "y" or retry == "yes":
                continue
            elif retry == "n" or retry == "no":
                return
    

def calculate_total_cost(df):
    """Calculates cost based on csv budget file"""

    # Get budget dataframe
    df_budget = load_budget_file()
    
    # Create table to display columns
    columns_display = Table(title=f"Columns for budget table")

    # Add columns
    for column in df_budget.columns:
        columns_display.add_column(column, justify="center")
    
    # Create list of columns
    budget_cols = df_budget.columns.tolist()

    # Add row of column index
    columns_display.add_row(*[str(i) for i in range(len(budget_cols))])
    
    console.print(columns_display)

    # Get correct index from user
    composition_index = get_composition_index(budget_cols)
    quantities_index = get_quantities_index(budget_cols)

    # Get column name based on column index
    composition_column_name = budget_cols[composition_index]
    quantities_column_name = budget_cols[quantities_index]

    # Preprocess columns by replacing comma with dot
    df_budget[quantities_column_name] = df_budget[quantities_column_name].apply(lambda x: float(str(x).replace(",", ".")))
    df["CUSTO TOTAL"] = df["CUSTO TOTAL"].apply(lambda x: float(str(x).replace(".", "").replace(",", ".")))

    # Apply left join to budget table and SINAPI table
    left_join = df_budget.merge(
                            df,
                            left_on=composition_column_name,
                            right_on="CODIGO  DA COMPOSICAO",
                            how="left")

    # Calculate total cost column
    left_join["_Total_Cost"] = left_join[quantities_column_name] * left_join["CUSTO TOTAL"]
    
    total_cost = left_join["_Total_Cost"].sum()
    mean_cost = left_join["_Total_Cost"].mean()

    # Print mean and sum cost results 
    console.print(f"Average cost per item: R${mean_cost:,.2f}")
    console.print(f"Project total cost: R${total_cost:,.2f}")

    # Prompt user to export results as a csv file
    export = input("Export csv file? y or n: ")
    if export == "y" or export == "yes":
        left_join.to_csv("Output.csv", index=False)
    elif export == "n" or export == "no":
        return


def get_composition_index(budget_cols):
    """Gets composition column index from input"""
    
    while True:
        try:
            composition_index = int(input("Enter composition code column index: "))
            if composition_index not in range(len(budget_cols)):
                print("Integer outside the range of column indexes")
                continue
            return composition_index
        except ValueError:
            print("Input needs to be an integer")


def get_quantities_index(budget_cols):
    """Gets quantities column index from input"""

    while True:
        try:
            quantities_index = int(input("Enter quantities column index: "))
            if quantities_index not in range(len(budget_cols)):
                print("Integer outside the range of column indexes")
                continue
            return quantities_index
        except ValueError:
            print("Input needs to be an integer")


if __name__ == "__main__":
    main()