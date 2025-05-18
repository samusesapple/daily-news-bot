import asyncio
from crawler.naver_ranking_crawler import NaverNewsCrawler, RequestsHTTPClient
from utils.article_extractor import extract_article_text
from summaries.dummy_summarizer import DummySummarizer
from messenger.message_formatter import MessageFormatter
from messenger.kakao_my_sender import KakaoMySender
from config import settings
import os


def test_kakao_self_message_flow():
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

        # 5. 카카오톡 나에게 보내기 (비동기)
        async def send():
            access_token = os.getenv("MY_KAKAO_ACCESS_TOKEN")
            if not access_token:
                print("MY_KAKAO_ACCESS_TOKEN 환경변수가 필요합니다. uuid_getter.py로 발급 후 .env에 추가하세요.")
                return
            sender = KakaoMySender(access_token)
            success = await sender.send_to_me(message)
            print("[카카오톡 나에게 보내기 결과]", "성공" if success else "실패")
        asyncio.run(send())

if __name__ == "__main__":
    test_kakao_self_message_flow() 