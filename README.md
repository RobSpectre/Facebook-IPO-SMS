# Facebook IPO SMS Monitor 

A dainty Twilio application that gives you an update on Facebook's stock price.

[![Build
Status](https://secure.travis-ci.org/RobSpectre/Facebook-IPO-SMS.png)]
(http://travis-ci.org/RobSpectre/Facebook-IPO-SMS)


## Summary

On the M train from Manhattan to Brooklyn during the day of the Facebook IPO, I
was bummed I couldn't get updates through the spotty data connection.  To
rectify this for me and the other Twilio developer evangelists who were on the
hoof on the big day, I did up a quick app to deliver the latest quote on $FB's
stock price.

As per usual, I depended on the  [Twilio Hackpack for Heroku and
Flask](https://github.com/RobSpectre/Twilio-Hackpack-for-Heroku-and-Flask) and
got data from [MarkitOnDemand](http://dev.markitondemand.com/).

## Usage

Text anything to (612) 213-2476 to see it work!

![Example of it
working](https://raw.github.com/RobSpectre/Facebook-IPO-SMS/master/images/usage.png)


## Installation

Step-by-step on how to deploy and develop this app.

### Deploy 

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Facebook-IPO-SMS.git 
</pre>

2) Install dependencies
<pre>
make init
</pre>

3) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create --stack cedar
</pre>

4) Deploy to Heroku
<pre>
git push heroku master
</pre>

5) Scale your dynos
<pre>
heroku scale web=1
</pre>

6) Configure a new TwiML app and Twilio phone number to use the app.
<pre>
python configure.py --account_sid ACxxxxxx --auth_token yyyyyyy -n -N
</pre>

7) Text the new number and watch the news!


### Development

Be sure to follow the configuration steps above and use this step-by-step guide to tweak to your heart's content.

1) Install the dependencies.
<pre>
make init
</pre>

2) Launch local development webserver
<pre>
foreman start
</pre>

3) Open browser to [http://localhost:5000](http://localhost:5000).

4) Tweak away on `app.py`.


## Testing

Better believe I tested this once-in-a-decade OMGWTFBBQ event.

<pre>
make test
</pre>



## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 
