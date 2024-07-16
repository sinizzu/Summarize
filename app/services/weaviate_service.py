
from app.db.connect_db import get_weaviate_client
from weaviate.classes.query import Filter

client = get_weaviate_client()
documentCollection = client.collections.get("pdf")

# weaviate full text 검색
def searchFulltext(pdf_link: str):
    try: 
        response = documentCollection.query.fetch_objects(
            filters=Filter.by_property("pdf_link").equal(pdf_link),
        )
        res = []
        # 오브젝트가 있으면
        if response.objects:
            for object in response.objects:
                res.append(object.properties) # 반환 데이터에 추가
            return {"resultCode" : 200, "data" : res}
        else:
            return {"resultCode" : 400, "data" : response}
    except Exception as e:
        return {"resultCode": 500, "data": str(e)}
