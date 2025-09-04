import asyncio
import os
from typing import Optional

import httpx


class Alerter:
    def __init__(self, bot_token: Optional[str], chat_id: Optional[str]) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def send(self, text: str) -> None:
        if not self.bot_token or not self.chat_id:
            print(f"{os.getenv('FALLBACK_PREFIX', 'ALERT')}: {text}")
            return

        url = f"{os.getenv('TELEGRAM_API_URL', 'https://api.telegram.org')}/bot{self.bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=int(os.getenv('HTTP_TIMEOUT', '10'))) as client:
            try:
                await client.post(url, json={
                    "chat_id": self.chat_id, 
                    "text": text, 
                    "parse_mode": "Markdown"
                })
            except Exception as e:
                print(f"{os.getenv('ERROR_PREFIX', 'Failed to send alert via bot')}: {e}. Falling back to console.\n{text}")
