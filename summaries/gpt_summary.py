# 📦 Step 2: 기사 본문 요약 (GPT API 사용 예시)

import openai

openai.api_key = "your-api-key"

def summarize_article(text):
    prompt = f"다음 기사를 3문장으로 요약해줘:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 예시 사용
# summary = summarize_article("여기에 기사 본문 텍스트 입력")
