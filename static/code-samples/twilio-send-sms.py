from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "ACf3f0805e01bc0a3db41e7aae79bc96d5" 
AUTH_TOKEN = "acf544c7ffb70d7b888eabc81d75698a" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
	to="2063838296", 
	from_="+14012065509", 
	body="Hi Adam! Just checking: are you signing up for TurnedOn? Say yes or no!",  
)
