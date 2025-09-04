import asyncio
import os
import json
import re
from pathlib import Path
from telethon import TelegramClient, events
from dotenv import load_dotenv
from .alerter import Alerter


def load_config():
    """Load configuration from config.json file"""
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}. Using default settings.")
        # Default configuration if file doesn't exist
        return {
            "filters": {
                "hashtags": ["#BUYCOP", "#SELLCOP"],
                "rate_providers": ["yadio.io"],
                "rate_thresholds": {
                    "yadio.io": {
                        "#BUYCOP": {"min_percentage": -1.0, "max_percentage": None},
                        "#SELLCOP": {"min_percentage": None, "max_percentage": 1.0}
                    }
                }
            },
            "formatting": {
                "buy_prefix": "*Buyer Found:*",
                "sell_prefix": "*Seller Found:*",
                "rate_prefix": "*Rate:*",
                "separator": "————————————",
                "link_text": "📱 View Offer"
            }
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing config.json: {e}. Using default settings.")
        # Return default config if JSON is invalid
        return {
            "filters": {
                "hashtags": ["#BUYCOP", "#SELLCOP"],
                "rate_providers": ["yadio.io"],
                "rate_thresholds": {
                    "yadio.io": {
                        "#BUYCOP": {"min_percentage": -1.0, "max_percentage": None},
                        "#SELLCOP": {"min_percentage": None, "max_percentage": 1.0}
                    }
                }
            },
            "formatting": {
                "buy_prefix": "*Buyer Found:*",
                "sell_prefix": "*Seller Found:*",
                "rate_prefix": "*Rate:*",
                "separator": "————————————",
                "link_text": "📱 View Offer"
            }
        }


async def main():
    load_dotenv()
    config = load_config()
    
    client = TelegramClient(
        os.getenv("SESSION_NAME") or "session",
        int(os.getenv("API_ID")),
        os.getenv("API_HASH")
    )
    await client.start(phone=os.getenv("PHONE_NUMBER"))
    entity = await client.get_entity(os.getenv("GROUP"))
    bot_token = os.getenv("BOT_TOKEN")
    alert_chat_id = os.getenv("ALERT_CHAT_ID")
    from .alerter import Alerter
    alerter = Alerter(bot_token, alert_chat_id)

    @client.on(events.NewMessage(chats=entity))
    async def handler(event):
        text = event.message.message or ""
        if not text.strip():
            return
        
        # Check if message contains any of the required hashtags
        hashtags = config["filters"]["hashtags"]
        has_hashtag = any(hashtag in text for hashtag in hashtags)
        if not has_hashtag:
            return
        
        # Determine message type for formatting
        is_buy_order = "#BUYCOP" in text
        is_sell_order = "#SELLCOP" in text
        
        # Check for rate provider lines
        rate_providers = config["filters"]["rate_providers"]
        tasa_line = ""
        rate_provider = None
        
        for line in text.split('\n'):
            line = line.strip()
            for provider in rate_providers:
                if line.startswith(f"Tasa: {provider}"):
                    tasa_line = line
                    rate_provider = provider
                    break
            if tasa_line:
                break
        
        if not tasa_line or not rate_provider:
            return  # No matching rate provider found
        
        # Extract percentage from Tasa line
        percentage_match = re.search(r'([+-]?\d+(?:\.\d+)?)%', tasa_line)
        
        if percentage_match:
            try:
                percentage = float(percentage_match.group(1))
                
                # Get the appropriate threshold based on order type
                rate_thresholds = config["filters"]["rate_thresholds"].get(rate_provider, {})
                
                if is_buy_order:  # #BUYCOP - looking for buyers (you're selling)
                    thresholds = rate_thresholds.get("#BUYCOP", {})
                    min_pct = thresholds.get("min_percentage", -1.0)
                    max_pct = thresholds.get("max_percentage", None)  # Default unlimited
                elif is_sell_order:  # #SELLCOP - looking for sellers (you're buying)
                    thresholds = rate_thresholds.get("#SELLCOP", {})
                    min_pct = thresholds.get("min_percentage", None)  # Default unlimited
                    max_pct = thresholds.get("max_percentage", 1.0)
                else:
                    # Fallback for unknown order type
                    min_pct, max_pct = -1.0, 1.0
                
                # Handle unlimited values (null means no limit)
                if min_pct is None:
                    min_pct = float('-inf')
                if max_pct is None:
                    max_pct = float('inf')
                
                # Apply the rate filter (direct logic per order type)
                if not (min_pct <= percentage <= max_pct):
                    return  # Rate outside configured range
                    
            except ValueError:
                return  # Could not parse percentage
        # If no percentage found but has rate provider, assume 0% (market rate) and allow
        
        # Extract the specific lines we want
        lines = text.split('\n')
        amount_line = ""
        
        for line in lines:
            line = line.strip()
            if "COP" in line and ("Por " in line or any(char.isdigit() for char in line)):
                amount_line = line.replace("Por ", "")
        
        # Build the formatted message
        # Use t.me format that opens in Telegram app
        if event.chat_id and event.message.id:
            # Convert chat_id to proper format for t.me links
            chat_id_str = str(event.chat_id)
            if chat_id_str.startswith('-100'):
                # Remove -100 prefix for supergroup links
                clean_chat_id = chat_id_str[4:]
                url = f"https://t.me/c/{clean_chat_id}/{event.message.id}"
            else:
                url = f"https://t.me/c/{event.chat_id}/{event.message.id}"
        else:
            url = "No link available"
        
        # Extract rate part from tasa_line
        rate_part = tasa_line.replace("Tasa: ", "")
        
        # Use appropriate formatting based on message type
        formatting = config["formatting"]
        if is_buy_order:
            order_prefix = formatting["buy_prefix"]
        elif is_sell_order:
            order_prefix = formatting["sell_prefix"]
        else:
            order_prefix = "*Offer:*"  # Fallback
        
        formatted_message = (
            f"{order_prefix} {amount_line}\n"
            f"{formatting['rate_prefix']} {rate_part}\n"
            f"{formatting['separator']}\n"
            f"[{formatting['link_text']}]({url})"
        )
        
        await alerter.send(formatted_message)

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
