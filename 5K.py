import pandas as pd

# Load data files
currency_code_file = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Retrieve-Country-Currency.csv"
exchange_rate_file = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Retrieve_Euro_EchangeRates.csv"

currency_data = pd.read_csv(currency_code_file, encoding='ISO-8859-1')  # Use ISO-8859-1 encoding
exchange_rate_data = pd.read_csv(exchange_rate_file, encoding='ISO-8859-1')  # Use ISO-8859-1 encoding


# Merge the datasets on currency code (aligning "CurrencyCode" with "CodeOut")
merged_data = pd.merge(currency_data, exchange_rate_data, left_on='CurrencyCode', right_on='CodeOut')

# Simple trade calculation
def calculate_trade(exchange_rate, trade_amount, trade_type):
    """Calculate trade result based on type (buy/sell)."""
    if trade_type == 'buy':
        return trade_amount / exchange_rate  # Amount in foreign currency
    elif trade_type == 'sell':
        return trade_amount * exchange_rate  # Amount in base currency
    else:
        raise ValueError("Invalid trade type. Use 'buy' or 'sell'.")

# Add a sample calculation for user input
trade_currency = 'USD'  # Example currency
trade_amount = 1000     # Example amount in EUR
trade_type = 'buy'      # 'buy' or 'sell'

# Find exchange rate for the selected currency
selected_rate = merged_data.loc[merged_data['CodeOut'] == trade_currency, 'Rate'].values[0]

# Calculate trade result
trade_result = calculate_trade(selected_rate, trade_amount, trade_type)

# Output the result
print(f"Trade: {trade_type} {trade_amount} EUR to {trade_currency}")
print(f"Exchange Rate: {selected_rate}")
print(f"Trade Result: {trade_result:.2f} {trade_currency}")

# Save merged data to a new file for reference
output_file = 'merged_currency_data.csv'
merged_data.to_csv(output_file, index=False)

print(f"Merged currency data with exchange rates saved to {output_file}.")
