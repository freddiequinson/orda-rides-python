from twilio.rest import Client
import random
import os

# Twilio credentials - in a real app, these would be environment variables
# For demo purposes, we'll use placeholder values
# You would need to sign up for a Twilio account and get these credentials
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'your_account_sid')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'your_auth_token')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+15005550006')  # This is a Twilio test number

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp(phone_number, otp):
    """Send OTP via SMS using Twilio"""
    try:
        # For demo purposes, we'll just print the OTP instead of actually sending it
        # In a real app, this would send an actual SMS
        print(f"Sending OTP {otp} to {phone_number}")
        
        # This is how you would send an actual SMS with Twilio
        # Uncomment this code and add your real Twilio credentials to send actual SMS
        """
        message = client.messages.create(
            body=f"Your OrDa Rides verification code is: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return message.sid
        """
        
        # For demo, just return a fake message ID
        return "SM" + str(random.randint(10000000000000000000, 99999999999999999999))
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return None
