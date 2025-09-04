
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
        
        # Extract the specific lines we want
        lines = text.split('\n')
        amount_line = ""
        tasa_line = ""
        
        for line in lines:
            line = line.strip()
            if "COP" in line and ("Por " in line or any(char.isdigit() for char in line)):
                amount_line = line.replace("Por ", "")
            elif line.startswith("Tasa:"):
                tasa_line = line
        
        # Build the formatted message
        url = f"https://t.me/c/{event.chat_id}/{event.message.id}" if event.chat_id and event.message.id else ""
        formatted_message = f"{amount_line}\n{tasa_line}\nLink: {url}"
        
        await alerter.send(formatted_message)

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
