from aiogram import Dispatcher

from app.bot.handlers.start import StartHandler
from app.bot.handlers.docs import DocsHandler

from aiogram.filters.command import Command
from aiogram import F

from app.services.googlesheetstools import GoogleSheetTools
from app.services.languagedetect import DetectLanguageTool
from app.services.n8nparsefile import DocumentParserTool
from app.services.openaitools import OpenAiTools

def register_handlers(dp: Dispatcher, documentparsertool: DocumentParserTool,
                 openaitools: OpenAiTools,
                 googlesheettools: GoogleSheetTools,
                 languagedetect: DetectLanguageTool):
    Start_Handler = StartHandler()
    Docs_Handler = DocsHandler(documentparsertool, openaitools, googlesheettools, languagedetect)
    dp.message.register(Start_Handler.start_handler, Command('start'))
    dp.message.register(Docs_Handler.docs_handler, F.document)