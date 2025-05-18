# src/app/routers/frontAPI.py
from fastapi import APIRouter, Response, BackgroundTasks, Request, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
from uuid import uuid4
from html2image import Html2Image
from pathlib import Path
import os, json

router = APIRouter()
BASE_URL = os.getenv("BASE_URL", "https://api.joshuatech.dev")
CDN_BASE = os.getenv("CDN_URL", "https://cdn.joshuatech.dev")

TMP_DIR = Path("/tmp")
STATIC_DIR = Path("static")
TMP_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"⚠️ 파일 삭제 실패: {path}, 이유: {e}")


@router.get("/robots.txt")
def robots_txt():
    return Response(
        content=f"""User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml""",
        media_type="text/plain",
    )


def get_posts(base_path: Path) -> list[dict]:
    if not base_path.exists():
        return []
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


@router.get("/sitemap.xml")
def sitemap():
    today = datetime.today().strftime("%Y-%m-%d")
    static_routes = [
        {"url": f"{BASE_URL}/", "lastmod": today},
        {"url": f"{BASE_URL}/about", "lastmod": today},
        {"url": f"{BASE_URL}/contact", "lastmod": today},
    ]
    blog_posts = get_posts(Path(__file__).parent / "../../blog/posts")
    work_posts = get_posts(Path(__file__).parent / "../../work/projects")
    all_urls = static_routes + blog_posts + work_posts

    xml = "\n".join(
        f"""<url><loc>{item['url']}</loc><lastmod>{item['lastmod']}</lastmod></url>"""
        for item in all_urls
    )
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml}
</urlset>
"""
    return Response(content=xml_content, media_type="application/xml")


@router.get("/og", summary="Open Graph 이미지 생성")
async def generate_og_image(
    request: Request, background_tasks: BackgroundTasks, title: str = "Portfolio"
):
    person = {
        "name": "Kaname Nenthuki",
        "role": "Full-stack Developer",
        "avatar": f"{CDN_BASE}/static/avatar.png",
    }

    html_content = f"""
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');
        body {{
          font-family: 'Inter', sans-serif;
          width: 1280px; height: 720px;
          background: #151515; color: white;
          padding: 8rem; display: flex;
        }}
        .container {{
          display: flex;
          flex-direction: column;
          justify-content: center;
          gap: 4rem;
        }}
        .title {{
          font-size: 8rem;
          line-height: 8rem;
          letter-spacing: -0.05em;
          white-space: pre-wrap;
          text-wrap: balance;
        }}
        .info {{
          display: flex;
          align-items: center;
          gap: 5rem;
        }}
        .avatar {{
          width: 12rem;
          height: 12rem;
          object-fit: cover;
          border-radius: 50%;
        }}
        .name {{
          font-size: 4.5rem;
          line-height: 4.5rem;
          white-space: pre-wrap;
          text-wrap: balance;
        }}
        .role {{
          font-size: 2.5rem;
          line-height: 2.5rem;
          opacity: 0.6;
          white-space: pre-wrap;
          text-wrap: balance;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="title">{title}</div>
        <div class="info">
          <img src="{person['avatar']}" class="avatar" alt="{person['name']}"/>
          <div>
            <div class="name">{person['name']}</div>
            <div class="role">{person['role']}</div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

    uid = uuid4().hex
    html_path = TMP_DIR / f"{uid}.html"
    image_path = TMP_DIR / f"{uid}.png"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    try:
        hti = Html2Image(output_path=str(TMP_DIR))
        hti.browser_path = "/usr/bin/chromium"  # ⚠️ 환경에 따라 경로 조정
        hti.screenshot(html_file=str(html_path), save_as=f"{uid}.png", size=(1280, 720))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 생성 실패: {str(e)}")

    # 파일 정리 예약
    background_tasks.add_task(cleanup_file, str(html_path))
    background_tasks.add_task(cleanup_file, str(image_path))

    return FileResponse(str(image_path), media_type="image/png")
