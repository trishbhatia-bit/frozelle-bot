import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random

def process_coupon_request(user_id, username, message_text):
    # 1. Setup connection
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    
    # 2. Open spreadsheet and worksheets
    spreadsheet = client.open("Copy of Frozelle Creamery")
    token_sheet = spreadsheet.worksheet("Token")
    log_sheet = spreadsheet.worksheet("Sheet1")
    
    # 3. Get all tokens and find 'Available' ones
    all_tokens = token_sheet.get_all_records()
    # List of indices for rows that are still available
    available_indices = [i for i, row in enumerate(all_tokens) if row['Status'] == 'Available']
    
    if not available_indices:
        return "Sorry, we're out of coupons for today!"

    # 4. PICK A RANDOM INDEX
    random_idx = random.choice(available_indices)
    chosen_row = all_tokens[random_idx]
    
    coupon_code = chosen_row['The Code']
    # Spreadsheet row = index + 2 (1 for header, 1 for 0-based index)
    sheet_row_to_update = random_idx + 2

    # 5. Update 'Token' tab status to 'Unavailable'
    token_sheet.update_cell(sheet_row_to_update, 2, "Unavailable")
    
    # 6. Log detailed transaction to 'Sheet1'
    # Columns: Date/Time, User ID, Username, Message, Coupon
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_sheet.append_row([now, user_id, username, message_text, coupon_code])
    
    return coupon_code