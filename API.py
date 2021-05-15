from flask import Flask, render_template, request, redirect, url_for

from flask_mysqldb import MySQL
from geopy.geocoders import Nominatim
app = Flask('__name__')
locator = Nominatim(user_agent='__name__')  # instantiate locator with app

# Database config
app.config['MYSQL_HOST'] = '____________'  # host
app.config['MYSQL_USER'] = '____________'        # username
app.config['MYSQL_PASSWORD'] = '____________'  # password
app.config['MYSQL_DB'] = '____________'  # name of the database
app.config['MYSQL_CURSORCLASS'] = '____________'  # cursor class

mysql = MySQL(app)      # instantiate app with sql

# get user address
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        btn = request.form['button']
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
            cur.execute("INSERT INTO address_table(u_name,address,area,city,country,pincode) VALUES(%s,%s,%s,%s,%s,%s)",
                        (u_name, address, area, city, country, pincode))
            mysql.connection.commit()
            cur.close()
            return '<h2>Added</h2><br><hr>To view map: Change url to http://127.0.0.1:5000/getUserId '
        else:
            return redirect(url_for('getUserId'))
    return render_template('getUserInfo.html')

# getting user's id to check map
@app.route('/getUserId', methods=['GET', 'POST'])
def get_id():
    if request.method == 'POST':
        iid = request.form['id']
        print(iid)
        return redirect(url_for('mapping', i=iid))

    # fetch database to display
    headings = ("ID", "Name", "Address", "Area", "City", "Pincode", "Country") #since these are conctant i've hardcoded
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM address_table")
    data = cur.fetchall()
    return render_template('id.html', header=headings, data=data)


# Display user location in OSM
@app.route('/mapping<i>', methods=['GET', 'POST'])
def mapping(i):
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

    location = locator.geocode(area + ','+city+','+pincode+','+country)
    lat = location.latitude
    long = location.longitude

    print(lat, long)  # To check log
    print(Name)
    return render_template('leaf.html', lati=lat, longi=long, c_lati=c_lat, c_longi=c_long, name=Name)


# check main to run
if __name__ == "__main__":
    app.run(debug=True)
