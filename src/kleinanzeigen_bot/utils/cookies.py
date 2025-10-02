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