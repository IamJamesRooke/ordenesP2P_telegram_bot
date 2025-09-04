# OrdenesP2P Telegram Bot

A smart Telegram bot that monitors the OrdenesP2P group and finds your ideal Bitcoin trading counterparties with professional formatting.

**⚠️ CONFIGURE FIRST:** This bot is pre-configured for selling Bitcoin. If you're buying or want different rates, see the **Configuration** section below!

## What It Does

- 🔍 **Monitors** the OrdenesP2P Telegram group 24/7 using your personal account
- 🎯 **Smart Filtering:** Finds counterparties for YOUR trades:
  - `#BUYCOP` messages = **Buyers** (good if you're selling)
  - `#SELLCOP` messages = **Sellers** (good if you're buying)
  - `Tasa: yadio.io` (specific exchange rate provider)
  - **Inverted rate logic** - finds good rates for YOUR side of the trade
- 📱 **Instant Alerts** via your personal bot to your DM
- ✨ **Professional Formatting** with clickable links that open directly in Telegram

**Example Alert:**
```
*Buyer Found:* 20.000 - 100.000 COP 🇨🇴
*Rate:* yadio.io -1%
————————————
� View Offer
```

**Smart Rate Logic:**
- **#BUYCOP (buyers):** Finds rates close to market (good for you as seller)
- **#SELLCOP (sellers):** Finds rates close to market (good for you as buyer)

**Key Features:**
- **Finds counterparties** - buyers when you're selling, sellers when you're buying
- **Smart rate filtering** - automatically inverts logic for buy vs sell orders
- Clickable links open directly in Telegram app
- Clean, readable formatting with bold text
- **Configurable filtering** via `config.json` file (no code editing needed!)

---

## ⚙️ Configuration

The bot uses a `config.json` file for easy customization without editing code.

**🚨 IMPORTANT: Configure for YOUR trading strategy before running!**

### **Quick Start - Choose Your Strategy:**

#### **Strategy 1: You're SELLING Bitcoin (looking for buyers)**
```json
{
  "filters": {
    "hashtags": ["#BUYCOP"],
    "rate_thresholds": {
      "yadio.io": {
        "#BUYCOP": {
          "min_percentage": -1.0,
          "max_percentage": null
        }
      }
    }
  }
}
```
*This finds buyers offering -1% or better (no upper limit - higher premiums welcomed!)*

#### **Strategy 2: You're BUYING Bitcoin (looking for sellers)**
```json
{
  "filters": {
    "hashtags": ["#SELLCOP"],
    "rate_thresholds": {
      "yadio.io": {
        "#SELLCOP": {
          "min_percentage": null,
          "max_percentage": 1.0
        }
      }
    }
  }
}
```
*This finds sellers offering +1% or better (no lower limit - bigger discounts welcomed!)*

#### **Strategy 3: Both buying and selling**
```json
{
  "filters": {
    "hashtags": ["#BUYCOP", "#SELLCOP"],
    "rate_thresholds": {
      "yadio.io": {
        "#BUYCOP": {
          "min_percentage": -1.0,
          "max_percentage": null
        },
        "#SELLCOP": {
          "min_percentage": null,
          "max_percentage": 1.0
        }
      }
    }
  }
}
```

### **How to Configure:**
1. **Edit `config.json`** in the project root
2. **Copy one of the strategies above** (or see [CONFIG.md](CONFIG.md) for more options)
3. **Restart the bot** to apply changes

**📋 Need help?**
- **[CONFIG.md](CONFIG.md)** - Complete configuration guide with examples
- **[CONFIG_TEMPLATES.md](CONFIG_TEMPLATES.md)** - Ready-to-copy configuration templates

---

## 🔧 How It Works

### Advanced Filtering Logic:
1. **Monitors** OrdenesP2P group in real-time using your personal Telegram account
2. **First Filter:** Only processes messages containing `#BUYCOP`
3. **Second Filter:** Only processes messages with `Tasa: yadio.io` rate lines
4. **Third Filter:** Extracts percentage from rate (e.g., "yadio.io -1%")
5. **Rate Validation:** Only forwards offers between -1% to +1% of market price
6. **Message Formatting:** Extracts amount, formats with Markdown, creates clickable link
7. **Bot Delivery:** Sends via your personal bot to your DM

### Technical Architecture:
- **Telethon:** Reads messages from group using your personal account
- **Regex Parsing:** Extracts rates and percentages from message text
- **HTTP Bot API:** Sends formatted alerts via your dedicated bot
- **Markdown Formatting:** Bold text and clickable links for better UX

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
- Ensure your account can see messages in the group

### Only getting a few alerts per day
- This is expected! The bot has strict filtering (±1% rates only)
- Most P2P offers have higher premiums (2-5%+)
- The bot only forwards the best deals
- You can check console output to see filtered messages

### Links not opening in Telegram app
- Make sure you're clicking the link from within Telegram
- Links use t.me format which should open in-app
- If opening in browser, copy link and paste in Telegram

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
- **Dependencies:** 
  - `telethon==1.36.0` (Telegram client API)
  - `python-dotenv==1.0.1` (environment variable loading)
  - `httpx==0.27.0` (async HTTP client for bot API)
- **Architecture:** Personal account monitors group → Advanced filtering → Bot forwards alerts
- **Configuration:** JSON-based filtering system (no code editing required)
- **Filtering Capabilities:** 
  - Multiple hashtags (`#BUYCOP`, `#SELLCOP`)
  - Multiple rate providers (`yadio.io`, `binance.com`, etc.)
  - Configurable rate thresholds per provider
  - Customizable message formatting
- **Message Format:** Markdown with bold text and clickable t.me links
- **Storage:** Stateless - configuration loaded on startup, no data persistence
- **Performance:** Lightweight - only processes matching messages

---

## 📄 License

This is personal-use software. Use responsibly and follow Telegram's Terms of Service.
