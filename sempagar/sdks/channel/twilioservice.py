from twilio.rest import TwilioRestClient
import twilio.twiml
import config

def send_sms(msg_body, to_phone, from_phone):
	# Your Account Sid and Auth Token from twilio.com/user/account
	account_sid = config.twilio_access['account_sid']
	auth_token  = config.twilio_access['auth_token']
	client = TwilioRestClient(account_sid, auth_token)
	message = client.messages.create(body=msg_body, to=to_phone, from_=from_phone)
	return message.sid
