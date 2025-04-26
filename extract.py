import json, pandas as pd

def read_config():
    pass 

def read_seed_csv():
    df = pd.read_csv('pymnts_elt_dbt/seeds/PS_20174392719_1491204439457_log.csv')
    print(df.sample(3))

if __name__ == '__main__':
    read_seed_csv()

