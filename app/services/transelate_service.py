import deepl
from app.core.config import settings
from app.services import weaviate_service

DEEL_KEY = settings.DEEPL_AUTH_KEY
translator = deepl.Translator(DEEL_KEY)

def kotoenTranslate(text):
    print(text)
    transeText = translator.translate_text(text, source_lang="ko", target_lang="en-us")
    return transeText.text

def entokoTranslate(text):
    transeText = translator.translate_text(text, source_lang="en", target_lang="ko")
    print("transeText: ", transeText)
    return transeText.text

def summaryTranslate(pdf_id):
    transResponde = weaviate_service.transelateSummarySearch(pdf_id)
    if transResponde.get("resultCode") == 200:
        return {"resultCode": 200, "data": transResponde.get("data")}
    else:
        summary = weaviate_service.summarySearch(pdf_id).get("data")
        response = entokoTranslate(summary)
        print("dnddddndnndn",response)
        return {"resultCode": 200, "data": response}
