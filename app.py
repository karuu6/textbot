from flask import Flask, request, redirect
from funx import *
from register import *

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():

	num = request.values.get('From')
	body = request.values.get('Body',None)
	body=body.split('\n')[0]
	msg_type, msg = parseMsg(body)


	if check(num) == False and msg_type!='register':
		return newUser()
	else:

		if len(msg) < 1:
			return short()

		if len(msg)<1 and msg_type!='hlp': 
			msg_type='no_arg'
		elif msg_type=='register':
			return register(msg,num)
		else:
			return reply(msg_type,msg)

def parseMsg(n):
	msg = str(n).split(' ')
	_type = msg[0].lower()
	msg.pop(0)
	body = str(' '.join(msg))

	return (_type, body)

def reply(_type,msg):
	if _type=='no_arg':
		return noArg()
	elif _type=='stock':
		return stock(msg)
	elif _type=='wiki':
		return wiki(msg)
	elif _type=='price':
		return crypto(msg)
	elif _type=='hlp':
		return help()
	elif _type=='image':
		return image(msg)
	elif _type=='definition':
		return defn(msg)
	elif _type=='def':
		return defn(msg)
	elif _type=='crypto':
		return crypto(msg)
	elif _type=='weather':
		return weather(msg)
	elif _type=='pic':
		return image(msg)

	else:
		return error()



if __name__ == "__main__":
	app.run()