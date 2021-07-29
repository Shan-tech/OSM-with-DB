from flask import Flask, render_template, request, redirect, url_for

from flask_mysqldb import MySQL
from geopy.geocoders import Nominatim
app = Flask('__name__')
locator = Nominatim(user_agent='__name__')  # instantiate locator with app

# Database config
app.config['MYSQL_HOST'] = 'localhost'  # host (localhost)
app.config['MYSQL_USER'] = 'root'        # username (root)
app.config['MYSQL_PASSWORD'] = 'Shan-tech'  # password
app.config['MYSQL_DB'] = 'osm'  # name of the database
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # cursor class (DICTCURSOR)

mysql = MySQL(app)      # instantiate app with sql

# get user address
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        btn = request.form['button']  #add map
        print(btn)
        print(request.form['city'])
        if btn == "add":
            u_name = request.form['name']
            address = request.form['address']
            area = request.form['area']
            city = request.form['city']
            country = request.form['country']
            pincode = request.form['pincode']
            print(u_name, address, area, city, country, pincode)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO address_table(u_name,house_no,area,city,country,pincode) VALUES(%s,%s,%s,%s,%s,%s)",
                        (u_name, address, area, city, country, pincode))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('get_id'))
        else:
            return redirect(url_for('get_id'))
    return render_template('getUserInfo.html')

# getting user's id to check map
@app.route('/getUserId', methods=['GET', 'POST'])
def get_id():
    if request.method == 'POST':
        iid = request.form['id']
        print(iid)
        print("@@@@@@@@@@@")
        return redirect(url_for('mapping', i=iid))

    # fetch database to display
    headings = ("ID", "Name", "HouseNo.", "Area", "City", "Pincode", "Country") #since these are conctant i've hardcoded
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM address_table")
    data = cur.fetchall()
    return render_template('getUserId.html', header=headings, data=data)


# Display user location in OSM
@app.route('/mapping<i>', methods=['GET', 'POST'])
def mapping(i): #110
    # fetch address
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM address_table WHERE id=%s" % i)  # here i is the id of user(auto_increment primary key i DB)
    db = cur.fetchall()
    #since data from db will be like a dict inside tupple (i.e) "({"key":"value"},)"
    # so can accessed like this ↙
    Name = db[0]['u_name']
    area = db[0]['area']
    city = db[0]['city']
    pincode = str(db[0]['pincode'])
    country = db[0]['country']

    # locator for map
    c_location = locator.geocode(area+","+pincode)
    c_lat = c_location.latitude
    c_long = c_location.longitude
    print("@@@@@@@@@@@@@@@@@@")
    print(c_lat,c_long);
    location = locator.geocode(area + ','+city+','+pincode+','+country)
    lat = location.latitude
    long = location.longitude

    print(lat, long)  # To check log
    print(Name)
    return render_template('leaflet.html', lati=lat, longi=long, c_lati=c_lat, c_longi=c_long, name=Name)


# check main to run
if __name__ == "__main__":
    app.run(debug=True)
