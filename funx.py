#funx
import wikipedia
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from config import *
import search_google.api
from datetime import datetime, timedelta


def help():
	r=MessagingResponse()
	r.message("<Command List>\nhlp: display this\nwiki <page>: search wikipedia for page\n\
image <search>: get image of search\nweather <zipcode>: get weather for zipcode\n\
def | definition <word>: get definition of word\ncrypto <btc>: get price of cryptocurrency\n")
	return str(r)

def error():
	r = MessagingResponse()
	msg = r.message("Error, no such command. Type hlp for list of commands")
	return str(r)

def crypto(oi):
	res = MessagingResponse()	

	url='https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD'.format(oi.upper())
	r = requests.get(url)
	price = json.loads(r.text)
	try:
		if price['Response'] == 'Error':
			res.message("Sorry, couldnt find that crypto currency")
	except:
		res.message(str(price['USD']))
	return str(res)


def wiki(msg):
	r = MessagingResponse()
	try:
		w = wikipedia.search(str(msg))[0]
		m = wikipedia.summary(w, sentences=6)
		r.message(str(m))
	except:
		r.message("No wiki page found")
	return str(r)


def defn(msg):
	res = MessagingResponse()
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + msg.lower()
	r = requests.get(url, headers={'app_id':APP_ID,'app_key':APP_KEY})

	try:
		j = json.loads(r.text)
		dfn = j["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
		res.message(dfn)
	except:
		res.message("Sorry, word not found")
	return str(res)
	

def weather(zip):
	res = MessagingResponse()
	url='http://api.wunderground.com/api/{}/conditions/q/CA/{}.json'.format(WEATHER_API,zip)
	r = requests.get(url)

	try:
		j = json.loads(r.text)

		temp_c=j["current_observation"]["temp_c"]
		temp_f=j["current_observation"]["temp_f"]
		loc = j["current_observation"]["display_location"]["full"]
		feel=j["current_observation"]["feelslike_string"]
		percip = j["current_observation"]["precip_today_string"]
	
		res.message("{}\nTemp: {}*C {}*F\nFeels like: {}\nPercipitation today: {}".format(loc,temp_c,temp_f,feel,percip))

	except:
		res.message("Couldnt get weather data, check zipcode")

	return str(res)


def image(k):
	res = MessagingResponse()
	argz={
		'serviceName':'customsearch',
		'version':'v1',
		'developerKey':API_KEY
	}
	data={
		'q': str(k),
		'cx':SEARCH_ID,
		'searchType':'image',
		'num':1,
		'safe':'off'
	}
	r=search_google.api.results(argz,data)
	try:	
		linkz = r.links
		title=r.get_values('items','title')[0]

		m = res.message(str(title))
		m.media(str(linkz[0]))

	except:
		res.message("Sorry, no image found")
	return str(res)



def noArg():
	res = MessagingResponse()
	res.message("Please enter an argument")
	return str(r)


def newUser():
	res = MessagingResponse()
	res.message("Register using command:\n register <username>")
	return str(res)


def short():
	res = MessagingResponse()
	res.message("Enter an argument")
	return str(res)


def stock(m):
	url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(m.upper(),STOCK_API)
	res = MessagingResponse()

	r = requests.get(url)
	j = json.loads(r.text)

	d=str(datetime.today())
	d = d.split(' ')[0]

	y = datetime.now() - timedelta(days=2)
	y.strftime('%m%d%y')
	y=str(y)
	y=y.split(' ')[0]

	try:
		price_l=j["Time Series (Daily)"][y]["3. low"]
		price_h=j["Time Series (Daily)"][y]["2. high"]
		res.message("Price low: {}\nPrice high: {}".format(price_l,price_h))
	except:
		res.message("Could not find stock")
	return str(res)