from dataclasses import dataclass
from typing import Optional
import os
import sys
from functools import partial
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, request
from werkzeug.serving import make_server

@dataclass
class KakaoOAuthConfig:
    rest_api_key: str
    redirect_uri: str
    token_url: str = "https://kauth.kakao.com/oauth/token"
    user_info_url: str = "https://kapi.kakao.com/v2/user/me"

class KakaoOAuthService:
    def __init__(self, config: KakaoOAuthConfig, http_client: requests.Session):
        self.config = config
        self.http_client = http_client

    def get_auth_url(self) -> str:
        params = {
            "client_id": self.config.rest_api_key,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code"
        }
        return f"https://kauth.kakao.com/oauth/authorize?{urlencode(params)}"

    def get_access_token(self, code: str) -> str:
        data = {
            "grant_type": "authorization_code",
            "client_id": self.config.rest_api_key,
            "redirect_uri": self.config.redirect_uri,
            "code": code
        }
        response = self.http_client.post(self.config.token_url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_user_id(self, access_token: str) -> str:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.http_client.get(self.config.user_info_url, headers=headers)
        response.raise_for_status()
        return str(response.json()["id"])

def create_app(oauth_service: KakaoOAuthService) -> Flask:
    app = Flask(__name__)
    server: Optional[make_server] = None

    @app.route("/oauth")
    def oauth_callback():
        nonlocal server
        code = request.args.get("code")
        if not code:
            return "Authorization code not found", 400

        try:
            access_token = oauth_service.get_access_token(code)
            user_id = oauth_service.get_user_id(access_token)
            print(f"\n카카오 UUID: {user_id}")
            print(f"카카오 Access Token: {access_token}")
            print("서버를 종료합니다...")
            
            if server:
                server.shutdown()
            return "UUID와 Access Token을 성공적으로 가져왔습니다. 콘솔을 확인해주세요."
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return f"Error: {str(e)}", 500

    return app

def main():
    load_dotenv()
    
    config = KakaoOAuthConfig(
        rest_api_key=os.getenv("KAKAO_REST_API_KEY"),
        redirect_uri=os.getenv("KAKAO_REDIRECT_URI")
    )
    
    if not config.rest_api_key or not config.redirect_uri:
        print("Error: KAKAO_REST_API_KEY와 KAKAO_REDIRECT_URI 환경 변수가 필요합니다.")
        sys.exit(1)

    http_client = requests.Session()
    oauth_service = KakaoOAuthService(config, http_client)
    app = create_app(oauth_service)

    auth_url = oauth_service.get_auth_url()
    print(f"\n카카오 로그인 URL: {auth_url}")
    print("브라우저에서 위 URL을 열고 로그인해주세요.")

    from werkzeug.serving import make_server
    server = make_server("localhost", 5000, app)
    server.serve_forever()

if __name__ == "__main__":
    main() 