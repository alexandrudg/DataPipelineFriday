import json
import requests
import yaml
import sqlite3

# import general settings
config = yaml.safe_load(open("config.yaml"))
environment = yaml.safe_load(open("environment.yaml"))
locations = config['restaurant_locations']

for location in locations:
  maximum = 50
  offset = 0
  while offset <= maximum:
    # Request restaurants and encoding
    url = environment['API-ROOT'] + "location=" + location["query"] + "&categories=" + location["categories"] + "&limit=50" + "&offset=" + str(offset)
    headers = {'Authorization': 'Bearer ' + environment['API-KEY'] }
    r = requests.get(url=url, headers=headers)
    text = r.text
    parsed = json.loads(text)
    restaurants = parsed['businesses']
    maximum = min(parsed['total'], 950)
    offset += 50

    formatted_restaurants = []
    for restaurant in restaurants:
      #Preparing the JSON entries for sqlite
      formatted_restaurant = {
        'id': restaurant['id'],
        'name': restaurant['name'],
        'url': restaurant['url'],
        'review_count': restaurant['review_count'],
        'categories': ', '.join(d['title'] for d in restaurant['categories']),
        'rating': restaurant['rating'],
        'price': restaurant['price'] if 'price' in restaurant else '',
        'street': restaurant['location']['address1'],
        'city': restaurant['location']['city'],
        'zip_code': restaurant['location']['zip_code'],
        'state': restaurant['location']['state']
      }
      formatted_restaurants.append(formatted_restaurant)

    # Connect to sqlite & prepare table if it's not there
    qry = config['TABLE-CREATE'].format(table=location['table'])
    con = sqlite3.connect('locations.sqlite')
    c = con.cursor()
    c.execute(qry)

    # Create secondary index if it does not exist
    createSecondaryIndex = "CREATE INDEX IF NOT EXISTS " + location["secondary_index"] + " ON " + location[
      "table"] + "(" + location["secondary_index"] + ")"
    c.execute(createSecondaryIndex)
    con.commit()
    c.close()

    # Insertion into db
    con = sqlite3.connect('locations.sqlite')
    cur = con.cursor()
    try:

      cur.executemany("INSERT INTO " + location['table'] + "(id, name, url, review_count, categories, rating,"
                                                           "price, street, city, zip_code, state)"
                                                           "VALUES (:id, :name, :url, :review_count, :categories, :rating,"
                                                           ":price, :street, :city, :zip_code, :state)", formatted_restaurants)
      con.commit()
      con.close()
    except IOError:
      print("I/O error")

