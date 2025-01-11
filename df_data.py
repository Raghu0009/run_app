import psycopg2
import pandas as pd
from psycopg2 import OperationalError
from db_cont import db_params

def fetch_table_data(schema_name, table_name):
    try:
        query = f'SELECT * FROM {schema_name}."{table_name}" LIMIT 10'

        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()

                df = pd.DataFrame(data, columns=columns)

                return df, query

    except (OperationalError, psycopg2.Error) as e:
        print(f"Database error: {e}")
        return pd.DataFrame(), ""

    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame(), ""
