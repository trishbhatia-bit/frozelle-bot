import requests
from flask import Flask, request
from bot_logic import process_coupon_request
import os

app = Flask(__name__)

# CONFIGURATION - Updated with your Long-Lived Page Token
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN") # This looks for the token on the server
VERIFY_TOKEN = "frozelle_bot_2026" 
PAGE_ID = "1112375071951427"

# Memory to prevent duplicate processing
processed_mids = set()

def get_insta_username(user_id):
    """Fetches the handle (e.g., @burner_account) using the numeric User ID."""
    try:
        url = f"https://graph.facebook.com/v25.0/{user_id}?fields=username&access_token={ACCESS_TOKEN}"
        response = requests.get(url).json()
        return response.get('username', 'User')
    except Exception as e:
        print(f"Error fetching username: {e}")
        return "User"

def send_insta_dm(recipient_id, text_content):
    """Sends the actual message back to the user."""
    url = f"https://graph.facebook.com/v25.0/{PAGE_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text_content}
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Reply Response: {response.json()}") 
    return response.json()

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def handle_messages():
    data = request.json
    try:
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                
                message_data = messaging_event.get('message', {})
                message_id = message_data.get('mid')

                # 1. Skip if bot's own reply or duplicate message
                if message_data.get('is_echo') or message_id in processed_mids:
                    continue
                
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']
                    # Use .lower() for case-insensitive triggers
                    message_text = message_data.get('text', '').lower()
                    
                    # 2. Expanded keywords
                    keywords = ["coupon", "code", "#freeicecream", "#frozellecreamery"]
                    
                    if any(word in message_text for word in keywords):
                        processed_mids.add(message_id)
                        
                        # Keep memory clean
                        if len(processed_mids) > 100:
                            processed_mids.pop()

                        # 3. Process Logic & Get Username
                        username = get_insta_username(sender_id)
                        coupon = process_coupon_request(sender_id, username, message_text)
                        
                        # 4. Final Exclusive Reply
                        response_msg = f"🍦 Thanks @{username}! Your exclusive coupon code is: {coupon}"
                        send_insta_dm(sender_id, response_msg)
                        
    except Exception as e:
        print(f"Error processing webhook: {e}")
    return "ok", 200

if __name__ == '__main__':
    # This must match what Render expects
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)