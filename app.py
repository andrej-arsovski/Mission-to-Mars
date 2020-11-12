from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up the route for the HTML page

@app.route("/")
def index():
   mars = mongo.db.mars.find_one() #  uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. We will also assign that path to themars variable for use later.
   return render_template("index.html", mars=mars) # tells Flask to return an HTML template using an index.html file. # We'll create this file after we build the Flask routes, mars = mars tells python to use the 'mars' collection in mongodb

# set up the scrape route
@app.route("/scrape") 
def scrape():
   mars = mongo.db.mars # assign a new variable pointing to the mars databse
   mars_data = scraping.scrape_all() # varible to hold the scraped data here we are referencing the scraping.py file exported from Jupyter Notebook
   mars.update({}, mars_data, upsert=True) # update the database. {} adds an empty JSON object. next use the data thats in mars_data and upsert tells mongo to create a new document if one doesn't already exist
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()