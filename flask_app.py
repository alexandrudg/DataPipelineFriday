# A very simple Flask Hello World app for you to get started with...
from flask import Flask, jsonify, abort, request
import sqlite3
import git

app = Flask(__name__)

# http://alexandrudg.pythonanywhere.com/
@app.route('/')
def hello_world():
    return 'Locations App from yelp api!'

# http://alexandrudg.pythonanywhere.com/yelp/api/v1.0/category/Klosterhof
@app.route('/yelp/api/v1.0/category/<string:restaurant>', methods=['GET'])
def get_categories(restaurant):
    categories = []
    qry = "SELECT categories FROM frankfurt WHERE name = '%s';" % (restaurant)
    con = sqlite3.connect('/home/alexandrudg/DataPipelineFriday/locations.sqlite')
    c = con.cursor()
    c.execute(qry)
    rows = c.fetchall()
    for row in rows:
        categories.append(row)
    c.close()
    if len(row) == 0:
        abort(404)
    return jsonify({'categories': categories[0]})

# http://alexandrudg.pythonanywhere.com/yelp/api/v1.0/rate_ranking/berlin
@app.route('/yelp/api/v1.0/rate_ranking/<string:city>', methods=['GET'])
def get_rate_ranking(city):
    ranking = []
    qry = "select name, url, rating, city, zip_code, state from '%s%' order by rating DESC;" % (city)
    con = sqlite3.connect('/home/alexandrudg/DataPipelineFriday/locations.sqlite')
    c = con.cursor()
    c.execute(qry)
    rows = c.fetchall()
    for row in rows:
        ranking.append(row)
    c.close()
    if len(row) == 0:
        abort(404)
    return jsonify({'ranking': ranking[0]})

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/alexandrudg/DataPipelineFriday')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
