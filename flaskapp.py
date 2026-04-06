# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

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
     rows= execute_query('''
            SELECT country.Name, city.Name
            FROM country
            JOIN city ON country.Capital = city.ID
            LIMIT 20;''')
     return render_template('country_capitals.html', users = rows)
  

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
