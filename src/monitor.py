
import asyncio
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from .alerter import Alerter


async def main():
    load_dotenv()
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
        if "#BUYCOP" not in text:
            return
        
        # Check for Tasa: yadio.io line
        tasa_line = ""
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith("Tasa: yadio.io"):
                tasa_line = line
                break
        
        if not tasa_line:
            return  # No yadio.io rate found
        
        # Extract percentage from Tasa line (e.g., "Tasa: yadio.io -1%" or "Tasa: yadio.io +0.5%")
        import re
        percentage_match = re.search(r'([+-]?\d+(?:\.\d+)?)%', tasa_line)
        
        if percentage_match:
            try:
                percentage = float(percentage_match.group(1))
                # Filter: only -1% to +1% (inclusive)
                if not (-1.0 <= percentage <= 1.0):
                    return
            except ValueError:
                return  # Could not parse percentage
        # If no percentage found but has "yadio.io", assume 0% (market rate) and allow
        
        # Extract the specific lines we want
        lines = text.split('\n')
        amount_line = ""
        
        for line in lines:
            line = line.strip()
            if "COP" in line and ("Por " in line or any(char.isdigit() for char in line)):
                amount_line = line.replace("Por ", "")
        
        # Build the formatted message
        url = f"https://t.me/c/{event.chat_id}/{event.message.id}" if event.chat_id and event.message.id else ""
        
        # Extract rate part from tasa_line (e.g., "yadio.io -3%" from "Tasa: yadio.io -3%")
        rate_part = tasa_line.replace("Tasa: ", "")
        
        formatted_message = f"**Buy Offer:** {amount_line}\n**Rate:** {rate_part}\n**Link:** {url}"
        
        await alerter.send(formatted_message)

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
