# Frozelle Instagram Coupon Bot 🍦

A production-ready automation pipeline that handles Instagram Direct Messages, validates keywords, and distributes randomized digital coupons while logging all transactions to a centralized database.

## 🚀 Features
- **Cloud-Native:** Deployed on **Render** using **Gunicorn** for production-grade request handling.
- **Secure Architecture:** Zero-credential footprint in source code; utilizes encrypted Environment Variables and Service Account JSON injection.
- **Real-time ETL:** Automatically extracts user data and coupon triggers, transforms timestamps, and loads records into **Google Sheets**.
- **Meta Integration:** Leverages the **Meta Graph API** Webhooks to listen for and respond to customer interactions instantly.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Framework:** Flask (REST API)
- **Server:** Gunicorn (WSGI)
- **APIs:** Meta Graph API (Instagram Graph), Google Sheets API (gspread)
- **Environment:** Render (Cloud Hosting), GitHub Actions (CI/CD)

## 📁 Project Structure
- `app.py`: The entry point for the Flask server and Webhook handshake.
- `bot_logic.py`: Contains the core logic for API calls, randomized coupon selection, and Google Sheets logging.
- `requirements.txt`: Managed dependencies for cloud environment consistency.
- `.env`: (Ignored) Local development secrets vault.
