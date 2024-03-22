import pandas as pd

# Read the CSV file with the appropriate encoding
df = pd.read_csv('filename.csv', encoding='ISO-8859-1')

# Fix SyntaxError by removing line breaks in the values
df = df.replace({"\n": " "}, regex=True)

# Get column names and data types from DataFrame
column_names = df.columns.tolist()
dtypes = [str(df[col].dtype) for col in column_names]

# Generate CREATE TABLE query
create_query = f"CREATE TABLE new_table (\n"
for name, dtype in zip(column_names, dtypes):
    if dtype == 'int64':
        dtype = "INTEGER"  # Adjusted data type for PostgreSQL (capitalized)
    else:
        dtype = "VARCHAR(255)"
    create_query += f"    {name} {dtype},\n"
create_query = create_query.rstrip(',\n')  # Remove the last comma and newline
create_query += "\n);"

# Generate INSERT INTO query
insert_query = f"INSERT INTO new_table ({', '.join(column_names)})\nVALUES "

for row in df.itertuples(index=False):
    values = ', '.join([f"""'{str(value)[:255].replace("'",'"')}'"""if pd.notna(value) and not isinstance(value, int) else 'NULL' if pd.isna(value) else str(value) for value in row])
    insert_query += f"\n    ({values}),"

insert_query = insert_query.rstrip(',')  # Remove the last comma
insert_query += ";"

# Write CREATE TABLE query to a file
with open('create_query.sql', 'w', encoding='utf-8') as create_file:
    create_file.write(create_query)

# Write INSERT INTO query to a file
with open('insert_query.sql', 'w', encoding='UTF-8') as insert_file:
    insert_file.write(insert_query)
