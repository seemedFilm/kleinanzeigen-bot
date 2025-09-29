import os
import json
import logging
from nodriver.cdp.network import CookieParam
import traceback

LOG = logging.getLogger(__name__)

async def import_cookies_into_page(browser, page):
    cookie_file = os.environ.get("KLEINBOT_COOKIE")
    if not cookie_file or not os.path.exists(cookie_file):
        LOG.info("Keine Cookie-Datei gesetzt oder Datei nicht gefunden, normaler Login wird verwendet.")
        return

    LOG.info("Lade Cookies aus: %s", cookie_file)
    try:
        with open(cookie_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)

        params = []
        for cookie in cookies:
            try:
                cj = {
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie.get("domain", ".kleinanzeigen.de"),
                    "path": cookie.get("path", "/"),
                }
                if "secure" in cookie:
                    cj["secure"] = bool(cookie["secure"])
                if "expires" in cookie:
                    try:
                        cj["expires"] = int(cookie["expires"])
                    except Exception:
                        pass

                params.append(CookieParam.from_json(cj))
            except Exception as e:
                LOG.warning("Cookie %s übersprungen: %s", cookie.get("name"), e)

        if params:
            await browser.cookies.set_all(cookies=params)
            LOG.info("Cookies erfolgreich importiert (%d Stück).", len(params))

        await page.reload()
    except Exception as e:
        LOG.error("Fehler beim Import der Cookies: %s", e)
        raise
    
# async def import_cookies_into_page(page):
#     cookie_file = os.environ.get("KLEINBOT_COOKIE")
#     if not cookie_file or not os.path.exists(cookie_file):
#         LOG.info("Keine Cookie-Datei gesetzt oder Datei nicht gefunden – normaler Login wird verwendet.")
#         return

#     LOG.info("Lade Cookies aus: %s", cookie_file)
#     try:
#         with open(cookie_file, "r", encoding="utf-8") as f:
#             cookies = json.load(f)

#         for cookie in cookies:
#             try:
#                 await page.set_cookie(cookie)
#             except Exception as e:
#                 LOG.warning("Cookie %s konnte nicht gesetzt werden: %s", cookie.get("name"), e)

#         await page.reload()
#         LOG.info("Cookies erfolgreich importiert.")
#     except Exception as e:
#         LOG.error("Fehler beim Import der Cookies: %s", e)
#         traceback.print_exc()
        
# async def import_cookies_into_page(page):
#     cookie_file = os.environ.get("KLEINBOT_COOKIE")
#     if not cookie_file or not os.path.exists(cookie_file):
#         LOG.error(f"Keine Cookie-Datei gesetzt oder Datei nicht gefunden - normaler Login wird verwendet.")
#         return
#     LOG.info(f"Lade Cookies aus: {cookie_file}")
#     try:
#         with open(cookie_file, "r", encoding="utf-8") as f:
#             cookies = json.load(f)

#         await page.wait_loaded()
#         for cookie in cookies:
#             try:
#                 await page.set_cookie(cookie)
#             except Exception as e:
#                 LOG.error(f"Cookie %s konnte nicht gesetzt werden: %s", cookie.get("name"), e)

#         await page.reload()
#         LOG.info(f"Cookies erfolgreich importiert.")
#     except Exception as e:
#         LOG.error(f"Fehler beim Import der Cookies: {e}")


# async def import_cookies(browser, cookie_file: str):
#     """
#     Importiert Cookies aus einer JSON-Datei und injiziert sie in den nodriver Browser.
#     """
#     if not os.path.exists(cookie_file):
#         print(f"[WARN] Cookie-Datei {cookie_file} nicht gefunden – überspringe Import.")
#         return

#     with open(cookie_file, "r", encoding="utf-8") as f:
#         cookies = json.load(f)

#     # Cookies können aus Chrome/Export anders aussehen → Mapping anpassen
#     for cookie in cookies:
#         try:
#             await browser.set_cookie(                
#                 domain=cookie.get("domain", ".kleinanzeigen.de"),
#                 name=cookie["name"],
#                 value=cookie["value"],
#                 path=cookie.get("path", "/"),                
#                 expires=cookie.get("expiry"),  # Can be none
#                 sameSite=cookie.get("sameSite", "Lax"),
#                 secure=cookie.get("secure", True),
#                 httpOnly=cookie.get("httpOnly", False)
#             )
#             print(f"[INFO]set {cookie.get('name')}")
#         except Exception as ex:
#             print(f"[WARN] Couldn't set {cookie.get('name')} nicht setzen: {ex}")
