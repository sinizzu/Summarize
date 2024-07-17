from fastapi import APIRouter, HTTPException
from app.services import summary_service, weaviate_service
from app.schemas.sentence import TextRequest

router = APIRouter()

@router.get("/summaryPaper")
async def summaryPaper(pdf_id: str):
    response = weaviate_service.searchFulltext(pdf_id)
    texts = response['data'][0].get('full_text', 'No content available')
    full = summary_service.textProcessing(texts)
    if full['resultCode'] == 200 and 'data' in full:
        start_combined_text = ' '.join([full['data'].get('abstract', ''), 
                                    full['data'].get('introduction', '')])
        end_combined_text = full['data'].get('conclusion', '')
    combined_text = { "resultCode": 200, "data": [start_combined_text, end_combined_text] }
    summary = await summary_service.summarize("testdata", combined_text)
    data = summary['data']
    data = ". ".join(data)
    print(data)
    last_sum = summary_service.extract_key_sentences(data)

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