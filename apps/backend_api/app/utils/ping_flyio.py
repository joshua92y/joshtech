import httpx


async def ping_render():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get("https://mainapi.joshuatech.dev/healthz")
            print(f"[Fly → Render] {res.status_code}")
    except Exception as e:
        print(f"[Fly → Render ERROR] {e}")
