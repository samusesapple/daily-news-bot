# 📦 Step 1: 뉴스 링크 크롤링
# - 네이버 YTN 인기기사 상위 3개 제목 + 링크 가져오기

from dataclasses import dataclass
from typing import List, Protocol
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

@dataclass
class NewsArticle:
    title: str
    link: str
    category: str = "일반"
    summary: str = ""
    keywords: List[str] = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

class NewsSource(Protocol):
    def fetch_articles(self, limit: int = 3) -> List[NewsArticle]:
        ...

class HTTPClient(Protocol):
    def get(self, url: str, headers: dict) -> requests.Response:
        ...

class RequestsHTTPClient:
    def get(self, url: str, headers: dict) -> requests.Response:
        return requests.get(url, headers=headers)

class NaverNewsCrawler:
    def __init__(
        self,
        http_client: HTTPClient,
        base_url: str = "https://media.naver.com/press/052/ranking",
        user_agent: str = "Mozilla/5.0"
    ):
        self.http_client = http_client
        self.base_url = base_url
        self.headers = {"User-Agent": user_agent}

    def fetch_articles(self, limit: int = 3, category: str = "popular") -> List[NewsArticle]:
        url = f"{self.base_url}?type={category}"
        response = self.http_client.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        articles = soup.select("ul.press_ranking_list li.as_thumb a")
        return [
            NewsArticle(
                title=article.get_text(strip=True),
                link=article['href'],
                category=category
            )
            for article in articles[:limit]
        ]

# 사용 예시
if __name__ == "__main__":
    http_client = RequestsHTTPClient()
    crawler = NaverNewsCrawler(http_client=http_client)
    
    articles = crawler.fetch_articles(limit=3)
    for article in articles:
        print(f"📰 {article.title}")
        print(f"🔗 {article.link}")
        print(f"📑 {article.category}")
        print("---")
