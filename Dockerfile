# 베이스 이미지로 Python 사용
FROM python:3.9.7

# step 2 : Package Install
RUN apt-get update && apt-get -y upgrade && apt-get -y install git net-tools vim

# 작업 디렉토리 설정
WORKDIR /root

# 의존성 설치
COPY ./SubFastAPI.tar.gz /root
RUN mkdir /root/SubFastAPI
WORKDIR /root/SubFastAPI
RUN tar xvzf SubFastAPI.tar.gz && rm SubFastAPI.tar.gz

# 가상 환경 생성 및 패키지 설치
RUN python3.9 -m venv .venv
RUN . .venv/bin/activate
RUN pip install -r requirements.txt

# 애플리케이션이 실행될 포트 설정
EXPOSE 3500

# 애플리케이션 시작 명령어
CMD ["./run.sh"]