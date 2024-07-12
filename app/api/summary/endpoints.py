from fastapi import APIRouter, Depends, HTTPException, Body
from app.services import summary_service
from app.db.connect_db import get_weaviate_client
from weaviate.classes.query import Filter
import os
router = APIRouter()

@router.get("/summaryPaper")
async def summaryPaper():
    response = await summary_service.searchFulltext("testdata")
    texts = response['data'][0].get('texts', 'No content available')
    return summary_service.summaryPaper(texts)

