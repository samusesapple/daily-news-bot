from typing import List
from dataclasses import dataclass
from datetime import datetime
from crawler.naver_ranking_crawler import NewsArticle
from summaries.news_summarizer import SummaryResult

@dataclass
class FormattedMessage:
    title: str
    content: str
    template_id: str = "news_summary"  # 카카오톡 템플릿 ID

class MessageFormatter:
    def __init__(self, template_id: str = "news_summary"):
        self.template_id = template_id
    
    def format_news_message(
        self,
        articles: List[NewsArticle],
        summaries: List[SummaryResult]
    ) -> FormattedMessage:
        now = datetime.now().strftime("%Y년 %m월 %d일")
        
        title = f"📢 {now} 오늘의 주요 뉴스"
        content_parts = []
        
        for i, (article, summary) in enumerate(zip(articles, summaries), 1):
            content_parts.append(f"{i}. {article.title}")
            content_parts.append(f"👉 요약: {summary.summary}")
            content_parts.append(f"🔗 {article.link}")
            
            if summary.keywords:
                content_parts.append("\n📘 오늘의 단어:")
                for keyword in summary.keywords[:3]:  # 상위 3개 키워드만 표시
                    explanation = summary.keyword_explanations.get(keyword, "")
                    content_parts.append(f"- '{keyword}': {explanation}")
            
            content_parts.append("---")
        
        content = "\n".join(content_parts)
        
        return FormattedMessage(
            title=title,
            content=content,
            template_id=self.template_id
        )

# 사용 예시
if __name__ == "__main__":
    from crawler.naver_ranking_crawler import NewsArticle
    from summaries.news_summarizer import SummaryResult
    
    # 테스트 데이터
    test_articles = [
        NewsArticle(
            title="전세 사기 또 발생... 피해자 속출",
            link="https://n.news.naver.com/article/052/0002000000",
            category="사회"
        )
    ]
    
    test_summaries = [
        SummaryResult(
            summary="전세보증금 피해가 반복되고 있으며, 정부의 대책이 시급한 상황입니다.",
            keywords=["전세보증금", "피해", "대책"],
            keyword_explanations={
                "전세보증금": "전세 계약 시 임대인이 보관하는 금액",
                "피해": "전세보증금을 돌려받지 못하는 상황",
                "대책": "정부의 전세 피해 방지 정책"
            }
        )
    ]
    
    formatter = MessageFormatter()
    message = formatter.format_news_message(test_articles, test_summaries)
    
    print(f"제목: {message.title}")
    print("\n내용:")
    print(message.content) 