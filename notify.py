from twilio.rest import Client
import time

# ✅ Twilio credentials (Replace with actual values)
account_sid = "AC4665b********c7f2d2****b42113"
auth_token = "8d*******************c728d3c6eac0f"
to_phone_number = "+91**********"  # Replace with actual recipient number

client = Client(account_sid, auth_token)


def send_sms(body):
    """Send an SMS using Twilio."""
    try:
        message = client.messages.create(
            body=body,
            from_="+182*******6",  # Your Twilio number
            to=to_phone_number,
        )
        print(f"✅ SMS Sent Successfully! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending SMS: {e}")


def generate_messages():
    """Generate messages for 20 iterations and send SMS on the 15th iteration."""
    for i in range(1, 21):  # Run for 20 iterations
        if i == 15:
            print(f"Iteration {i}: Failure Probability >75% ⚠️")
            send_sms("⚠️ Alert: Failure detected at iteration 15!")
        else:
            print(f"Iteration {i}: No Failure ✅")

        time.sleep(1)  # 1-second delay between messages


if __name__ == "__main__":
    generate_messages()
