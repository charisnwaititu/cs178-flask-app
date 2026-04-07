# Going Around the world!!!

**CS178: Cloud and Database Systems — Project #1**
**Author:** Charis Waititu
**GitHub:** charisnwaititu

---

## Overview

This project is a Flask web application that allows users to interact with the world database. Users can search for countries by continent, can look at countries capitals and can even save their favorite countries. DynamoDB is used to save users favorite countries, and delete any countries that are no longer favorites. 
---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html        # Landing page
│   ├── [other].html     # Add descriptions for your other templates
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://54.242.211.158/:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `city` — stores information about cities such as their name, countrycode, district and population; primary key is `ID`; 
- `country` — stores information about countries (name, continent, population, capital, etc.); primary key is `Code`; foreign key links to `city`
- `countrylanguage` — stores languages spoken in each country (language name, whether it is official, percentage); `CountryCode` is a foreign key that links to `country`

The JOIN query used in this project: <!-- describe it in plain English -->
The JOIN query combines the country and city tables to display each country along with its capital city. It works by matching the Capital field in the country table with the ID field in the city table, allowing the program to show both the country name and its capital city name in the same result.

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `FavCountries`
- **Partition key:** `Username`
- **Attributes:** Stores `Username` and `Country`
- **Used for:** Stores users favourite country. 

---

## CRUD Operations

| Operation | Route                | Description    |
| --------- | ----------           | -------------- |
| Create    | `/add-country`       | Adds a User's favorite country to `FavCountries`|
| Read      | `/view-favs`         | Displays all users and their favorite countries by scanning the table. |
| Read      | `/display-countries` | Shows all countries with name, continent, and population.|
| Read      | `/search-continent`  | Queries countries in a specific continent. Flashes a warning if none are found.|
| Read      | `/country-capital`   | Displays each country and its capital using a join between country and city tables.|
| Update    | `/add-country`   | (Indirect) Could delete then add a different country for the user |
| Delete    | `/delete-user`   | Deletes a user and their favorite country from the table. |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
While creating the DynamoDB database, I used a sort key, as I didn't fully understand what it was for. This led to my functions getting complicated since I didn't want 1 user to have 2 favourite countries. I deleted that table and created a new one with just a partition key and no sort key. I learned what a sort key does and how to use it. It allows the partition key value to be entered more than once (so that the sort and partition key together make up a primary key)

I decided to split the buttons that explore the DynamoDB table and the one's that explore the world database on the home page for ease of access
---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
I used ChatGPT mostly to debug the functions related to the add and delete user. This was because I originally had a sort key and was trying to make it work. I finally decided to delete the original table and the sort key. I used ChatGPT to check my logic (like if the user already had a favorite country, they couldn't enter a value again)