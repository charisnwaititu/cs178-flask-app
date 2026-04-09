# dbCode.py
# Author: Charis Waititu
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def get_countries_by_continent(continent):
    return execute_query("""
        SELECT Name, Continent, Population
        FROM country
        WHERE Continent = %s
        LIMIT 500
    """, (continent,))

def get_all_countries():
    return execute_query("""
        SELECT Name, Continent, Population
        FROM country
    """)

def get_country_capitals():
    return execute_query("""
        SELECT country.Name AS CountryName, city.Name AS CapitalName
        FROM country
        JOIN city ON country.Capital = city.ID
    """)