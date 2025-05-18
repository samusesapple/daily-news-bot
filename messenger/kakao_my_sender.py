import aiohttp
import json
from messenger.message_formatter import FormattedMessage

class KakaoMySender:
    """
    카카오톡 나에게 보내기 API 전용 (사업자/채널 없이 본인 계정에만 메시지 전송)
    """
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    async def send_to_me(self, message: FormattedMessage) -> bool:
        data = {
            "template_object": json.dumps({
                "object_type": "text",
                "text": message.content,
                "link": {"web_url": "https://developers.kakao.com"}
            })
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    data=data
                ) as response:
                    if response.status != 200:
                        print("카카오 나에게 보내기 응답:", response.status, await response.text())
                    return response.status == 200
        except Exception as e:
            print(f"나에게 보내기 발송 중 오류 발생: {e}")
            return False 