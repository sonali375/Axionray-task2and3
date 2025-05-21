import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the merged dataset
merged_data = pd.read_csv('merged_data.csv')

# Check the column names and the first few rows
print("Column Names:", merged_data.columns)
print(merged_data.head())

# Strip whitespace from column names if necessary
merged_data.columns = merged_data.columns.str.strip()

# Step 2: Exploratory Data Analysis (EDA)
# a. Visualization 1: Revenue Over Time
# Convert 'Invoice Date' to datetime format
merged_data['Invoice Date'] = pd.to_datetime(merged_data['Invoice Date'], errors='coerce')

# Drop rows with missing Invoice Dates
merged_data = merged_data.dropna(subset=['Invoice Date'])

# Group by month and calculate total revenue
monthly_revenue = merged_data.resample('M', on='Invoice Date')['Revenue'].sum()

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(monthly_revenue.index, monthly_revenue.values, marker='o')
plt.title('Total Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# b. Visualization 2: Cost vs. Actual Hours
# Plotting
plt.figure(figsize=(12, 6))
sns.scatterplot(data=merged_data, x='Actual Hours', y='Cost', alpha=0.6)
plt.title('Cost vs. Actual Hours')
plt.xlabel('Actual Hours')
plt.ylabel('Cost')
plt.grid()
plt.tight_layout()
plt.show()

# c. Visualization 3: Heatmap of Failure Conditions vs. Costs
# Create a pivot table for heatmap
print("Columns in dataframe:", merged_data.columns.tolist())
heatmap_data = merged_data.pivot_table(values='Cost', index='Failure Condition - Failure Component', columns='Fix Condition - Fix Component', aggfunc='mean')

# Plotting
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='coolwarm', cbar_kws={'label': 'Average Cost'})
plt.title('Heatmap of Average Cost by Failure and Fix Conditions')
plt.xlabel('Fix Condition')
plt.ylabel('Failure Condition')
plt.tight_layout()
plt.show()

# Step 3: Root Cause Identification

# 1. Failure Condition Analysis
# Count occurrences of each failure condition
failure_counts = merged_data['Failure Condition - Failure Component'].value_counts()
failure_costs = merged_data.groupby('Failure Condition - Failure Component')['Cost'].mean()

# Combine into a DataFrame for easier analysis
failure_analysis = pd.DataFrame({'Count': failure_counts, 'Average Cost': failure_costs}).reset_index()
failure_analysis.columns = ['Failure Condition - Failure Component', 'Count', 'Average Cost']

# Display the analysis
print("Failure Condition Analysis:")
print(failure_analysis.sort_values(by='Average Cost', ascending=False))

# 2. Fix Condition Analysis
# Count occurrences of each fix condition
fix_counts = merged_data['Fix Condition - Fix Component'].value_counts()
fix_costs = merged_data.groupby('Fix Condition - Fix Component')['Cost'].mean()

# Combine into a DataFrame for easier analysis
fix_analysis = pd.DataFrame({'Count': fix_counts, 'Average Cost': fix_costs}).reset_index()
fix_analysis.columns = ['Fix Condition - Fix Component', 'Count', 'Average Cost']

# Display the analysis
print("Fix Condition Analysis:")
print(fix_analysis.sort_values(by='Average Cost', ascending=False))
