from fastapi import APIRouter, HTTPException
from app.services import summary_service, weaviate_service
from app.schemas.sentence import TextRequest, LanguageRequest

router = APIRouter()

@router.get("/summaryPaper")
async def summaryPaper(pdf_id: str):
    getSummary = await weaviate_service.summarySearch(pdf_id)
    res = getSummary.get("resultCode")
    if res == 200:
        res = getSummary.get("data", "")
        print("summaries: ", res)
        return {"summary": res}
    else:
        response = await weaviate_service.searchFulltext(pdf_id)
        # print("response: ", response)
        texts = response['data'][0].get('full_text', 'No content available')
        # print("texts: ", texts)
        full = await summary_service.textProcessing(texts)
        start_combined_text = ''
        end_combined_text= ''
        if full['resultCode'] == 200 and 'data' in full:
            print("data: ", full['data'])
            start_combined_text = ' '.join([full['data'].get('abstract', ''), 
                                        full['data'].get('introduction', '')])
            end_combined_text = full['data'].get('conclusion', '')
        
        combined_text = { "resultCode": 200, "data": [start_combined_text, end_combined_text] }
        summary = await summary_service.summarizePaper(combined_text)
        data = summary['data']
        data = ". ".join(data)
        last_sum = await summary_service.extract_key_sentences(data)
        save_result = await weaviate_service.summarySave(pdf_id, last_sum)
        print("save_result: ", save_result)
        return {"summary": last_sum}

@router.get("/summaryPdf")
async def summaryPdf(pdf_id: str):
    getSummary = await weaviate_service.summarySearch(pdf_id)
    res = getSummary.get("resultCode")
    if res == 200:
        res = getSummary.get("data", "")
        print("summaries: ", res)
        return {"summary": res}
    else:
        response = await weaviate_service.searchFulltext(pdf_id)
        texts = response['data'][0].get('full_text', 'No content available')
        lang = response['data'][0].get('language', 'No content available')
        summary = await summary_service.summarizePdf(texts, lang)
        data = summary['data']
        data = ". ".join(data)
        last_sum = await summary_service.summarizePdf(data, lang)
        print("last_sum: ", last_sum)
        last_sum = last_sum['data'][0]
        save_result = await weaviate_service.summarySave(pdf_id, last_sum)
        return {"summary": last_sum}

# 넣을 때, \n을 삭제해줘야함.
@router.post("/summaryScroll")
async def summaryScroll(request: LanguageRequest):
    try:
        text = request.text
        lang = request.lang
        data = await summary_service.summarize_texts(text, lang)
        return {"resultCode": 200, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/summarySave")
async def summarySave(pdf_id: str, summary: str):
    response = await weaviate_service.summarySave(pdf_id, summary)
    return response

# 넣을 때, \n을 삭제해줘야함.
@router.post("/summaryKo")
async def summaryKor(request: TextRequest):
    try:
        json_body = request.text
        data = await summary_service.summarizeTextsKo(json_body)
        return {"resultCode": 200, "data": data}
    except Exception as e:
        raise await HTTPException(status_code=500, detail=str(e))