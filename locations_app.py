# http://sonalinayak.pythonanywhere.com/yelp/api/v1.0/category/Kabuki
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, abort
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Locations App from yelp api!'

# http://sonalinayak.pythonanywhere.com/yelp/api/v1.0/category/Kabuki
@app.route('/yelp/api/v1.0/category/<string:restaurant>', methods=['GET'])
def get_categories(restaurant):
    categories = []
    qry = "SELECT categories FROM frankfurt WHERE name = '%s';" % (restaurant)
    con = sqlite3.connect('/home/sonalinayak/Deploy/locations.sqlite')
    c = con.cursor()
    c.execute(qry)
    rows = c.fetchall()
    for row in rows:
        categories.append(row)
    c.close()
    if len(row) == 0:
        abort(404)
    return jsonify({'categories': categories[0]})