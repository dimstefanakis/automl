import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()

# Your Account SID from twilio.com/console
account_sid = os.environ.get('TWILIO_SID')
# Your Auth Token from twilio.com/console
auth_token = os.environ.get('TWILIO_TOKEN')

client = Client(account_sid, auth_token)

message = client.messages.create(
    to=os.environ.get('MY_NUMBER'),
    from_=os.environ.get('TWILIO_NUMBER'),
    body="Hello from Python!")

print(message.sid)
