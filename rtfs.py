import urllib2
import os

MTA_URL = "http://datamine.mata.info/mta_esi.php?key={0}&feed_id={1}"

def get_feed(feed_id, api_key=None):

    if not api_key:
        api_key = os.environ['MTA_API_KEY']

    response = urllib.urlopen(MTA_URL.format(api_key, feed_id))

    return response.read()


if __name__ == "__main__":

    print get_feed(1)

