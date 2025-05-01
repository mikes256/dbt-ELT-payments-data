# dbt-ELT-payments-data

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

```
![](https://logowik.com/content/uploads/images/csv-file-format8052.jpg)

##### ![](https://www.hibob.com/wp-content/uploads/fivetran-logo-blue-rgb-2021-08-03-1.png)
##### ![](https://www.inovex.de/wp-content/uploads/Bildschirm%C2%ADfoto-2023-05-11-um-12.55.59.png)
![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxHAqB0W_61zuIGVMiU6sEeQyTaw-9xwiprw&s)
![](https://optim.tildacdn.one/tild6238-3035-4335-a333-306335373139/-/resize/824x/-/format/webp/IMG_3349.jpg.webp)
![](https://upload.wikimedia.org/wikipedia/commons/d/de/AirflowLogo.png)
![](https://miro.medium.com/v2/resize:fit:1125/1*E-TJsd6C1rwWMiiLJt5xxA.png)
```

# What did I do?
Back testing is so important for continuous learning. Similar to trading I need to know the why as to what I am doing.

![](https://media.licdn.com/dms/image/v2/D4D12AQGdzi96ie3b5A/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1662570624498?e=2147483647&v=beta&t=qkcMpqgnYhJb-JbpcLn-5HNCThubQ2yTiqrgZlvaBOs)

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
![](https://cdn.prod.website-files.com/6130fa1501794e37c21867cf/619195d4078138631a197fea_619030308ec46f1a4b39143b_2106_Fivetran_dbt_packages_BlogCard.png)
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
## 4. `dbt seed` command
Running this command (remember if I was using Fivetran it would be ``{{ source('schema', 'table') }}``) pulls data from the `dbt_project/seeds` folder and pushes it into the data warehouse. 

I can now query the seed data and add data transformation to this modelling step.

![](https://miro.medium.com/v2/resize:fit:1372/format:webp/0*MzFp1-JlToLc-2-w)
## 5. `dbt_project/target/run/` View seeds & models
This dir path will enable you to view the result of the `dbt run` by giving you a display of the raw sql used to create the file.

## 6. Query the seed file and model file
In a realdev environment I would be querying the data using Snowflake, GBigQuery or Amazon etc. But because I am doing this project locally, duckdb will suffice.

Python script used:
```python
import duckdb 
con = duckdb.connect('/workspaces/dbt-ELT-payments-data/pymnts_elt_dbt/pymnts.duckdb')
result = con.execute("SELECT * FROM stg_transaction LIMIT 3").fetchdf()
print(result)
```

### 6.1 Cleaner SQL GUI editor
Entered the commands line by line below:
```bash
curl -L https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip -o duckdb_cli.zip
unzip duckdb_cli.zip
chmod +x duckdb
sudo mv duckdb /usr/local/bin/
duckdb 'name_of_dbt_project_'.duckdb
```

## 7. Start building intermediate or fact model
Next I create higher level models which are closer to production.

- Intermediate (`int_*`) models: combining or further transforming your staging models.
- Fact (`fct_*`) models: final business-ready tables, e.g., `fct_transactions`, `fct_payments`.

These would go in models/core/ or models/facts/, depending on your folder structure.

***__note__***: if my project was large enough I would create `dim_*` (dimension) tables like:

- `dim_users`
- `dim_merchants`
- `dim_products`

| Stage          | Purpose                                                  | Example                    |
|----------------|----------------------------------------------------------|----------------------------|
| `stg_*`        | Clean column names, cast types, handle NULLs              | `stg_transaction`         |
| `int_*`        | Join multiple `stg_*` together, add intermediate calcs    | `int_transaction`         |
| `fct_*`        | Business facts, ready for dashboards, finance, analytics  | `fct_transactions`        |

## 8. Create a `models/facts/fct_transaction`
![dd](https://assets-global.website-files.com/6064b31ff49a2d31e0493af1/642d766f7dc50a6d85ecdaef_dbt_data_model%401%20(1).jpg)
Next stage was to create a fact transactions table and `{{ ref(' ') }}` it from the stg_transaction.    
In a real world example there could be `dim_*` for dimesions table.   
But ultimately, I would do further transformation in the `models/intermediate/int_*` and reference the `models/stg_*` and even further transformation in the `models/facts/fct_*` and reference the `models/intermediate/int_*`.

Reminder in a real company the structure would appear like this:

`models/stg_*` = lightly cleaned raw data

`models/intermediate/int_*` = enriched/combined data

`models/facts/fct_*` = final facts for business reporting (finance, operations, analytics)

## 9. `dbt test`
To ensure my models are in fact water-tight another step that is taken is the testing stage. Here the goal is to test data quality. This replaces the need for example in python unit tests where you can isolate your code and test individual functions or modules to ensure everything is working as it should.   
The main difference with .py unittest/pytest is you create a fake test based on a function from a module.     
dbt you test your actual models to ensure they work and flow as they should.

![alt image](https://www.wikihow.com/images/thumb/5/5d/Open-a-Tight-Jar-Step-2-Version-3.jpg/550px-nowatermark-Open-a-Tight-Jar-Step-2-Version-3.jpg)

### 9.1. Two tests generic test and customer sql test

Generic Tests (built-in, YAML-based)

Custom Tests (SQL-based for complex logic)

There are other generic tests:
```yml
accepted_values: checks if column values are within a specific list

relationships: ensures foreign key relationships exist between models
```
### 9.1.1. Generic Tests
I need to update my yaml file for generic tests. By only adding the necessary columns from my models I can test the most important inputs. 

Tests should cover:

- Should be unique and/or not null
- Foreign key for joins
- Time-based logic e.g. date_time

I had to create a `schema.yml` file which included the necessities I wanted to test. Here is the `schema.yml` file, heads up in needs to remain in the same dir as the `.sql` I am testing.
```yml
version: 2

models:
  - name: fct_transation
    description: "Fact table containing cleaned, completed transactions"
    columns:
      - name: step
        tests:
          - not_null
      - name: type
        tests:
          - not_null
          - accepted_values:
              values: [CASH_OUT, TRANSFER, DEBIT, CASH_IN, PAYMENT]
      - name: nameOrig
        tests:
          - not_null
          - unique
      - name: nameDest
        tests:
          - not_null
```
__models/name__ == stg_*/int_*/dim_*/fct_* table name without the .sql     
**models/description** == the table I am testing, any description associated    
__models/columns__ == all columns I am testing    
__models/columns/name__ == column name I am testing    
__models/columns/tests__ == the type of generic test

### 9.1.2. run `dbt test`
This will activate the test and tell you what passes, failed etc.

## 10. dimension dim models
In a star or snowflake schema, I would have a central fact table then multiple dimsension tables that join to the fact. Below is a really good example of this.
![](https://sdmntpritalynorth.oaiusercontent.com/files/00000000-dce0-6246-8ca0-5b37355f2321/raw?se=2025-05-01T17%3A21%3A36Z&sp=r&sv=2024-08-04&sr=b&scid=7800342a-4495-5311-8e6e-3c0d35ac7064&skoid=06e05d6f-bdd9-4a88-a7ec-2c0a779a08ca&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-01T07%3A29%3A36Z&ske=2025-05-02T07%3A29%3A36Z&sks=b&skv=2024-08-04&sig=L0/CTM5XT3UQksKaVzxFMECdkvmyvofj/%2Bk1TKPRwO4%3D)

Example dim tables:
- Customers (`dim_customers`)

- Products (``dim_products``)

- Employees (`dim_employees`)

- Dates (`dim_date`)

These tables:

- Contain descriptive attributes that help support the fact table (e.g. customer name, age, region)

- Tend to be slow-changing (they don't update as often as fact tables like a `fct_transaction` which will always have new transactions)

- Are used to enrich fact tables, helping end users explore and analyse data in a business-friendly way

## 11. Documentation
Documentation in dbt helps make my code more readable and accessible. Documentation can help answer questions without you having to be present. Good documentation speaks for itself.   
You can also record metadata, tests and descriptions so even if I were to look in the future I would understand what is going on.

### 11.1 Documentation `schema.yml`
In the `models/fct` folder there is the schema file. This needs to be updated with `description: ` so each column name has a description of what it is intended to do. This way anyone reading the code can immediately understand. 

This is the command to run to see the documentation:
```bash
dbt docs generate
dbt docs serve
```

## 12. Stakeholer involvement next steps
At this stage I would want to augment the data to tailor it towards my stakeholders needs. For example, below are a few cases a stakeholder could want:
- Build aggregated models (e.g., daily transaction volumes)

- Create reporting views tailored to stakeholders

- Join it with dimension tables (if you had any) for richer analytics

- Feed the output into dashboards (e.g., via BI tools)

##  12.1 `dbt run`/`dbt test`/`dbt docs generate`/`dbt docs serve`
At this stage you continue creating models from you `fct_transaction` table to refine the requirements. For example, a stakeholder could ask for the total number of transactions during a certain period.  
Or they could ask for a click view funnel analysis to be presented in a Tableau.

# End