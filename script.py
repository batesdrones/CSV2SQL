import pandas as pd
#Note processing can take up to 10 mins depending on the size of data table

df = pd.read_csv('data.csv')

# Remove columns from the DataFrame
columns_to_remove = ['object_classes_funding_this_award', 'program_activities_funding_this_award', 'treasury_accounts_funding_this_award']  # Specify the columns to remove
df = df.drop(columns=columns_to_remove)

# Fix SyntaxError by removing line breaks in the values
df = df.replace({"\n": " "}, regex=True)

# Get column names and data types from DataFrame
column_names = df.columns.tolist()
dtypes = [str(df[col].dtype) for col in column_names]

# Generate CREATE TABLE query
create_query = "CREATE TABLE new_table (\n"
for name, dtype in zip(column_names, dtypes):
    if dtype == 'int64':  # Check if data type is integer
        dtype = "numeric"  # Adjusted data type for PostgreSQL
    else:
        dtype = "character varying(255) COLLATE pg_catalog.\"default\""  # Adjusted data type for PostgreSQL
    create_query += f"    {name} {dtype},\n"
create_query = create_query.rstrip(',\n')  # Remove the last comma and newline
create_query += "\n);"

# Generate INSERT INTO query
insert_query = f"INSERT INTO new_table ({', '.join(column_names)})\nVALUES "
for row in df.itertuples(index=False):
    values = ', '.join([f"'{str(value)[:255]}'" if pd.notna(value) and not isinstance(value, int) else str(value) for value in row])
    insert_query += f"\n    ({values}),"
insert_query = insert_query.rstrip(',')  # Remove the last comma
insert_query += ";"

# Write CREATE TABLE query to a file
with open('create_query.sql', 'w') as create_file:
    create_file.write(create_query)

# Write INSERT INTO query to a file
with open('insert_query.sql', 'w') as insert_file:
    insert_file.write(insert_query)
