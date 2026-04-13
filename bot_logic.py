import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random
import os
import json # Add this to handle the string-to-dict conversion

def process_coupon_request(user_id, username, message_text):
    # Setup connection using Environment Variable instead of a file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Get the JSON string from the environment
    creds_json = os.environ.get("GOOGLE_CREDS")
    creds_dict = json.loads(creds_json)
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # ... (rest of your logic remains exactly the same)
    spreadsheet = client.open("Copy of Frozelle Creamery")
    token_sheet = spreadsheet.worksheet("Token")
    log_sheet = spreadsheet.worksheet("Sheet1")
    
    all_tokens = token_sheet.get_all_records()
    available_indices = [i for i, row in enumerate(all_tokens) if row['Status'] == 'Available']
    
    if not available_indices:
        return "Sorry, we're out of coupons!"

    random_idx = random.choice(available_indices)
    chosen_row = all_tokens[random_idx]
    coupon_code = chosen_row['The Code']
    token_row_idx = random_idx + 2

    token_sheet.update_cell(token_row_idx, 2, "Unavailable")
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_sheet.append_row([now, user_id, username, message_text, coupon_code])
    
    return coupon_code