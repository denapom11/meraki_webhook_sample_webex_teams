#!flask/bin/python

"""
Cisco Meraki Location Scanning Receiver

A simple example demonstrating how to interact with the CMX API.

How it works:
- Meraki access points will listen for WiFi clients that are searching for a network to join and log the events.
- The "observations" are then collected temporarily in the cloud where additional information can be added to
the event, such as GPS, X Y coordinates and additional client details.
- Meraki will first send a GET request to this CMX receiver, which expects to receieve a "validator" key that matches
the Meraki network's validator.
- Meraki will then send a JSON message to this application's POST URL (i.e. http://yourserver/ method=[POST])
- The JSON is checked to ensure it matches the expected secret, version and observation device type.
- The resulting data is sent to the "save_data(data)" function where it can be sent to a databse or other service
    - This example will simply print the CMX data to the console.

Default port: 5000

Cisco Meraki CMX Documentation
https://documentation.meraki.com/MR/Monitoring_and_Reporting/CMX_Analytics#CMX_Location_API

Written by Cory Guynn
2016

www.InternetOfLEGO.com
"""

# Libraries
from pprint import pprint
from flask import Flask
from flask import json
from flask import request
from flask import render_template
import sys, getopt
import json

############## USER DEFINED SETTINGS ###############
# MERAKI SETTINGS
webhook_data = "Webhook Data Goes Here"
secret = "secret goes here"
####################################################
app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_webhook_json():
    global webhook_data

    webhook_data = request.json
    pprint(webhook_data, indent=1)

    # Return success message
    return "WebHook POST Received"

# Launch application with supplied arguments
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:", ["secret="])
    except getopt.GetoptError:
        print("webhookreceiver.py -s <secret>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("webhookreceiver.py -s <secret>")
            sys.exit()
        elif opt in ("-s", "--secret"):
            secret = arg

    print("secret: " + secret)


if __name__ == "__main__":
    main(sys.argv[1:])
    app.run(host="0.0.0.0", port=5005, debug=False)
