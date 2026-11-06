import sys
from modules.persistent_bot import publish_naver_direct, publish_tistory_direct
from config import Config
from modules.generator import generate_blog_content
from modules.topic_manager import peek_current_topic

topic_info = peek_current_topic()
print(f"Current Topic: [{topic_info['topic_type']}] {topic_info['keyword']}")

blog_data = generate_blog_content(
    keyword=topic_info["keyword"],
    category=topic_info["category"],
    topic_type=topic_info["topic_type"]
)

print(f"Generated Title: {blog_data['title']}")
print(f"Generated Content Length: {len(blog_data['content'])} chars")
print(f"Naver ID: {Config.NAVER_ID}, Naver PW Exists: {bool(Config.NAVER_PW)}")
print(f"Kakao ID: {Config.KAKAO_ID}, Kakao PW Exists: {bool(Config.KAKAO_PW)}")

