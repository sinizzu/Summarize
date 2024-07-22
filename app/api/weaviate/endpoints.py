from fastapi import APIRouter, HTTPException
from app.services import summary_service, weaviate_service
from app.schemas.sentence import TextRequest

router = APIRouter()

@router.get("/searchFulltext")
async def searchFulltext(pdf_id: str):
    response = weaviate_service.searchFulltext(pdf_id)
    texts = response['data'][0].get('full_text', 'No content available')

    return {"full_text": texts}

@router.get("/searchAll")
async def searchAll(collection_name: str):
    response = weaviate_service.searchAll(collection_name)
    data = response['data']
    
    return {"data": data}

@router.get("/searchPaperId")
async def searchPaperId(pdf_url: str):
    response = weaviate_service.searchPaperId(pdf_url)
    data = response['data']
    
    return {"data": data}

@router.get("/searchSummary")
async def summarySearch(pdf_id: str):
    response = weaviate_service.summarySearch(pdf_id)
    data = response['data']
    
    if data:
        return {"resultCode" : 200, "data" : data}
    else:
        return {"resultCode" : 400, "data" : data}
    
@router.get("/searchKeywords")
async def keywordSearch(pdf_id: str):
    response = weaviate_service.keywordSearch(pdf_id)
    data = response['data']
    
    if response['resultCode'] == 200:
        return {"resultCode" : 200, "data" : data}
    else:
        return {"resultCode" : 400, "data" : data}
    
@router.get("/searchTranslateSummary")
async def translateSummary(pdf_id: str):
    try:
        return weaviate_service.transelateSummarySearch(pdf_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
