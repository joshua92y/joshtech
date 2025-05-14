from fastapi import FastAPI, Response

router = FastAPI()

BASE_URL = "https://api.joshuatech.dev"  # 🔁 baseURL에 맞게 수정


@router.get("/robots.txt")
def robots_txt():
    content = f"""
User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
""".strip()
    return Response(content=content, media_type="text/plain")


from fastapi import FastAPI, Response
from datetime import datetime
import os
from pathlib import Path
import json

app = FastAPI()

# 예: 환경변수로 baseURL 관리
BASE_URL = os.getenv("BASE_URL", "https://example.com")


# 유틸 함수: posts.json or markdown 데이터 불러오기
def get_posts(base_path: Path) -> list[dict]:
    # 예시: JSON 메타파일들이 있다고 가정
    posts = []
    for path in base_path.glob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            slug = path.stem
            posts.append(
                {
                    "url": f"{BASE_URL}/{base_path.parts[-2]}/{slug}",
                    "lastmod": data.get("publishedAt", datetime.today().isoformat()),
                }
            )
    return posts


@app.get("/sitemap.xml")
def sitemap():
    today = datetime.today().strftime("%Y-%m-%d")

    # 🔁 정적 라우트
    routes = [
        {"url": f"{BASE_URL}/", "lastmod": today},
        {"url": f"{BASE_URL}/about", "lastmod": today},
        {"url": f"{BASE_URL}/contact", "lastmod": today},
        # 필요에 따라 더 추가
    ]

    # 🔁 블로그와 프로젝트 경로
    blog_posts = get_posts(Path("src/app/blog/posts"))
    work_posts = get_posts(Path("src/app/work/projects"))

    all_urls = routes + blog_posts + work_posts

    # ✅ XML 구성
    xml_items = "\n".join(
        f"""
        <url>
            <loc>{item['url']}</loc>
            <lastmod>{item['lastmod']}</lastmod>
        </url>
        """.strip()
        for item in all_urls
    )

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset 
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>
""".strip()

    return Response(content=xml_content, media_type="application/xml")
