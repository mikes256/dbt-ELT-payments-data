import duckdb , pandas as pd

# Connect to your duckdb file
con = duckdb.connect('/workspaces/dbt-ELT-payments-data/pymnts_elt_dbt/pymnts.duckdb')

result = con.execute("SELECT * FROM stg_transaction LIMIT 3").fetchdf()

print(result)
"""
# Run a query
df = con.execute('SELECT * FROM main.PS_20174392719_1491204439457_log LIMIT 1').fetchall()

print(df)
"""
# Show the tables inside
#tables = con.execute("SHOW TABLES").fetchall()
#print("Tables:", tables)

# Now query your seeded table
#result = con.execute("SELECT * FROM PS_20174392719_1491204439457_log LIMIT 3").fetchdf()
