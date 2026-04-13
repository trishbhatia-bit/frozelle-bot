import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv # <--- Add this

load_dotenv() # <--- This loads the variables from your .env file

def process_coupon_request(user_id, username, message_text):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # This looks for GOOGLE_CREDS in your .env (locally) or Render (cloud)
    creds_json = os.environ.get("GOOGLE_CREDS")
    creds_dict = json.loads(creds_json)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

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