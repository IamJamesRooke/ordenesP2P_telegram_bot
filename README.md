# OrdenesP2P Telegram Bot

A personal Telegram bot that monitors the OrdenesP2P group and forwards filtered messages to your DM with clean formatting.

## What It Does

- 🔍 **Monitors** the OrdenesP2P Telegram group 24/7
- 🎯 **Filters** for #BUYCOP messages only  
- 📱 **Forwards** to your personal DM via bot
- ✨ **Formats** messages to show only: Amount, Rate, and Link

**Example Output:**
```
20.000 - 100.000 COP 🇨🇴
Tasa: yadio.io -1%
Link: https://t.me/c/-1001696822031/19126
```

---

## 🚀 Quick Setup Guide

### Step 1: Get Telegram API Credentials

1. **Go to [my.telegram.org](https://my.telegram.org)**
2. **Login** with your phone number
3. **Click "API Development Tools"**
4. **Create new application:**
   - App title: `OrdenesP2P Monitor` (or any name)
   - Short name: `ordenesp2pbot` (alphanumeric, 5-32 chars)
   - URL: Leave blank
   - Platform: Desktop
   - Description: `Personal bot for monitoring P2P offers`
5. **Save your API_ID and API_HASH** (keep them secret!)

### Step 2: Create Alert Bot

1. **Message [@BotFather](https://t.me/BotFather)** on Telegram
2. **Send `/newbot`**
3. **Follow prompts** to create your bot
4. **Save the bot token** (looks like `123456:ABC-DEF...`)
5. **Start a chat with your new bot** (send any message)
6. **Get your chat ID:**
   - Open: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find `"message":{"from":{"id":NUMBERS}}`
   - Save that number as your chat ID

### Step 3: Install on Your Device

#### **iPhone (iSH Shell):**
```bash
# Install iSH Shell from App Store

# In iSH, install dependencies:
apk update
apk add python3 py3-pip git screen

# Clone the bot:
git clone https://github.com/IamJamesRooke/ordenesP2P_telegram_bot.git
cd ordenesP2P_telegram_bot

# Install Python packages:
pip3 install telethon python-dotenv httpx
```

#### **Windows/Mac/Linux:**
```bash
# Clone the repository:
git clone https://github.com/IamJamesRooke/ordenesP2P_telegram_bot.git
cd ordenesP2P_telegram_bot

# Create virtual environment:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install dependencies:
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file with your credentials:

```bash
# Create .env file:
nano .env  # iPhone/Linux
# OR use any text editor on Windows/Mac
```

**Add this content (replace with your actual values):**
```env
API_ID=your_api_id_here
API_HASH=your_api_hash_here
PHONE_NUMBER=+1234567890
GROUP=https://t.me/OrdenesP2P
BOT_TOKEN=your_bot_token_here
ALERT_CHAT_ID=your_numeric_chat_id_here
SESSION_NAME=session
```

### Step 5: Run Your Bot

#### **iPhone (24/7 operation):**
```bash
# Start in background session:
screen -S telegram_bot

# Run the bot:
python3 -m src.monitor

# Detach to run in background:
# Press Ctrl+A then D

# Later, reconnect:
screen -r telegram_bot
```

#### **Computer:**
```bash
python -m src.monitor
```

---

## 📱 iPhone Setup for 24/7 Operation

### iOS Settings:
1. **Settings → Battery** → Turn OFF "Low Power Mode"
2. **Settings → General → Background App Refresh** → Enable for iSH
3. **Settings → Display & Brightness → Auto-Lock** → Set to "Never"
4. Keep iPhone plugged in/charging
5. Keep iSH app active (don't fully close it)

### Battery Optimization:
- Turn OFF "Optimized Battery Charging"
- Ensure no Screen Time limits on iSH
- Consider Airplane Mode + WiFi (saves battery)

---

## 🔧 Updating the Bot

When new features are added:

```bash
cd ordenesP2P_telegram_bot
git pull origin main
# Your .env file stays safe!
python3 -m src.monitor
```

---

## ❓ Troubleshooting

### "No module named 'telethon'"
```bash
pip3 install telethon python-dotenv httpx
```

### "Missing API_ID or API_HASH"
- Check your `.env` file exists and has the right values
- Make sure there are no extra spaces or quotes

### Bot not receiving messages
- Make sure you're a member of OrdenesP2P group
- Check your phone has good internet connection
- Verify bot token and chat ID are correct

### iPhone bot stops working
- Check Background App Refresh is enabled
- Ensure iSH app isn't being closed by iOS
- Use `screen` to run in background
- Keep phone charging

---

## 🔒 Security Notes

- **Never share** your API_ID, API_HASH, or bot token
- **Don't commit** your `.env` file to git
- Your personal Telegram account is used to read messages
- The bot only forwards filtered messages, doesn't store anything

---

## 🛠️ Technical Details

- **Language:** Python 3
- **Libraries:** Telethon (Telegram client), httpx (HTTP requests), python-dotenv (environment variables)
- **Architecture:** Personal account monitors group → Bot forwards filtered messages
- **Filtering:** Only #BUYCOP hashtag messages
- **Formatting:** Extracts amount, rate, and link only

---

## 📄 License

This is personal-use software. Use responsibly and follow Telegram's Terms of Service.
