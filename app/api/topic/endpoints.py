from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.services import keyword_extract_service, summary_service

router = APIRouter()

@router.get('/keywordExtract')
async def keyword_extraction(title: str):
    try:
        response = summary_service.searchFulltext("testdata")
        texts = response['data'][0].get('texts', 'No content available')
        keywordsResult = keyword_extract_service.keyword_extraction(texts)

        # Extract the keys from the 'data' dictionary
        keywords = list(keywordsResult['data'].keys())

        return JSONResponse(content={"result_Code": 200, "data": keywords})
    except Exception as e:
        print(f"Error in /keywordExtraction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
