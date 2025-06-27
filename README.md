# 개요

진저(**진**짜 최**저**가)는 기존 전자 제품 시장의 최저가 제품의 전력낭비 문제 해결을 위해 전자 제품의 생애 전 주기를 포함한 최저가를 제시하여 저전력 소비로의 전환을 실현하기 위한 플랫폼입니다.

# 설계

## 주요 기능

- 전자 제품의 이용 비용 계산
  - 전력 소모량, 이용 시간 데이터를 기반으로 전기세, 탄소 발자국 등 이용 비용 계산
- 라벨 기반 전자 제품 분류
  - 전자 제품의 라벨 이미지를 Vision AI로 분석하여 제품 코드 등 특징 정보, 업체명 등 Metadata 추출
  - RAG를 이용하여 전자 제품 분류 및 정보 제공
- 자연어 기반 추천 질의 처리
  - 문장형 질문(예. 전력 효율이 좋은 노트북을 추천해줘)을 LLM을 이용하여 문장형 질의를 각 의미별로 분리
  - 분리한 각 의미를 데이터베이스 쿼리로 사용하여 근접한 데이터 추출

## 시스템 아키텍쳐

- BackEnd : Python, FastAPI
- FrontEnd : Jinja, Html, CSS, Javascript
- Database : Azure Database for MySQL, Azure Blob Storage
- AI/Reasoning : Azure OpenAI
- Deploy/Build : Docker

# 실행 방법

본 프로젝트는 MS Azure을 이용한 클라우드 컴퓨팅 기능을 활용하여 빌드하였습니다. 

```dotenv
AZURE_CONNECTION_STRING=
AZURE_CONTAINER_NAME=
AZURE_CONTAINER_ACCOUNT_KEY=

AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=

AZURE_DATABASE_USER=
AZURE_DATABASE_PASSWORD=
AZURE_DATABASE_HOST=
AZURE_DATABASE_PORT=
AZURE_DATABASE_DATABASE=
```

Azure 서비스와의 연동을 위하여 본 프로젝트의 실행 전에 프로젝트의 root 디렉토리에 위 예시와 같은 .env 파일 추가가 선결되어야 합니다.

```commandline
docker build -t shoeragon .

docker run -d -p 8000:8000 shoeragon
```

이후, Docker를 사용하여 애플리케이션을 빌드 및 실행합니다. 실행된 애플리케이션은 [localhost:8000](http://localhost:8000)에서 동작합니다.
