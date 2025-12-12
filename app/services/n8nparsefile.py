import aiohttp
import asyncio
from typing import Optional, BinaryIO


class DocumentParserTool:

    def __init__(
        self,
        webhook_url: str,
        *,
        timeout: int = 60,
    ):
        self.webhook_url = webhook_url
        self.timeout = timeout

        self._session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()


    async def _init(self):
        if self._session:
            return

        async with self._lock:
            if self._session:
                return

            timeout = aiohttp.ClientTimeout(total=self.timeout)

            self._session = aiohttp.ClientSession(
                timeout=timeout,
            )

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def parse_bytes(
        self,
        buffer: BinaryIO,
        *,
        filename: str,
        mime_type: str,
    ) -> dict:

        await self._init()

        form = aiohttp.FormData()

        form.add_field(
            name="data",
            value=buffer,
            filename=filename,
            content_type=mime_type,
        )

        async with self._session.post(self.webhook_url, data=form) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(
                    f"Parser error {resp.status}: {text}"
                )

            res = await resp.json()
            return res
