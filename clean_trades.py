import csv

# Read all rows from trades.csv
with open('trades.csv', 'r') as infile:
    reader = list(csv.reader(infile))

# Get header row
header = reader[0]

# Keep only rows where PnL is not empty
cleaned_rows = [header] + [row for row in reader[1:] if len(row) == len(header) and row[-1].strip() != ""]

# Overwrite the original file with cleaned data
with open('trades.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(cleaned_rows)

print("✅ Cleaned trades.csv — old rows without PnL have been removed.")
