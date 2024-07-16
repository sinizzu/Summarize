from fastapi import APIRouter, HTTPException, Request
from app.services import transelate_service
from app.schemas.sentence import TextRequest

router = APIRouter()

@router.post("/transelateToKorean")
async def transelateText(request: TextRequest):
    try:
        json_body = request.text
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
    