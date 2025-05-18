from typing import List, Optional, Protocol
import aiohttp
from dataclasses import dataclass
from config import settings
from messenger.message_formatter import FormattedMessage

@dataclass
class KakaoMessage:
    template_id: str
    template_args: dict
    receiver_uuids: List[str]

class KakaoSender(Protocol):
    async def send_message(self, message: FormattedMessage, receiver_uuids: List[str]) -> bool:
        ...

class KakaoRestApiSender:
    """
    카카오 REST API(내게 메시지) 발송용
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://kapi.kakao.com/v2/api/talk/message/default/send"
    ):
        self.api_key = api_key or settings.KAKAO_REST_API_KEY
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    async def send_message(self, message: FormattedMessage, receiver_uuids: List[str]) -> bool:
        """
        카카오톡 메시지를 발송합니다.
        
        Args:
            message: 포맷팅된 메시지
            receiver_uuids: 수신자 UUID 목록
            
        Returns:
            bool: 발송 성공 여부
        """
        kakao_message = KakaoMessage(
            template_id=message.template_id,
            template_args={
                "title": message.title,
                "content": message.content
            },
            receiver_uuids=receiver_uuids
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    data={
                        "template_id": kakao_message.template_id,
                        "template_args": kakao_message.template_args,
                        "receiver_uuids": kakao_message.receiver_uuids
                    }
                ) as response:
                    return response.status == 200
        except Exception as e:
            print(f"REST API 메시지 발송 중 오류 발생: {e}")
            return False

class KakaoAlimtalkSender:
    """
    카카오 알림톡(비즈 인증) 발송용 - 실제 운영 시 사용
    (실제 엔드포인트/파라미터는 알림톡 가이드에 맞게 수정 필요)
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://alimtalk-api.kakao.com/send"):
        self.api_key = api_key or settings.KAKAO_REST_API_KEY
        self.base_url = base_url
        self.headers = {
            "Authorization": f"KakaoAK {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def send_message(self, message: FormattedMessage, receiver_uuids: List[str]) -> bool:
        # 실제 알림톡 파라미터 구조에 맞게 변환 필요
        payload = {
            "template_code": message.template_id,
            "receiver_uuids": receiver_uuids,
            "message": message.content
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                ) as response:
                    return response.status == 200
        except Exception as e:
            print(f"알림톡 발송 중 오류 발생: {e}")
            return False

class KakaoSelfMessageSender:
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
        import json
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

# 사용 예시
if __name__ == "__main__":
    import asyncio
    from messenger.message_formatter import MessageFormatter
    
    async def test_send():
        formatter = MessageFormatter()
        test_message = FormattedMessage(
            title="테스트 메시지",
            content="이것은 테스트 메시지입니다.",
            template_id="test_template"
        )
        # REST API 방식
        rest_sender = KakaoRestApiSender()
        success_rest = await rest_sender.send_message(
            message=test_message,
            receiver_uuids=[settings.MY_KAKAO_UUID]
        )
        print(f"REST API 발송 {'성공' if success_rest else '실패'}")
        # 알림톡 방식 (실제 운영 시)
        alimtalk_sender = KakaoAlimtalkSender()
        success_alim = await alimtalk_sender.send_message(
            message=test_message,
            receiver_uuids=["test-uuid-1"]
        )
        print(f"알림톡 발송 {'성공' if success_alim else '실패'}")
    
    asyncio.run(test_send()) 