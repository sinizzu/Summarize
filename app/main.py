from fastapi import FastAPI
from app.api import summary_endpoints, topic_endpoints, translate_endpoints, weaviate_endpoints
from app.api import summary_endpoints, topic_endpoints, weaviate_endpoints
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
import os

MainFastAPI = os.getenv("MainFastAPI")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8500", MainFastAPI],  # 모든 도메인에서 오는 요청을 허용합니다. 실제로는 필요한 도메인만 허용하도록 변경해야 합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(summary_endpoints.router, prefix="/api/summary", tags=["summary"])
app.include_router(topic_endpoints.router, prefix="/api/topic", tags=["topic"])
app.include_router(translate_endpoints.router, prefix="/api/translate", tags=["translate"])
app.include_router(weaviate_endpoints.router, prefix="/api/weaviate", tags=["weaviate"])
app.include_router(weaviate_endpoints.router, prefix="/api/weaviate", tags=["weaviate"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3500, reaload=True)
