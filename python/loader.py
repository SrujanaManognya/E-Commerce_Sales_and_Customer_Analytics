import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("Data/processed/analytical_order_level.csv")

username = "postgres"
password = "f0rFutur3"
host = "localhost"
port = "5432"
database = "E-Commerce Sales & Customer Analytics"

engine = create_engine(
f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

table_name = "analytical_order_level"

df.to_sql(
table_name,
engine,
if_exists="replace",
index=False
)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")
