from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars= mongo.db.colection.find_one()
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars = scrape_mars.scrape()

    mars_dict = {"news_title": mars["news_title"], "news_paragraph": mars["news_paragraph"],
     "featured_image_url": mars["featured_image_url"], "html_table": mars["html_table"], "hemisphere_image_urls": mars["hemisphere_image_urls"]}
    
    mongo.db.colection.insert_one(mars_dict)
   

    return redirect("/", code = 302)


if __name__ == "__main__":
    app.run(debug=True)
