import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches_sheet')

def get_sale_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please input sales data from the last market")
        print("Data should be six figures, seperated by commas")
        print("Example:10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
    
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid')
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts the values to integers.
    Raises a ValueError if the data cannot be converted,
    or if there is not exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
                )
    
    except ValueError as e:
        print(f'Invalid data: {e}, please try again\n')
        return False

    return True

def update_sales_worksheet(data):
    """
    Updates sales worksheet,  add new row with the list data provided.
    """
    print("Updating worksheet ... \n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully! \n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stocks and calculate surplus of each item.

    Surplus is defined as stocks minus sales;
    -   A positive surplus indicates unsold stock that must be discarded.
    -   A negative surplus indicates sandwiches made fresh due to insufficient stock
    """
    print("Calculating surplus data ...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def update_surplus_worksheet(data):
    """
    Updates surplus worksheet,  add new row with the list data provided.
    """
    print("Updating worksheet ... \n")
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully! \n")

def main():
    """
    Run all program functions
    """
    data = get_sale_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)

print("Welcome to Love Sandwiches Data Automation")
main()