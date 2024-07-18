from fastapi import APIRouter, HTTPException, Request
from app.services import transelate_service, weaviate_service
from app.schemas.sentence import TextRequest

router = APIRouter()

@router.post("/transelateToKorean")
async def transelateText(request: TextRequest):
    try:
        json_body = request.text
        print(json_body)
        data = transelate_service.entokoTranslate(json_body)
        return {"resultCode": 200, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transelateToEnglish")
async def transelateText(request: TextRequest):
    try:
        json_body = request.text
        data = transelate_service.kotoenTranslate(json_body)
        return {"resultCode": 200, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transelateSummary")
async def transelateSummary(pdf_id: str):
    try:
        res = transelate_service.summaryTranslate(pdf_id)
        text = res.get("data")
        if res.get("resultCode") == 200:
            save = weaviate_service.transSave(pdf_id, text)
            print(save)
            return {"resultCode": 200, "data": text}
        else:
            print("summaryTranslate error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    


