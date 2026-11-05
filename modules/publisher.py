"""
멀티 플랫폼 블로그 포스팅 발행 모듈 (티스토리 Open API 및 네이버 연동)
"""
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any, Optional, List
from modules.logger import setup_logger

logger = setup_logger("publisher")

def publish_to_tistory(
    access_token: str,
    blog_name: str,
    title: str,
    content: str,
    visibility: int = 3, # 0: 비공개, 1: 보호, 3: 공개발행
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    티스토리 공식 Open API 글쓰기 실행
    엔드포인트: https://www.tistory.com/apis/post/write
    """
    if not access_token or not access_token.strip():
        return {"success": False, "message": "티스토리 Access Token을 입력해 주세요."}
    if not blog_name or not blog_name.strip():
        return {"success": False, "message": "티스토리 블로그 이름(서브도메인)을 입력해 주세요."}

    url = "https://www.tistory.com/apis/post/write"
    tag_str = ",".join(tags) if tags else ""
    
    data = {
        "access_token": access_token.strip(),
        "output": "json",
        "blogName": blog_name.strip(),
        "title": title,
        "content": content,
        "visibility": visibility,
        "tag": tag_str
    }

    try:
        logger.info(f"[티스토리] 포스팅 요청 시작 - 블로그: {blog_name}, 제목: {title}")
        response = requests.post(url, data=data, timeout=15)
        
        # HTTP 응답 검증
        if response.status_code != 200:
            logger.error(f"[티스토리] HTTP 에러 ({response.status_code}): {response.text}")
            return {
                "success": False,
                "message": f"티스토리 서버 응답 오류 (HTTP {response.status_code}): {response.text}"
            }

        res_json = response.json()
        tistory_obj = res_json.get("tistory", {})
        
        # 티스토리 API 상태코드 검증 (200: 성공)
        status = tistory_obj.get("status")
        if status == "200":
            post_url = tistory_obj.get("url", f"https://{blog_name}.tistory.com")
            post_id = tistory_obj.get("postId", "")
            logger.info(f"[티스토리] 발행 성공! 포스트ID: {post_id}, URL: {post_url}")
            return {
                "success": True,
                "platform": "Tistory",
                "message": "티스토리에 성공적으로 포스팅이 발행되었습니다!",
                "post_url": post_url,
                "post_id": post_id
            }
        else:
            err_msg = tistory_obj.get("error_message", "알 수 없는 오류")
            logger.warning(f"[티스토리] API 거부: {err_msg}")
            return {
                "success": False,
                "message": f"티스토리 API 오류: {err_msg}"
            }

    except requests.exceptions.Timeout:
        logger.error("[티스토리] 요청 타임아웃 발생")
        return {"success": False, "message": "티스토리 API 서버 연결 시간이 초과되었습니다."}
    except Exception as e:
        logger.error(f"[티스토리] 예외 발생: {str(e)}", exc_info=True)
        return {"success": False, "message": f"시스템 예외: {str(e)}"}

def publish_to_naver_email(
    naver_id: str,
    naver_password: str,
    title: str,
    content_html: str,
    blog_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    네이버 블로그의 공식 '이메일로 글쓰기' 기능을 활용한 안정적 자동 포스팅
    - 네이버 블로그 관리자에서 '글쓰기 설정 -> 이메일 글쓰기 설정'을 켜두면, 
      네이버 계정의 SMTP를 통해 안전하게 포스팅이 자동 등록됩니다 (캡차/차단 없음).
    """
    clean_id = naver_id.strip().split("@")[0] # 아이디만 추출
    target_blog_id = blog_id.strip() if blog_id else clean_id
    
    if not clean_id or not naver_password:
        return {"success": False, "message": "네이버 아이디 또는 비밀번호(애플리케이션 비밀번호)를 입력해 주세요."}

    sender_email = f"{clean_id}@naver.com"
    # 네이버 블로그 이메일 포스팅 수신 주소
    recipient_email = f"{target_blog_id}@blog.naver.com"

    try:
        logger.info(f"[네이버 이메일 포스팅] 전송 준비 - 발신: {sender_email} -> 수신: {recipient_email}")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = title
        msg["From"] = sender_email
        msg["To"] = recipient_email

        html_part = MIMEText(content_html, "html", "utf-8")
        msg.attach(html_part)

        # 네이버 SMTP 서버 접속 (포트 587 TLS 또는 465 SSL)
        with smtplib.SMTP_SSL("smtp.naver.com", 465, timeout=15) as server:
            server.login(clean_id, naver_password.strip())
            server.sendmail(sender_email, [recipient_email], msg.as_string())

        logger.info("[네이버] 이메일 기반 포스팅 발행 완료!")
        return {
            "success": True,
            "platform": "Naver",
            "message": "네이버 블로그에 포스팅이 성공적으로 전송/발행되었습니다!",
            "post_url": f"https://blog.naver.com/{target_blog_id}"
        }

    except smtplib.SMTPAuthenticationError:
        logger.error("[네이버] SMTP 인증 실패")
        return {
            "success": False,
            "message": "네이버 로그인 인증에 실패했습니다. (2단계 인증 계정인 경우 '애플리케이션 비밀번호' 또는 블로그 글쓰기 허용 여부를 확인하세요)"
        }
    except Exception as e:
        logger.error(f"[네이버] 포스팅 실패: {str(e)}", exc_info=True)
        return {"success": False, "message": f"네이버 포스팅 중 오류: {str(e)}"}
