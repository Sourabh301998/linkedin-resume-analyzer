import pandas as pd

# Load the CSV file
df = pd.read_csv("data/temp_jobs.csv")

# Print the column names
print("Columns in the CSV:")
print(df.columns)

# Show the first few rows
print("\nFirst few rows of data:")
print(df.head())


