import asyncio
import gspread_asyncio
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = Path(__file__).resolve().parent
def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name(
        BASE_DIR / "credentials.json",
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    )

class GoogleSheetTools:
    def __init__(self, spreadsheet_id: str):
        self.agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
        self.spreadsheet_id = spreadsheet_id

        self._client = None
        self._spreadsheet = None
        self._sheet = None
        self._lock = asyncio.Lock()

    async def _init(self):
        if self._sheet:
            return

        async with self._lock:
            if self._sheet:
                return

            self._client = await self.agcm.authorize()
            self._spreadsheet = await self._client.open_by_key(self.spreadsheet_id)
            self._sheet = await self._spreadsheet.worksheet("Лист1")

    async def append_row(self, data: list):
        await self._init()
        await self._sheet.append_row(data)