# 📦 보조 기능: 기사 본문 추출 (BeautifulSoup + 정규표현식 필요할 수 있음)

import requests
from bs4 import BeautifulSoup

def extract_article_text(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    # 본문 위치는 뉴스마다 다름 (네이버 뉴스는 id="dic_area"인 경우가 많음)
    article = soup.select_one("#dic_area")
    return article.get_text(strip=True) if article else "본문 추출 실패"
