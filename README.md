# New York City - Train Arrival

## Introduction
This application launches a GUI which displays the next several trains arriving at a given subway station.

## Requirements

Coming Soon... requirements.txt file with required Python Packages

### API Key
This application requires a development key from MTA.  You can apply for one here:
http://web.mta.info/developers/

Once you have this key, either load it into an environment variable using `$ MTA_API_KEY=[your api key]` or save it to a file called `api_key` saved in the project root directory.

## How to Run
Run using the command `$ python app.py [stop_id]` the stop_id can be found in `google_transit/stops.txt`.  Once the app is launched, clicking on the "Northbound" or "Southbound" indicator will change the direction.

The application updates from MTA's servers every 30 seconds by default.  

Coming Soon... ability to select different stops during runtime.
