from openai import AsyncOpenAI

class OpenAiTools:
    def __init__(self, token: str):
        self.client = AsyncOpenAI(
            api_key=token,
        )

    async def get_chatgpt(self, message: str):
        try:
            response = await self.client.responses.create(
                input=message,
                model="gpt-4o",
            )

            return response.output_text
        except:
            return

    async def get_summary(self, text: str):
        try:
            response = await self.get_chatgpt(
                message="Сделай короткую выжимку из текста в 3-7 предложений, текст:\n"+text,
            )
            return response
        except:
            return

    async def get_keywords(self, text: str):
        try:
            response = await self.get_chatgpt(
                message="Выведи 5-10 ключевых слова из текста через запятую, текст:\n"+text,
            )
            return response
        except:
            return