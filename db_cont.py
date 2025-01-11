import psycopg2
from psycopg2 import OperationalError

db_params = {
    'dbname': 'IPTR',
    'user': 'postgres',
    'password': 'Steels$Paints',
    'host': '10.10.50.59',
    'port': '5432'
}

# logic to input the value schema_name, table_name_filter from main.py
def list_tables(schema_name, table_name_filter=None):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = %s
                    AND table_type = 'BASE TABLE'
                """
                query_params = [schema_name]

                if table_name_filter:
                    query += " AND table_name LIKE %s"
                    query_params.append(table_name_filter)

                query += " ORDER BY table_name;"

                cursor.execute(query, query_params)
                tables = cursor.fetchall()

                return [table[0] for table in tables]

    except (OperationalError, psycopg2.Error) as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
