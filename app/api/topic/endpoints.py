from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.services import keyword_extract_service
from fastapi import APIRouter
import requests


router = APIRouter()


@router.get('/keywordExtract')
async def keyword_extraction(file: UploadFile = File(...)):
    try:
        pdfBytes = await file.read()
        ocrResponse = requests.post(
            "http://localhost:8000/ocr/ocrTest",
            files = {"file": (file.filename, pdfBytes, file.content_type)}
        )
        if ocrResponse.status_code != 200:
            raise HTTPException(status_code=400, detail="OCR failed")
        ocrResult = ocrResponse.json()
        text = ocrResult.get("data",{}).get("texts")
        
        if not text : 
            raise HTTPException(status_code=404, detail="No text extracted from the PDF")
        
        keywordsResult = keyword_extract_service.keyword_extraction(text)
        
        return JSONResponse(content=keywordsResult)
    except Exception as e:
        print(f"Error in /keywordExtraction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))