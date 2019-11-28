from twilio.rest import Client


#Create an account on Twilio and get account_sid and auth_token
account_sid = 'YOUR ACCOUNT SID HERE'
auth_token = 'YOUR AUTH TOKEN HERE'
client = Client(account_sid, auth_token)

def getClient():
	return client
