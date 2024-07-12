from fastapi import APIRouter, Depends, HTTPException, Body
from app.services import summary_service
from app.db.connect_db import get_weaviate_client
from weaviate.classes.query import Filter
import os
router = APIRouter()

@router.get("/summaryPaper")
async def summaryPaper():
    response = summary_service.searchFulltext("testdata")
    texts = response['data'][0].get('texts', 'No content available')
    full = summary_service.textProcessing(texts)
    if full['resultCode'] == 200 and 'data' in full:
        start_combined_text = ' '.join([full['data'].get('abstract', ''), 
                                    full['data'].get('introduction', '')])
        end_combined_text = full['data'].get('conclusion', '')
    combined_text = { "resultCode": 200, "data": [start_combined_text, end_combined_text] }
    summary = summary_service.summarize("testdata", combined_text)

    return {"summary": summary}
