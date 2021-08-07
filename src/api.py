#!/usr/bin/python
import psycopg2
import pandas as pd
from psycopg2 import Error

def get_traits(crop="barley", variety='strider'):
    crop = crop.lower()
    variety = variety.lower()
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="gonsongo",
                                      password="",
                                      host="localhost",
                                      port="5432",
                                      database="ner")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        sql_query = "SELECT value FROM crop_data WHERE crop_name = '"+crop+"' and cvar = '"+variety+"' and label = 'TRAT';"
        cursor.execute(sql_query)

        # Fetch result
        records = cursor.fetchall()

        # Create a pandas data frame with the results
        rows = []
        for record in records:
            rows.append(record[0])
        d = {'Traits': rows}
        df = pd.DataFrame(data=d)
        return df


    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    x = get_traits("Barley", "Maja")
    print(x.head(1))
