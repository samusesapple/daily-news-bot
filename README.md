# 📰 Daily News Bot

매일 주요 뉴스를 자동으로 수집하고 요약하여 카카오톡으로 전송해주는 봇 서비스입니다.

## 🚀 주요 기능

- 네이버 뉴스 랭킹 크롤링
- GPT를 활용한 뉴스 요약
- 카카오톡 자동 발송
- 구독 기반 서비스

## 🛠 기술 스택

- Python 3.11+
- FastAPI
- OpenAI GPT API
- SQLAlchemy
- BeautifulSoup4
- 카카오톡 API

## ⚙️ 설치 방법

1. 저장소 클론

```bash
git clone https://github.com/your-username/daily-news-bot.git
cd daily-news-bot
```

2. 가상환경 설정

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
   `.env` 파일을 생성하고 다음 변수들을 설정:

```
OPENAI_API_KEY=your_openai_api_key
KAKAO_REST_API_KEY=your_kakao_rest_api_key
DATABASE_URL=sqlite:///./news_bot.db
```

## 🏃‍♂️ 실행 방법

```bash
# 서버 실행
uvicorn main:app --reload
```

## 📝 라이선스

MIT License
