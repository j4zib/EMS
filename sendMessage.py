from twilio.rest import Client
from setup import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

#Create an account on Twilio and get account_sid and auth_token
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

def getClient():
	return client
