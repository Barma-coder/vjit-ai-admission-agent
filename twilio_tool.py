import os
from twilio.rest import Client  # <--- MUST HAVE THIS LINE
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_alert(message_body):
    # Fetch credentials from .env
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM")
    to_whatsapp = os.getenv("MY_WHATSAPP_NUMBER")

    # WHATSAPP LIMIT PROTECTION (1600 Characters)
    if len(message_body) > 1600:
        message_body = message_body[:1597] + "..."
        print("⚠️ Warning: Message truncated to stay under 1600 chars.")

    try:
        # Initializing the Twilio Client
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        print(f"✅ WhatsApp alert sent! SID: {message.sid}")
        return True
    except Exception as e:
        # This will catch if keys are missing or numbers aren't joined to sandbox
        print(f"❌ Failed to send WhatsApp: {e}")
        return False