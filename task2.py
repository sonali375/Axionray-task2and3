import pandas as pd
from googletrans import Translator

# Step 1: Load the datasets
repair_data = pd.read_excel('Repair Data.xlsx')
work_order_data = pd.read_excel('Work Order Data.xlsx')

# Step 2: Identify the primary key
primary_key = 'Order No'
print(f"Identified Primary Key: {primary_key}")

# Step 3: Data Cleaning
# a. Inspect the column structure
print(repair_data.info())
print(repair_data.head())

# b. Handle missing values
missing_values = repair_data.isnull().sum()
print("Missing Values Before Cleaning:\n", missing_values)

# Fill missing values
repair_data.fillna(method='ffill', inplace=True)

# Check for duplicates
duplicates = repair_data.duplicated().sum()
print(f"Number of Duplicates Before Cleaning: {duplicates}")

# Remove duplicates
repair_data.drop_duplicates(inplace=True)

# c. Format Correction - Consistent data types
# Remove dollar signs and commas, then convert to float
repair_data['Revenue'] = repair_data['Revenue'].replace({'\$': '', ',': ''}, regex=True).astype(float)
repair_data['Cost'] = repair_data['Cost'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# If applicable, apply language translation
translator = Translator()
# Example translation for a specific column (if needed)
# repair_data['Complaint'] = repair_data['Complaint'].apply(lambda x: translator.translate(x, dest='en').text)

# Summary of data cleaning
print("Data Cleaning Summary:")
print("Missing Values After Cleaning:\n", repair_data.isnull().sum())
print(f"Number of Duplicates After Cleaning: {repair_data.duplicated().sum()}")

# Step 4: Data Integration
# a. Merge the two datasets on the identified primary key
merged_data = pd.merge(repair_data, work_order_data, on=primary_key, how='inner')

# b. Justification for join type
print("Merged Data Summary:")
print(merged_data.info())
print(merged_data.head())

# Save the merged dataset to a new CSV file if needed
merged_data.to_csv('merged_data.csv', index=False)
print("Merged data saved to 'merged_data.csv'.")
