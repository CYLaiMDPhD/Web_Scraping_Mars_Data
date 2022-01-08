# Module 10.5 Execises
# FLASK App for collected Mission-to-Mars data

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping



app = Flask(__name__)


# Connect to Mongo
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)


# Routes
@app.route('/')
def index():
	mars = mongo.db.mars.find_one()
	return render_template("index.html",mars=mars)


@app.route('/scrape')
def scrape():
	mars = mongo.db.mars	#points to the mars db in mongo
	mars_data = scraping.scrape_all()	# uses the scraping.py file to scrape new data
	mars.update_one({},{"$set":mars_data}, upsert=True)	# updates the mars db with new data
	return redirect('/', code = 302)



if __name__ == "__main__":
	app.run()


