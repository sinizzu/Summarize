import deepl
from app.core.config import settings

DEEL_KEY = settings.DEEPL_AUTH_KEY
translator = deepl.Translator(DEEL_KEY)

def kotoenTranslate(text):
    print(text)
    transeText = translator.translate_text(text, source_lang="ko", target_lang="en-us")
    return transeText

def entokoTranslate(text):
    print(text)
    transeText = translator.translate_text(text, source_lang="en", target_lang="ko")
    return transeText