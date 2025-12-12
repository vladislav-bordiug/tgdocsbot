from app.bot.utils import TelegramError

from aiogram import types

class StartHandler:

    async def start_handler(self, message: types.Message):
        try:
            await message.answer(
                text = """📄Этот бот принимает на вход файлы pdf, txt, md и docx\nБот суммаризирует содержание, извлекает ключевые слова и сохраняет результаты в файл:\n https://docs.google.com/spreadsheets/d/1FWCSV6riSNbNKpDuRT67mBvdhsXk_R5VtGbnThf6P58/edit?usp=sharing \nОтправьте файл для суммаризации""",
            )
        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err