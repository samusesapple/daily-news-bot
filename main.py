from crawler.naver_ranking_crawler import NaverNewsCrawler, RequestsHTTPClient
from utils.article_extractor import extract_article_text
# from summaries.news_summarizer import GPTNewsSummarizer
from summaries.dummy_summarizer import DummySummarizer
from messenger.message_formatter import MessageFormatter
from messenger.kakao_sender import KakaoRestApiSender
import asyncio
import openai
from config import settings
from typing import Optional

# 통합 테스트: 뉴스 크롤링 → 본문 추출 → 요약/단어설명+예문 → 메시지 포맷 → 카카오톡 발송

def main():
    # 1. 뉴스 크롤링 (테스트는 1개만)
    crawler = NaverNewsCrawler(RequestsHTTPClient())
    articles = crawler.fetch_articles(limit=1)
    if not articles:
        print("크롤링 결과가 없습니다.")
        return

    for article in articles:
        print(f"[크롤링] {article.title} ({article.link})")
        # 2. 기사 본문 추출
        article_text = extract_article_text(article.link)
        print(f"[본문 일부] {article_text[:100]}...")

        # 3. 요약 및 단어 설명/예문 생성
        summarizer = DummySummarizer()
        summary_result = summarizer.summarize(article_text)

        # 4. 메시지 포맷팅
        formatter = MessageFormatter()
        message = formatter.format_news_message([article], [summary_result])
        print("[카카오톡 메시지 미리보기]\n", message.content)

        # 5. 카카오톡 발송 (비동기)
        async def send():
            sender = KakaoRestApiSender()
            success = await sender.send_message(message, receiver_uuids=[settings.MY_KAKAO_UUID])
            print("[카카오톡 발송 결과]", "성공" if success else "실패")
        asyncio.run(send())

if __name__ == "__main__":
    main() 