#!/usr/bin/python
import psycopg2
import pandas as pd
from psycopg2 import Error

def get_crop_info(crop_name = 'potato', variety_name = 'yukon gold'):
    crop_name = crop_name.lower()
    variety_name = variety_name.lower()
    connection = ""
    cursor = ""
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="ner",
                                      password="",
                                      host="localhost",
                                      port="5432",
                                      database="ner")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        sql_query = """
        SELECT DISTINCT A1.variety_name, category_name, trait_description as info FROM
        (SELECT variety_name, date_time FROM
        (SELECT variety_name, crop_name FROM crop_variety
        WHERE variety_name = '""" + variety_name + """' AND crop_name = '""" + crop_name +"""') A
        JOIN
        annotation_source B
        USING(variety_name)) A1
        JOIN
        (SELECT C1.* FROM trait C1 JOIN
        (SELECT category_name FROM category WHERE
        category_name = 'release date' OR category_name = 'geographic range') C2
        USING (category_name)) B1
        USING(variety_name, date_time) ORDER BY category_name;
        """
        cursor.execute(sql_query)

        # Fetch result
        column_names =["Variety Name", "Category Name", "Info" ]
        records = cursor.fetchall()
        df = pd.DataFrame(records, columns=column_names)

        return df
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_crop_varieties(crop="potato"):
    crop = crop.lower()
    connection = ""
    cursor = ""
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="ner",
                                      password="",
                                      host="localhost",
                                      port="5432",
                                      database="ner")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        sql_query = "SELECT DISTINCT variety_name FROM crop_variety WHERE crop_name = '"+crop+"';"
        cursor.execute(sql_query)

        records = cursor.fetchall()
        # Fetch result
        column_names = ["Variety Name"]
        df = pd.DataFrame(records, columns=column_names)
        return df
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_traits(crop_name = 'potato', variety_name = 'yukon gold'):
    crop_name = crop_name.lower()
    variety_name = variety_name.lower()
    connection = ""
    cursor = ""
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="ner",
                                      password="",
                                      host="localhost",
                                      port="5432",
                                      database="ner")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        sql_query = """
        SELECT DISTINCT A1.variety_name, category_name, trait_description as trait FROM
        (SELECT variety_name, date_time FROM
        (SELECT variety_name, crop_name FROM crop_variety
        WHERE variety_name = '""" + variety_name + """' AND crop_name = '""" + crop_name +"""') A
        JOIN
        annotation_source B
        USING(variety_name)) A1
        JOIN
        (SELECT C1.* FROM trait C1 JOIN
        (SELECT category_name FROM category WHERE category_name LIKE '%trait%' ) C2
        USING (category_name)) B1
        USING(variety_name, date_time) ORDER BY category_name;
        """
        cursor.execute(sql_query)
        # Fetch result
        column_names =["Variety Name", "Category Name", "Info" ]
        records = cursor.fetchall()
        df = pd.DataFrame(records, columns=column_names)
        return df

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_source(crop_name = 'potato', variety_name = 'yukon gold', trait = 'susceptible to common scab'):
    crop_name = crop_name.lower()
    variety_name = variety_name.lower()
    trait = trait.lower()
    connection = ""
    cursor = ""
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="ner",
                                      password="",
                                      host="localhost",
                                      port="5432",
                                      database="ner")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        sql_query = """
        SELECT DISTINCT source_number, trait_description
        FROM
        (SELECT source_number, date_time, variety_name
        FROM
        (SELECT * FROM crop_variety WHERE variety_name = '"""+variety_name+"""' AND crop_name = '"""+crop_name+"""') A
        JOIN
        annotation_source B
        USING(variety_name)) A1
        JOIN
        (SELECT *  FROM trait WHERE trait_description LIKE '%"""+trait+"""%') B1
        USING(variety_name, date_time);

        """
        cursor.execute(sql_query)
        # Fetch result
        column_names =["Source Number", "Trait" ]
        records = cursor.fetchall()
        df = pd.DataFrame(records, columns=column_names)
        return df

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_file_name(source_number = 1):
    connection = ""
    cursor = ""
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="ner",
                                      password="",
                                      host="localhost",
                                      port="5432",
                                      database="ner")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        sql_query = """
        SELECT DISTINCT file_name FROM annotation_source WHERE source_number = """+str(source_number)+""";
        """
        cursor.execute(sql_query)
        # Fetch result
        record = cursor.fetchall()
        return record[0][0]

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
if __name__ == "__main__":
    x = get_file_name(4)
    print(x)
