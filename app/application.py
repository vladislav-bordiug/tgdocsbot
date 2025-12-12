import os
from dotenv import load_dotenv
import logging
import asyncio

from aiogram import Bot, Dispatcher

from app.services.googlesheetstools import GoogleSheetTools
from app.services.languagedetect import DetectLanguageTool
from app.services.n8nparsefile import DocumentParserTool
from app.services.openaitools import OpenAiTools

from app.bot.setup import register_handlers

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(
    token=TOKEN
)

dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    openai_tools = OpenAiTools(os.getenv("OPENAI_API_KEY"))
    googlesheettools = GoogleSheetTools(os.getenv("SPREADSHEET_ID"))
    detectlanguagetool = DetectLanguageTool()
    documentparsertool = DocumentParserTool(os.getenv("N8N_WEBHOOK_URL"))
    register_handlers(dp, documentparsertool, openai_tools, googlesheettools, detectlanguagetool)
    asyncio.run(main())