# 📂 PDFast 서비스 소개

![파이널-프로젝트-001](https://github.com/user-attachments/assets/b6ceb105-2b41-4101-b510-ac062fe5c130)

![파이널-프로젝트-004](https://github.com/user-attachments/assets/4ec19ea5-4540-4606-8ef0-fc35691e852e)


<br/>
<br/>

## 🎥 시연 영상

|<img width="1000" src="https://github.com/user-attachments/assets/6d27a6c6-caf8-4071-974c-54c735fe1d0f">|
| :---: |
|PDF 문서를 통한 학습 보조 웹 플랫폼|

<br/>
<br/>

## ✅ 추진 배경


![파이널-프로젝트-005](https://github.com/user-attachments/assets/4c7d0043-7651-4d3c-b1f0-294b8818998d)


# 👥 팀원 소개

| <img width="250" alt="hj" src="https://github.com/user-attachments/assets/c0af7daa-f81b-4527-b62b-f9ee8d23e311"> | <img width="250" alt="yj" src="https://github.com/user-attachments/assets/bee1516f-d25d-46af-8cee-2771a4d9c917"> | <img width="250" alt="jh" src="https://github.com/user-attachments/assets/0c08e694-5ca3-446a-8af9-e7441b83553f"> |
| --- | --- | --- |
| 🐼[정현주](https://github.com/wjdguswn1203)🐼 | 🐱[송윤주](https://github.com/raminicano)🐱 | 🐶[신지현](https://github.com/sinzng)🐶 |


<br/>
<br/>
<br/>


# ⚒ 전체 아키텍처

![파이널-프로젝트-008](https://github.com/user-attachments/assets/da29e426-b752-4f92-98ef-833580c38298)

<br/>
<br/>

# 📝 기능 소개

 | <img width="250" alt="chat" src="https://github.com/user-attachments/assets/518dac3e-fd26-4bd8-9690-a14510af82ce"> | <img width="250" src="https://github.com/user-attachments/assets/2289d108-de30-4e09-9f9c-f970bc6a42b6"> | <img width="250" alt="keyword" src="https://github.com/user-attachments/assets/6fa0ef0a-e09b-45b3-92c0-0593e983d32e"> | 
| --- | --- | --- |
| 영어 요약 | 한국어 요약 | PDF 툴팁 요약 |


<br/>
<br/>

# 🏆 기술 스택
## Programming language

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<br/>

## Library & Framework

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<br/>

## API 

<img src="https://img.shields.io/badge/huggingface-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
<br/>

## Database

<img src="https://img.shields.io/badge/weaviate-6EBE49?style=for-the-badge"/>

<br/>


## Version Control System
<img alt="github" src="https://img.shields.io/badge/Github-000000?style=for-the-badge&logo=github&logoColor=white"> 
<br/>


## Communication Tool

<img alt="notion" src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white"> <img alt="kakao" src="https://img.shields.io/badge/KakaoTalk-FFCD00?style=for-the-badge&logo=kakao&logoColor=black"> 


<br/>
<br/>
<br/>


<br/>
<br/>
<br/>


# 설명
Summarize api (요약관련 API)

# 디렉토리 설명

```
SubFastAPI/
├── .github/
├── .venv/
├── app/
│   ├── api/
│   │   ├── summary/ 
│   │   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connect_db.py
│   ├── models/
│   │   ├── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── paper.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── summary_service.py
│   ├── main.py
│   ├── __init__.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
```

## app/api
- `summary` : 요약 기능 관련 API 엔드 포인트 정의
- `__init__.py`: API 디렉토리 패키지 초기화 파일

## api/core
- `config.py`: 애플리케이션 설정 및 환경 변수를 관리합니다.
- `__init__.py`: Core 디렉토리 패키지 초기화 파일입니다.

## app/db
- `connect_db.py`: Weaviate 데이터베이스와의 연결을 설정하고 관리하는 파일입니다.
- `__init__.py`: DB 디렉토리 패키지 초기화 파일입니다.

## app/models
- `__init__.py`: Models 디렉토리 패키지 초기화 파일입니다.

## app/schemas
- `paper.py`: Pydantic 스키마를 정의하여 데이터 유효성 검사를 수행합니다.
- `__init__.py`: Schemas 디렉토리 패키지 초기화 파일입니다.

## app/services
- `summary_service.py`: 요약 로직을 처리하는 서비스 레이어입니다.
- `__init__.py`: Services 디렉토리 패키지 초기화 파일입니다.


## app/main.py
FastAPI 애플리케이션을 초기화하고 라우터를 포함하는 메인 파일입니다.
