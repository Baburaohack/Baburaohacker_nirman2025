from twilio.rest import Client

# ✅ Correct Twilio credentials
account_sid = "A****5bbe871d9c5b******0eec3b42113"  # Replace with real Account SID
auth_token = "8d2bf***3d61***59cec******6eac0f"  # Replace with real Auth Token
to_phone_number = "+9163********"  # Replace with actual recipient number

client = Client(account_sid, auth_token)

try:
    message = client.messages.create(
        body="Test Message from Twilio 🚀",
        from_="+18285744436",  # Replace with your Twilio number
        to=to_phone_number,
    )
    print(f"✅ SMS Sent Successfully! SID: {message.sid}")
except Exception as e:
    print(f"❌ Error sending SMS: {e}")
