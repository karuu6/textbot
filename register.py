import sqlite3
from twilio.twiml.messaging_response import MessagingResponse


	
def initDB():
	conn = sqlite3.connect('userz.db')
	c = conn.cursor()

	c.execute('CREATE TABLE IF NOT EXISTS userz (user text, phone text)')
	conn.commit()

	return (c,conn)

def register(msg,num):
	c,conn=initDB()

	r=MessagingResponse()
	user=c.execute("SELECT * FROM userz WHERE user=?",(msg,))
	user=c.fetchone()

	phone=c.execute("SELECT * FROM userz WHERE phone=?",(num,))
	phone=c.fetchone()

	if user is not None:
		r.message("User already exists")
		return str(r)
	elif phone is not None:
		r.message("Phone number already registered")
		return str(r)

	c.execute("INSERT INTO userz VALUES (?,?)",(str(msg),str(num)))
	conn.commit()

	chek=c.execute("SELECT * FROM userz WHERE phone=?", (num,))
	chek=c.fetchone()

	if chek is not None:
		r.message("User registered!\nHi {}! I am TextBot\nType hlp for a list of commands".format(msg))
	else:
		r.message("Error registering :(")
	conn.close()
	return str(r)



def check(num):
	c,conn=initDB()
	chek=c.execute("SELECT * FROM userz WHERE phone=?", (num,))
	chek=c.fetchone()
	
	if chek is None:
		conn.close()
		return False
	else:
		conn.close()
		return True