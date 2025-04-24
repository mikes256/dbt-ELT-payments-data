# dbt-ELT-payments-data
Payments data ELT tool with dbt

```csharp
[API]
     ↓
[Python Script or dbt Seed]
     ↓
[Supabase (Postgres DB)]
     ↓
[dbt Models]
     ↓
[Metabase or Supabase UI for Visualization]
```

# 🔐 Payments Data ELT Project (Supabase + dbt + API)
Project Outline
1. Data Ingestion (Extract & Load)
Use Python scripts to call the API (e.g., payments data)

Load raw CSV/JSON data directly into Supabase raw schema tables
Example tables:

```raw.users```

```raw.transactions```

``raw.merchants``

``raw.cards``

2. Transformation Layer (dbt Models in Supabase)
Create a separate schema for cleaned/staged data: e.g., stg

dbt models to clean, standardize, and enrich the raw data:

``stg_users`` (normalize names, fix types)

``stg_transactions`` (filter test data, fix nulls)

``stg_merchants``, ``stg_cards``

More complex models for business logic:

``dim_users`` (customer profiles)

``dim_merchants`` (merchant categories, locations)

``fct_payments`` (fact table for payments with metadata)

``fct_failed_transactions`` (declined or suspicious payments)

``int_user_daily_balances`` (intermediate balances)

3. Testing & Documentation (dbt)
Add dbt tests (not_null, unique, accepted_values)

Add descriptions and documentation for your models

4. Visualization & Analytics
Connect Supabase or export data to a BI tool (Metabase, Superset, etc.)

Build dashboards to track KPIs like transaction volume, failed payment rate, retention

Step-by-Step Plan
Step 1: Set up Supabase project
Create project in Supabase

Create schemas: raw, stg, int, dim, fct

Create raw tables matching API data structure (users, transactions, merchants, cards)

Step 2: Write Python ETL script
Extract data from API (using requests)

Load raw data into Supabase tables (use psycopg2 or supabase-py client)

Step 3: Initialize dbt project
Connect dbt to your Supabase DB (Postgres connection details)

Scaffold models:

``models/stg/stg_users.sql``

``models/stg/stg_transactions.sql``

etc.

Step 4: Build and run dbt models
Write transformations to clean and standardize raw data

Run dbt run to create tables/views in Supabase

Add tests: dbt test

Step 5: Build intermediate & final models
Build fact and dimension tables based on cleaned data

Create business logic models (e.g., user balances, failed transactions)

Step 6: Document and test
Add model descriptions, YAML schema tests

Run dbt docs generate and view docs

Step 7: Connect BI tool (optional)
Connect Metabase or Superset to Supabase

Build dashboards for KPIs and insights

Optional Advanced Steps
Automate ETL pipeline with Apache Airflow (schedule API extraction + dbt runs)

Use Fivetran if you want a no-code connector for APIs instead of Python scripts

Add dbt snapshots to track slowly changing dimensions (e.g., user profile changes)

```csharp
🧱 Stack Breakdown:

Layer	Tool	Purpose
Source	Public API / Mock API	Simulated fintech data
Ingestion	Python script / Fivetran	Bring data into your data warehouse
Warehouse	Supabase / Snowflake	Where raw and transformed data lives
Transform	dbt	Clean, model, and create KPIs
Orchestration	Airflow	Automate & schedule pipeline steps
Version Control	Git/GitHub	Manage codebase and collaboration
BI/Analytics	Metabase / Superset	Visualize KPIs or dashboards
```


# What did I do?
Back testing is so important for continuous learning. Similar to trading I need to know the why as to what I am doing.

## 1. Loading `.csv` seed file into `dbt_project/seeds` dir
I loaded a static `.csv` file into the dbt_project/seeds folder. Seeds allows me to load in static data such as `.csv`, configs, mapping tables and dummy inputs.     
I can then run `dbt seed` to run activate the `.csv` file and then this `dbt seed` deposits the `.csv` into my duckdb warehouse for transformation. This is the *Extract* & *Load* in *'ELT'*. 

## 2. Running `dbt seed` command and creating models
I had an issue locating the `dbt_project.yml` file. ChatGPT'd for a solution but took a while, I think it looks in your pc root dir and tries to find `.dbt/dbt_project.yml`
After running the command `dbt seed`, I can then create in my `dbt_project/models/stg_transaction.sql`

## 3. Models/Staging_Transaction.SQL
This is to reference the seed file into a clean dbt like sql file. This then allows me to model the data where the main transformation takes place. So the syntax in jinja looks like:
```csharp
SELECT * FROM 
{{ ref('your_csv_name_without_csv_extension') }}
```
### 3.1 Staging Layer Seeds
This is part of the staging layer in dbt. `seeds/` in dbt is like a raw data tables folder. They are loaded into the linked warehouse once I run `dbt seed`.  

### 3.2 stg_transactions.sql

This model selects from the seed table and:
- Renames/standardises columns

- Casts data types

- Filters out test rows or bad data

- Adds basic transformations

- This is called staging, and it makes your raw data ready to be used in downstream models like fct_payments or dim_users.
     

So ultimately:
- You’re turning unstructured/semi-clean data into a clean, reliable source layer that the rest of your models can trust.

### 3.3 FiveTran Connector
If Fivetran were involved:

Fivetran handles ingestion and skips the upload stage I did with the `.csv` into the `/seeds/` folder manually.   
It pulls data directly from APIs, databases, SaaS apps, etc., and automatically creates raw tables in your warehouse (e.g., Snowflake or BigQuery).   

You’d still build stg_models in dbt. You would replace `{{ ref('.csv_filename')}}` with `{{ source('fivetran_schema_name', 'fivetran_table_name')}}`
Even though the raw tables come from Fivetran, you'd still do:
```sql
SELECT
  id,
  cast(timestamp as timestamp) as transaction_time,
  ...
FROM {{ source('fivetran_schema', 'transactions_table') }}
```
So instead of `ref()`, you’d use `source()` to access Fivetran tables.

#### 3.3.1 The learning here
Seeds (`.csv`) mimic how I'd work with actual ingested data into dbt.

Staging models are where you build a clean interface for the rest of your data pipeline.

If you replaced seeds with Fivetran, your pipeline design would be the same, just the data ingestion part would be automated.

- Use `source()` for raw external tables (usually not managed by dbt).

- Use `ref()` for anything dbt manages (`seeds`, `models`).

Always have a staging model to clean/cast/prepare messy data before your `fact/dim` models.

So for a messy `.csv` loaded as a dbt seed, it’s totally fine to `ref()` it, but your staging model should do the cleaning!


