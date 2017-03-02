import requests
import json

def queryPrice(symbol, max_tries = 3):
	tries = 1
	url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20csv%20where%20url%3D%27http%3A%2F%2Fdownload.finance.yahoo.com%2Fd%2Fquotes.csv%3Fs%3D" + symbol + "%26f%3Dsl1d1t1c1ohgv%26e%3D.csv%27%20and%20columns%3D%27symbol%2Cprice%2Cdate%2Ctime%2Cchange%2Ccol1%2Chigh%2Clow%2Ccol2%27&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
	while tries <= max_tries:
		try:
			r = requests.get(url)
			res = json.loads(r.text)["query"]["results"]["row"]
			price = float(res["price"])
			return price
		except:
			tries += 1
			if tries == max_tries:
				return None
				
def feedback_context_fill(msg, title, result, link, button = "Retry"):
	feedback = {
			"feedback_msg": msg, 
			"title": title, 
			"result": result,
			"link": link,
			"button": button,
		}
	return feedback
	
def validate_password(password, password_conf):
	# check password length
	if len(password) < 6:
		return "Password must be at least 6 characters long. Please try again!"
	# check password match
	if password != password_conf:
		return "Password and password confirmation fields must match. Please try again!"
	# check for at least 1 digit and 1 letter
	if not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
		return "Your password must contain at least 1 digit and 1 alphabetic character. Please try again!"
	return None