# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

import boto3
from boto3.dynamodb.conditions import Key

REGION = "us-east-1"
TABLE_NAME = "FavCountries"

def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)



app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')




def view_continent(continent):
        """
    Returns all countries that are in that continent.
    """
        rows = execute_query("""
            SELECT Name, Continent, Population
            FROM country
            WHERE Continent = %s
            LIMIT 500
    """, (str(continent),))
        return rows


@app.route('/search-continent', methods=['GET', 'POST'])
def continent_form_post():
    """
    Reads the continent typed in the form, runs the query, and returns results.
    If no countries are found, flash a warning and redirect back.
    """
    #CHAT helped with if statement
    if request.method == ['POST']:
         continent = request.form['continent']
         rows = view_continent(continent)
         if not rows:
              flash("Continent not found!", "warning")
              return redirect(url_for('continent_form'))
         
         return render_template('display_countries.html', users=rows)
    return render_template('continents.html', fieldname="Continent")



@app.route('/display-countries')
def display_countries():

    rows = execute_query("""
        SELECT Name, Continent, Population
        FROM country
    """)

    return render_template('display_countries.html', users = rows)

@app.route('/country-capital')
def country_capital():
     '''
     Displays the capital of a country
     '''

     #Here both columns are named Name so I had to troubleshoot with chat and was recommended an alias
     rows= execute_query('''
            SELECT country.Name AS CountryName, city.Name AS CapitalName 
            FROM country
            JOIN city ON country.Capital = city.ID''')
     
     print('ROW:',rows)
     return render_template('country_capitals.html', users = rows)
  




# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
