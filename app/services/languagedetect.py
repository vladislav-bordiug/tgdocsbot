from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

class DetectLanguageTool:

    def detect_language(self, text: str) -> str:
        if not text:
            return "unknown"

        return detect(text)