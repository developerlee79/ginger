import json

from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

try:
    AI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
    AI_KEY = os.environ["AZURE_OPENAI_API_KEY"]
    deployment_name = "gpt-4.1-mini"
    api_version = '2024-12-01-preview'
except KeyError:
    print("Missing environment variable 'OPENAI_ENDPOINT' or 'OPENAI_KEY'")
    exit()


class AzureOpenAIParser:

    def convert_text_to_query(self, text_query):
        client = AzureOpenAI(
            api_key=AI_KEY,
            api_version=api_version,
            base_url=f"{AI_ENDPOINT}/openai/deployments/{deployment_name}"
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content":
                        """
                        너는 사용자가 입력한 검색어에서 데이터베이스 컬럼에 일치하는 의미 단위 맥락들을 추출하고, SQL 쿼리 형식으로 변환하는 자연어 분석 전문 AI야.
                        사용자는 전자 제품을 검색하는 이커머스 플랫폼에서 원하는 제품을 찾기 위해 자유롭게 검색어를 입력할 거야.  
                        검색어는 다음과 같은 두 가지 형태가 있어:

                        1. 단순 키워드 검색 (예: "Macbook Air M1", "삼성 냉장고")
                        2. 조건 기반 자연어 검색 (예: "전기 요금이 적게 드는 냉장고", "가성비 좋은 세탁기")
                        
                        너는 이 사용자 입력을 아래 테이블 구조에 기반하여 정확한 SQL 검색 쿼리의 조건 및 정렬 항목으로 바꿔야 해.
                        
                        ---
                        
                        테이블 구조는 다음과 같아:
                        
                        ```sql
                        CREATE TABLE ELECTRONIC_DEVICE(
                            id bigint primary key auto_increment,
                            category int not null comment '제품 카테고리(1: 노트북, 2: 냉장고, 3: 청소기, 4: TV, 5: 세탁기)',
                            manufacturer varchar(200) not null,
                            model_code varchar(100) not null,
                            serial_code varchar(250) null,
                            model_name varchar(250) null,
                            model_image_url varchar(255) null,
                            power_consumption int,
                            electricity_bill int,
                            price int not null
                        );
                        
                        너의 목표는, 검색어를 분석해 다음과 같은 SQL 질의 요소로 나누는 것이야:
                        
                        where: 제품 필터링 조건 (예: category=2, manufacturer='samsung')
                        sort: 정렬 기준 (예: electricity_bill asc, price desc)
                        처리 시 고려할 규칙은 다음과 같아:
                        
                        제품 유형 명칭은 category로 변환해야 해. (예: "노트북" → category=1)
                        "전기 요금이 적은", "전력 소비가 낮은" 등은 electricity_bill asc 혹은 power_consumption asc로 변환해야 해.
                        "가격이 저렴한" → price asc, "가격이 높은" → price desc
                        "추천", "보여줘" 같은 단어는 무시해도 좋아.
                        "Macbook Air" 같은 제품명이나 "Apple" 같은 브랜드명은 model_name 또는 manufacturer로 처리해.
                        가능한 정렬 기준은 다음과 같아: price, electricity_bill, power_consumption
                        반드시 아래 형식으로 JSON 응답만 출력해. 다른 텍스트는 포함하지 마:
                        
                        {"where": [...], "sort": [...]}
                        예시:
                        
                        입력: "전기요금이 적게 드는 냉장고를 보여줘"
                        출력: {"where": ["category=2"], "sort": ["electricity_bill asc"]}
                        
                        입력: "삼성에서 나온 TV 중 전력 소비가 낮은 거 보여줘"
                        출력: {"where": ["category=4", "manufacturer='samsung'"], "sort": ["power_consumption asc"]}
                        
                        입력: "가격이 저렴한 선풍기"
                        출력: {"where": ["category=3"], "sort": ["price asc"]}
                        
                        입력: "Macbook Air M1"
                        출력: {"where": ["model_name LIKE '%Macbook Air M1%'"], "sort": []}
                        """
                },
                {
                    "role": "user",
                    "content": text_query
                }
            ],
            max_tokens=3000
        )

        infer_result = response.choices[0].message.content
        return json.loads(infer_result)
