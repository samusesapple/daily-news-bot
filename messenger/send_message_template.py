# 📦 Step 3: 카카오톡 자동 발송 (예시 개념)

# 실제 카카오톡 채널 또는 알림톡은 API 연동이 필요하며,
# 샘플 개념으로 메세지 형태만 구성

def create_message(title, link, summary):
    return f"📌 {title}\n{summary}\n🔗 {link}"

# 예시 출력
# print(create_message("기사 제목", "https://링크", "요약된 내용"))
