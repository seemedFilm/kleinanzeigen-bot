import os
import json
import asyncio

async def import_cookies(browser, cookie_file: str):
    """
    Importiert Cookies aus einer JSON-Datei und injiziert sie in den nodriver Browser.
    """
    if not os.path.exists(cookie_file):
        print(f"[WARN] Cookie-Datei {cookie_file} nicht gefunden – überspringe Import.")
        return

    with open(cookie_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    # Cookies können aus Chrome/Export anders aussehen → Mapping anpassen
    for cookie in cookies:
        try:
            await browser.set_cookie(                
                domain=cookie.get("domain", ".kleinanzeigen.de"),
                name=cookie["name"],
                value=cookie["value"],
                path=cookie.get("path", "/"),                
                expires=cookie.get("expiry"),  # Can be none
                sameSite=cookie.get("sameSite", "Lax"),
                secure=cookie.get("secure", True),
                httpOnly=cookie.get("httpOnly", False)
            )
            print(f"[INFO]set {cookie.get('name')}")
        except Exception as ex:
            print(f"[WARN] Couldn't set {cookie.get('name')} nicht setzen: {ex}")
