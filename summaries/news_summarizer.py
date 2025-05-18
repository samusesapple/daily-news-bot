from typing import List, Protocol
import openai
from dataclasses import dataclass
from config import settings

@dataclass
class KeywordDetail:
    explanation: str
    example: str

@dataclass
class SummaryResult:
    summary: str
    keywords: List[str]
    keyword_details: dict[str, KeywordDetail]

class Summarizer(Protocol):
    def summarize(self, text: str) -> SummaryResult:
        ...

class GPTNewsSummarizer:
    def __init__(self, api_key: str = settings.OPENAI_API_KEY):
        openai.api_key = api_key
    
    def summarize(self, text: str) -> SummaryResult:
        prompt = f"""
        다음 뉴스 기사를 요약해주세요:
        
        {text}
        
        다음 형식으로 응답해주세요:
        1. 200자 이내의 요약
        2. 중요한 키워드 5개
        3. 각 키워드에 대해 '설명'과 '예문'을 생성
        
        형식:
        요약: [요약문]
        키워드: [키워드1, 키워드2, ...]
        단어설명:
        - 키워드1: 설명: [설명] / 예문: [예문]
        - 키워드2: 설명: [설명] / 예문: [예문]
        ...
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful news summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=700
        )
        
        result = response.choices[0].message.content
        
        # 응답 파싱
        lines = result.split('\n')
        summary = ""
        keywords = []
        keyword_details = {}
        
        for line in lines:
            if line.startswith("요약:"):
                summary = line.replace("요약:", "").strip()
            elif line.startswith("키워드:"):
                keywords = [k.strip() for k in line.replace("키워드:", "").strip("[]").split(",")]
            elif line.startswith("- "):
                # - 키워드: 설명: ... / 예문: ...
                try:
                    key, rest = line[2:].split(": 설명:", 1)
                    explanation, example = rest.split("/ 예문:")
                    keyword_details[key.strip()] = KeywordDetail(
                        explanation=explanation.strip(),
                        example=example.strip()
                    )
                except Exception:
                    continue
        
        return SummaryResult(
            summary=summary,
            keywords=keywords,
            keyword_details=keyword_details
        )

# 사용 예시
if __name__ == "__main__":
    summarizer = GPTNewsSummarizer()
    test_text = """
    [서울=뉴시스] 정부가 내년부터 전세사기 피해자 지원을 위한 '전세사기 피해자 지원 특별법'을 시행한다.
    이 법안은 전세보증금을 반환받지 못한 피해자들에게 최대 5000만원까지 지원금을 지급하는 내용을 담고 있다.
    """
    
    result = summarizer.summarize(test_text)
    print(f"요약: {result.summary}")
    print("\n키워드:")
    for keyword in result.keywords:
        detail = result.keyword_details.get(keyword)
        if detail:
            print(f"- {keyword}: {detail.explanation} 예) {detail.example}") 