import duckdb

# Connect to your duckdb file
con = duckdb.connect('/workspaces/dbt-ELT-payments-data/pymnts_elt_dbt/dev.duckdb')

# Run a query
df = con.execute('SELECT * FROM main.PS_20174392719_1491204439457_log LIMIT 10').fetchdf()

print(df)
