from typing import List, Protocol
import openai
from dataclasses import dataclass
from config import settings

@dataclass
class SummaryResult:
    summary: str
    keywords: List[str]
    keyword_explanations: dict[str, str]

class Summarizer(Protocol):
    def summarize(self, text: str) -> SummaryResult:
        ...

class GPTNewsSummarizer:
    def __init__(self, api_key: str = settings.OPENAI_API_KEY):
        self.client = openai.OpenAI(api_key=api_key)
    
    def summarize(self, text: str) -> SummaryResult:
        prompt = f"""
        다음 뉴스 기사를 요약해주세요:
        
        {text}
        
        다음 형식으로 응답해주세요:
        1. 200자 이내의 요약
        2. 중요한 키워드 5개
        3. 각 키워드에 대한 간단한 설명
        
        형식:
        요약: [요약문]
        키워드: [키워드1, 키워드2, ...]
        설명: 
        - 키워드1: [설명]
        - 키워드2: [설명]
        ...
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful news summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        
        # 응답 파싱
        lines = result.split('\n')
        summary = ""
        keywords = []
        explanations = {}
        
        current_section = ""
        for line in lines:
            if line.startswith("요약:"):
                summary = line.replace("요약:", "").strip()
            elif line.startswith("키워드:"):
                keywords = [k.strip() for k in line.replace("키워드:", "").strip("[]").split(",")]
            elif line.startswith("- "):
                key, explanation = line.replace("- ", "").split(":", 1)
                explanations[key.strip()] = explanation.strip()
        
        return SummaryResult(
            summary=summary,
            keywords=keywords,
            keyword_explanations=explanations
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
        print(f"- {keyword}: {result.keyword_explanations.get(keyword, '')}") 