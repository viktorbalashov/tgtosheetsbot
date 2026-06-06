# 📬 Telegram → Google Sheets Bot

Every message you send to this bot is saved into a **new sheet tab** inside a Google Sheets spreadsheet.

---

## 📁 Project Structure

```
tg-sheets-bot/
├── bot.py              # Main bot code
├── credentials.json    # Google Service Account key (YOU must add this)
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── Procfile            # For Railway / Render deployment
└── runtime.txt         # Python version for cloud platforms
```

---

## 🚀 Setup Guide

### Step 1 — Create a Telegram Bot
1. Open Telegram, find **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **Bot Token** you receive

---

### Step 2 — Set up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable these two APIs:
   - **Google Sheets API**
   - **Google Drive API**
4. Go to **IAM & Admin → Service Accounts** → Create a Service Account
5. After creating it, click on it → **Keys** tab → **Add Key → JSON**
6. Download the JSON file and **rename it to `credentials.json`**, place it in this folder
7. Open the JSON file and copy the `client_email` field (looks like `xxx@xxx.iam.gserviceaccount.com`)

---

### Step 3 — Create a Google Spreadsheet
1. Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet
2. **Share** the spreadsheet with the `client_email` from Step 2 (give it **Editor** access)
3. Copy the **Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/  <<<THIS_PART>>>  /edit
   ```

---

### Step 4 — Set Environment Variables

Create a `.env` file (copy from `.env.example`):
```
TELEGRAM_BOT_TOKEN=your_bot_token
SPREADSHEET_ID=your_spreadsheet_id
```

---

### Step 5 — Run Locally

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=your_token
export SPREADSHEET_ID=your_spreadsheet_id
python bot.py
```

---

### Step 6 — Deploy for Free on Railway

1. Go to [railway.app](https://railway.app) and sign up (free tier available)
2. Click **New Project → Deploy from GitHub repo**
3. Push this folder to a GitHub repo first, then connect it
4. In Railway dashboard, go to your project → **Variables** tab and add:
   - `TELEGRAM_BOT_TOKEN`
   - `SPREADSHEET_ID`
5. For `credentials.json`: go to **Variables → Raw Editor** and add a variable named `GOOGLE_CREDENTIALS` with the full JSON content. Then update `bot.py` to load from env (see note below*)
6. Railway will auto-detect the `Procfile` and run `python bot.py`

> *️⃣ **Tip for Railway:** Instead of uploading `credentials.json`, you can paste its entire contents as an environment variable. The bot already supports this — see the section below.

---

## 🔐 Using GOOGLE_CREDENTIALS env variable (recommended for cloud)

Instead of using a file, set an environment variable `GOOGLE_CREDENTIALS` with the **entire JSON content** of your service account key. The bot auto-detects this.

In `bot.py`, the `get_sheets_client()` function supports both methods:
- If `credentials.json` file exists → uses the file
- If `GOOGLE_CREDENTIALS` env var is set → uses the env var (recommended for Railway/Render)

---

## 📊 What Gets Saved

Each message creates a **new sheet tab** with this structure:

| Timestamp           | User ID   | Username  | Message          |
|---------------------|-----------|-----------|------------------|
| 2026-06-06 12:34:56 | 123456789 | john_doe  | Hello, world!    |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `SPREADSHEET_ID not found` | Make sure env variable is set |
| `403 Forbidden` on Sheets | Share the spreadsheet with the service account email |
| Bot not responding | Check the bot token is correct |
| `credentials.json not found` | Place the file in the same folder as `bot.py` |
