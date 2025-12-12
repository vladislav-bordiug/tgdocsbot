import logging

class TelegramError(Exception):
    def __init__(self, msg: str = "Error"):
        self.msg=msg
    def output(self):
        logging.error("Telegram error:", self.msg)