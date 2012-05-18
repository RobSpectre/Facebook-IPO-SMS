import os
import signal

from flask import Flask
from flask import request
import requests
import simplejson as json

from twilio import twiml


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


# Voice Request URL
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    response = twiml.Response()
    quote = getFBQuote()
    response.say(quote)
    return str(response)


# SMS Request URL
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    response = twiml.Response()
    quote = getFBQuote()
    response.sms(quote)
    return str(response)


def getFBQuote():
    response = requests.get(
            "http://dev.markitondemand.com/Api/Quote/json?symbol=FB")
    try:
        if response.status == 200:
            data = json.loads(response.text)
        data = data['Data']
    except:
        return "Could not retrieve stock data.  Try again shortly."
    return "Last Price: %s Change Percent: %s  Timestamp: %s" % \
        (data['LastPrice'], data['ChangePercent'], data['Timestamp'])


@app.errorhandler(500)
def server_error():
    response = twiml.Response()
    if request.form['CallSid']:
        response.say("FB IPO is currently unavailable.  Try again shortly.")
    else:
        response.sms("FB IPO is currently unavailable.  Try again shortly.")
    return str(response)


# Handles SIGTERM so that we don't get an error when Heroku wants or needs to
# restart the dyno
def graceful_shutdown(signum, frame):
    exit()

signal.signal(signal.SIGTERM, graceful_shutdown)


# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
