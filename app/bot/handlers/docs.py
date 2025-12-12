from app.bot.utils import TelegramError

from aiogram import types
from io import BytesIO
from datetime import datetime, timezone

from app.services.googlesheetstools import GoogleSheetTools
from app.services.languagedetect import DetectLanguageTool
from app.services.n8nparsefile import DocumentParserTool
from app.services.openaitools import OpenAiTools

ALLOWED_EXT = {
    "pdf",
    "txt",
    "md",
    "docx",
}

class DocsHandler:
    def __init__(self, documentparsertool: DocumentParserTool,
                 openaitools: OpenAiTools,
                 googlesheettools: GoogleSheetTools,
                 languagedetect: DetectLanguageTool):
        self.documentparsertool = documentparsertool
        self.openaitools = openaitools
        self.googlesheettools = googlesheettools
        self.languagedetect = languagedetect

    async def docs_handler(self, message: types.Message):
        try:
            document = message.document

            ext = document.file_name.split(".")[-1].lower()

            if not ext in ALLOWED_EXT:
                await message.answer(
                    "❌ Поддерживаются только PDF, TXT, DOCX и MD"
                )
                return

            await message.answer("⏳ Получил файл, обрабатываю...")

            file = await message.bot.get_file(document.file_id)

            buffer = BytesIO()
            await message.bot.download_file(file.file_path, buffer)
            buffer.seek(0)

            result = await self.documentparsertool.parse_bytes(
                buffer=buffer,
                filename=document.file_name,
                mime_type=document.mime_type,
            )

            if "fileName" not in result:
                result["fileName"] = document.file_name
            if "fileSize" not in result:
                result["fileSize"] = ""
            if "fileType" not in result:
                result["fileType"] = ""
            if "fileText" not in result:
                result["fileText"] = ""

            result["user"] = message.from_user.username

            result["summary"] = await self.openaitools.get_summary(result["fileText"])

            result["keywords"] = await self.openaitools.get_keywords(result["fileText"])

            result["language"] = self.languagedetect.detect_language(result["fileName"]+result["fileText"])

            result["time"] = datetime.now(timezone.utc).isoformat()

            await message.answer(
                f"📄 Обработан файл:\n"
                f"Имя: {result['fileName']}\n"
                f"Размер: {result['fileSize']}\n"
                f"Тип: {result['fileType']}\n"
                f"Язык: {result['language']}\n"
                f"Время обработки: {result['time']}\n"
                f"Автор: {result['user']}\n"
                f"Выжимка: {result['summary']}\n"
                f"Ключевые слова: {result['keywords']}\n"
            )

            await self.googlesheettools.append_row([
                result["fileName"],
                result["fileSize"],
                result["fileType"],
                result["language"],
                result["time"],
                result["user"],
                result["summary"],
                result["keywords"],
            ])

        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err