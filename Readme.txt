OSM with Database functions.🗺
    "Simple integration of Open Street Map along with mySQL database functionalities.""

About:🅰
    I've created mySQL data base to get and store user's data(i.e location info.)
     In page getUserId.html data in the db is displayed.
      on entering the id of the user and on of "View map " button,
       opens OSM and points the location of the particular user witha marker.
        Also poits 1km distance around the user area.   

    Built with:👷‍♂️
        Python
        Flask
        Html
        Css
        Js
Prerequisities:📌
    instalation:
        pip install flask
        pip install flask_mysqldb
        pip install geopy
Usage:🎉
    In file api.py, line 09 to 13,
        enter your database credientials like "HOST","USERNAME","PASSWORD","NAME OF UR DB". 
    Copy the code which is in file "Create_Db.txt" and past it in the DB console and run.
        1.Run(--Table creation) then,
        2.Run(--initialize auto_inc)
        This creates a address_table to store user's address info.  
    run api.py file
      & go with the flow..✌

Acknowledgements Documentation:📃
    Nominatim-> https://nominatim.org/
    LeafletJs-> https://leafletjs.com/reference-1.7.1.html
    Maptiler->  https://www.maptiler.com/docs/
