# New York City - Train Arrival

## Introduction
This application launches a GUI which displays the next several trains arriving at a given subway station.

## Screen Layout
The screen layout is optimized for a 480x320px touchscreen display.  The cursor is hidden during operation.  There is currently no means of configuring the application other than modifying source code.  

## Requirements

Requirements are included in `requirements.txt`.  Run `pip install -r requirements.txt` to install missing Python packages.

### API Key
You can apply for one here:
http://web.mta.info/developers/

Once you have this key, either load it into an environment variable using `$ MTA_API_KEY=[your api key]` or save it to a file called `api_key` saved in the project root directory.  The latest version of this application uses data from [nyc-train-arrival-server](https://github.com/bcpearce/nyc-train-arrival-server).  

## How to Run
Run using the command `$ python app.py [stop_id] [server](optional)` the stop_id can be found in `google_transit/stops.txt`.  Once the app is launched, clicking on the "Northbound" or "Southbound" indicator will change the direction.  By default the server will look for port 5000 on your localhost, otherwise you may specify an external server.  

The application updates from the server every 30 seconds by default.  

### Stop Selection

Selecting the direction indicator will reverse the direction.  In NYC subway parlance, there is only Northbound and Southbound.  For available stops, Northbound trains head towards uptown Manhattan and the Bronx.  Southbound trains head towards downtown Manhattan and Brooklyn.

Selecting the Station Name will open a selection window to choose other stations.
