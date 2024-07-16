from fastapi import APIRouter, HTTPException
from app.services import summary_service, weaviate_service
from app.schemas.sentence import TextRequest

router = APIRouter()

@router.get("/searchFulltext")
async def searchFulltext(pdf_link: str):
    response = weaviate_service.searchFulltext(pdf_link)
    texts = response['data'][0].get('full_text', 'No content available')

    return {"full_text": texts}

@router.get("/searchAll")
async def searchAll(collection_name: str):
    response = weaviate_service.searchAll(collection_name)
    data = response['data']
    
    return {"data": data}