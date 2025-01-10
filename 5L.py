import pandas as pd

# Define file paths for input and output
input_file_name_male = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\04-Clark\Retrieve-Data_male-names.csv"
input_file_name_female = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\04-Clark\Retrieve-Data_female-names.csv"
input_file_name_lastnames = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\04-Clark\Retrieve-Data_last-names.csv"
output_file_name1 = 'Assess-Staff.csv'
output_file_name2 = 'Assess-Customers.csv'

# Load the input data for names
print('Loading Male Names...')
male_names_df = pd.read_csv(input_file_name_male)
print("Male Names Columns:", male_names_df.columns)  # Print column names

print('Loading Female Names...')
female_names_df = pd.read_csv(input_file_name_female)
print("Female Names Columns:", female_names_df.columns)  # Print column names

print('Loading Last Names...')
last_names_df = pd.read_csv(input_file_name_lastnames)
print("Last Names Columns:", last_names_df.columns)  # Print column names

# Combine male and female names into one DataFrame
first_names_df = pd.concat([male_names_df, female_names_df], ignore_index=True)

# Handle case when first names outnumber last names
if len(first_names_df) <= len(last_names_df):
    staff_data = {
        'first_name': first_names_df['NameValues'],  # Use 'NameValues' column for first names
        'last_name': last_names_df['NameValues'][:len(first_names_df)],  # Use as many last names as there are first names
        'position': ['Staff'] * len(first_names_df),  # Example position
        'hourly_rate': [15.00] * len(first_names_df),  # Example hourly rate
        'hours_worked': [160] * len(first_names_df)  # Example hours worked per month
    }
else:
    print("Warning: There are more first names than last names, using the last names cyclically.")
    # Cycle last names to match the number of first names
    staff_data = {
        'first_name': first_names_df['NameValues'],  # Use 'NameValues' column for first names
        'last_name': last_names_df['NameValues'] * (len(first_names_df) // len(last_names_df)) +
                     last_names_df['NameValues'][:len(first_names_df) % len(last_names_df)],  # Cycle last names
        'position': ['Staff'] * len(first_names_df),
        'hourly_rate': [15.00] * len(first_names_df),
        'hours_worked': [160] * len(first_names_df)
    }

# Convert to DataFrame
staff_df = pd.DataFrame(staff_data)

# Calculate payroll (Salary = hourly_rate * hours_worked)
staff_df['salary'] = staff_df['hourly_rate'] * staff_df['hours_worked']

# Save the staff payroll information to a CSV
print('Saving Staff Payroll to', output_file_name1)
staff_df.to_csv(output_file_name1, index=False)

# Sample Customer Data (you can adjust this or load from a file)
customer_data = {
    'customer_id': range(1, 11),  # Example customer IDs
    'first_name': ['John', 'Alice', 'Robert', 'Sophia', 'David', 'Emma', 'Daniel', 'Olivia', 'James', 'Isabella'],
    'last_name': ['Doe', 'Smith', 'Johnson', 'Williams', 'Brown', 'Davis', 'Miller', 'Taylor', 'Anderson', 'Thomas'],
    'total_payment': [2000, 5000, 3000, 4500, 6000, 3500, 7000, 2500, 4000, 5500]  # Example total payments
}

# Convert to DataFrame
customers_df = pd.DataFrame(customer_data)

# Save the customer information to a CSV
print('Saving Customer Data to', output_file_name2)
customers_df.to_csv(output_file_name2, index=False)

# Final message indicating completion
print('### Payroll and Customer Data Generation Completed!')
