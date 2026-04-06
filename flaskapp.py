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

@app.route("/search-continent", methods=['GET'])
def continent_form():
    """
    Renders an empty form for the user to type a continent name.
    """
    return render_template('continents.html', fieldname="Continent")


@app.route('/search-continent', methods=['GET', 'POST'])
def continent_form_post():
    """
    Reads the continent typed in the form, runs the query, and returns results.
    If no countries are found, flash a warning and redirect back.
    """
    continent = request.form['continent']
    rows = view_continent(continent)

    #ChatGPT helped me write this code. I wanted a warning to flash when the user types a continent that doesn't exist.
    if not rows:
        flash("Continent not found!", "warning")
        return redirect(url_for('continent_form'))

    return render_template('display_countries.html', users=rows)
    


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
     
     return render_template('country_capitals.html', users = rows)
  
# Flask route to add a favorite country
# Written with the help of chat
@app.route('/add-country', methods=['GET', 'POST'])
def add_country():
    if request.method == 'POST':
        # Get the user input from the form
        name = request.form['username']  
        country_name = request.form['country'] 

        # Check MySQL if the country exists
        rows = execute_query("""
            SELECT Name
            FROM country
            WHERE Name = %s
        """, (country_name,))

        if not rows:
            # Country not valid — show warning on same page
            flash(f"{country_name} is not a valid country!", "warning")
            return render_template('add_user.html')

        table = get_table()

        # Check if the user already has a favorite
        existing = table.get_item(Key={"Username": name})
        if "Item" in existing:
            # User already has a favorite — show warning
            flash(f"User '{name}' already has a favorite country: {existing['Item']['Country']}", "warning")
            return render_template('add_user.html')

        table.put_item(Item={
            "Username": name,
            "Country": country_name
        })

        # Success — redirect to home
        flash(f"{country_name} added to your favorites!", "success")
        return redirect(url_for('home'))

    # GET request: render the form
    return render_template('add_user.html')


@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Get the username from the form
        name = request.form['name']

        table = get_table()  # your DynamoDB helper

        # Check if the user exists first
        response = table.get_item(Key={"Username": name})
        if "Item" in response:
            table.delete_item(Key={"Username": name})
            flash(f"User '{name}' deleted successfully!", "warning")
        else:
            flash(f"User '{name}' does not exist!", "warning")

        return redirect(url_for('home'))

    # GET request: show the form
    return render_template('delete_user.html')


@app.route('/view-favs')
def view_fav_countries():
    table = get_table()  

    # Scan the table to get all items
    response = table.scan()
    items = response.get('Items', [])

    # Render an HTML template and pass the items
    return render_template('view_favs.html', countries=items)

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
