from typing import List, Optional
import aiohttp
from dataclasses import dataclass
from config import settings
from messenger.message_formatter import FormattedMessage

@dataclass
class KakaoMessage:
    template_id: str
    template_args: dict
    receiver_uuids: List[str]

class KakaoMessageSender:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://kapi.kakao.com/v2/api/talk/message/default/send"
    ):
        self.api_key = api_key or settings.KAKAO_API_KEY
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
            print(f"메시지 발송 중 오류 발생: {e}")
            return False

# 사용 예시
if __name__ == "__main__":
    import asyncio
    from messenger.message_formatter import MessageFormatter
    
    async def test_send():
        # 테스트 메시지 생성
        formatter = MessageFormatter()
        test_message = FormattedMessage(
            title="테스트 메시지",
            content="이것은 테스트 메시지입니다.",
            template_id="test_template"
        )
        
        # 발송자 생성
        sender = KakaoMessageSender()
        
        # 메시지 발송 (실제 UUID 필요)
        success = await sender.send_message(
            message=test_message,
            receiver_uuids=["test-uuid-1", "test-uuid-2"]
        )
        
        print(f"메시지 발송 {'성공' if success else '실패'}")
    
    # 테스트 실행
    asyncio.run(test_send()) 