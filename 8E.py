import os
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Define base path and directories
Base =  r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'
print('Working Base :', Base)
Company = '01-Vermeulen'
InputFileName = 'Online-Retail-Billboard.xlsx'
EDSAssessDir = '02-Assess/01-EDS'
InputAssessDir = os.path.join(EDSAssessDir, '02-Python')

# Ensure the assessment directory exists
sFileAssessDir = os.path.join(Base, Company, InputAssessDir)
if not os.path.exists(sFileAssessDir):
    os.makedirs(sFileAssessDir)

# Input file path
sFileName = os.path.join(Base, Company, '00-RawData', InputFileName)

# Load data
df = pd.read_excel(sFileName)
print(f"Initial dataset shape: {df.shape}")

# Preprocess data
df['Description'] = df['Description'].str.strip()
df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')
df = df[~df['InvoiceNo'].str.contains('C')]  # Remove canceled invoices

# Basket for France
basket = (df[df['Country'] == "France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

# Define encoding function
def encode_units(x):
    return x > 0

# Encode data for France basket
basket_sets = basket.apply(lambda col: col.map(encode_units))

# Ensure Boolean type
basket_sets = basket_sets.astype(bool)

# Drop 'POSTAGE' column if it exists
if 'POSTAGE' in basket_sets.columns:
    basket_sets.drop('POSTAGE', inplace=True, axis=1)

# Generate frequent itemsets and rules for France
frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1,num_itemsets=10)

# Select relevant columns including antecedent and conviction
rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift', 'conviction']]

print("Association Rules for France (including antecedent and conviction): ")
print(rules.head())

# Filter rules based on lift and confidence
filtered_rules = rules[(rules['lift'] >= 6) & (rules['confidence'] >= 0.8)]
print(f"Filtered Rules (Lift >= 6, Confidence >= 0.8):\n{filtered_rules}")

# Analyze specific products
sProduct1 = 'ALARM CLOCK BAKELIKE GREEN'
print(sProduct1)
if sProduct1 in basket.columns:
    print(basket[sProduct1].sum())
else:
    print(f"Product '{sProduct1}' not found in the data.")

sProduct2 = 'ALARM CLOCK BAKELIKE RED'
print(sProduct2)
if sProduct2 in basket.columns:
    print(basket[sProduct2].sum())
else:
    print(f"Product '{sProduct2}' not found in the data.")

# Basket for Germany
basket2 = (df[df['Country'] == "Germany"]
           .groupby(['InvoiceNo', 'Description'])['Quantity']
           .sum().unstack().reset_index().fillna(0)
           .set_index('InvoiceNo'))

# Encode data for Germany basket
basket_sets2 = basket2.apply(lambda col: col.map(encode_units))

# Ensure Boolean type
basket_sets2 = basket_sets2.astype(bool)

# Drop 'POSTAGE' column if it exists
if 'POSTAGE' in basket_sets2.columns:
    basket_sets2.drop('POSTAGE', inplace=True, axis=1)

# Generate frequent itemsets and rules for Germany
frequent_itemsets2 = apriori(basket_sets2, min_support=0.05, use_colnames=True)
rules2 = association_rules(frequent_itemsets2, metric="lift", min_threshold=1,num_itemsets=10)

# Select relevant columns including antecedent and conviction
rules2 = rules2[['antecedents', 'consequents', 'support', 'confidence', 'lift', 'conviction']]

print("Association Rules for Germany (including antecedent and conviction): ")
filtered_rules2 = rules2[(rules2['lift'] >= 4) & (rules2['confidence'] >= 0.5)]
print(filtered_rules2)

print("Execution Completed - Association Rule Mining")
