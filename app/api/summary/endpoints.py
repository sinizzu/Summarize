from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException
from app.services import summary_service, weaviate_service
from app.schemas.sentence import TextRequest

router = APIRouter()

@router.get("/summaryPaper")
async def summaryPaper(pdf_id: str):
    get_summary = weaviate_service.searchPaperSummary(pdf_id)
    res = get_summary.get("resultCode")
    if res == 200:
        res = get_summary.get("data", "")
        print("summaries: ", res)
        return {"summary": res}
    else:
        response = weaviate_service.searchFulltext(pdf_id)
        texts = response['data'][0].get('full_text', 'No content available')
        full = summary_service.textProcessing(texts)
        if full['resultCode'] == 200 and 'data' in full:
            start_combined_text = ' '.join([full['data'].get('abstract', ''), 
                                        full['data'].get('introduction', '')])
            end_combined_text = full['data'].get('conclusion', '')
        combined_text = { "resultCode": 200, "data": [start_combined_text, end_combined_text] }
        summary = await summary_service.summarize(pdf_id, combined_text)
        data = summary['data']
        data = ". ".join(data)
        last_sum = summary_service.extract_key_sentences(data)
        save_result = weaviate_service.summarySave(pdf_id, last_sum)
        print("save_result: ", save_result)
        return {"summary": last_sum}

# 넣을 때, \n을 삭제해줘야함.
@router.post("/summaryScroll")
async def summaryScroll(request: TextRequest):
    try:
        json_body = request.text
        data = summary_service.summarize_texts(json_body)
        return {"resultCode": 200, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/summarySave")
async def summarySave(pdf_id: str, summary: str):
    response = weaviate_service.summarySave(pdf_id, summary)
    return response