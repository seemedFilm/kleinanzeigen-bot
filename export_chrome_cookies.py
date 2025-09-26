import os
import shutil
import sqlite3
import json
import base64
import win32crypt
from Crypto.Cipher import AES

def get_chrome_cookie_db(profile="Default", browser="chrome"):
    """
    Ermittelt den Cookie-Pfad fÃ¼r Chrome oder Edge
    """
    if browser == "chrome":
        base = os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data", profile)
    elif browser == "edge":
        base = os.path.join(os.environ['LOCALAPPDATA'], r"Microsoft\Edge\User Data", profile)
    else:
        raise ValueError("Unbekannter Browser")

    # Neue Struktur (Network\Cookies) bevorzugen
    cookies_db_new = os.path.join(base, "Network", "Cookies")
    cookies_db_old = os.path.join(base, "Cookies")

    if os.path.exists(cookies_db_new):
        return cookies_db_new
    elif os.path.exists(cookies_db_old):
        return cookies_db_old
    else:
        raise FileNotFoundError(f"Keine Cookies-Datenbank gefunden fÃ¼r {browser} - Profil: {profile}")

def decrypt_cookie(encrypted_value, key=None):
    """
    EntschlÃ¼sselt einen Cookie-Wert (DPAPI -> win32crypt)
    """
    try:
        return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode("utf-8")
    except Exception:
        return ""

def export_cookies_for_domain(domain, out_file="cookies.json", profile="Default", browser="chrome"):
    """
    Exportiert Cookies fÃ¼r eine Domain aus dem gewÃ¤hlten Browser
    """
    cookies_db = get_chrome_cookie_db(profile, browser)

    # Temp-Datei, weil DB gesperrt sein kann
    tmp_db = cookies_db + "_tmp"
    shutil.copy2(cookies_db, tmp_db)

    conn = sqlite3.connect(tmp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT host_key, name, path, encrypted_value FROM cookies WHERE host_key LIKE ?", ('%' + domain + '%',))

    cookies = []
    for host_key, name, path, encrypted_value in cursor.fetchall():
        value = decrypt_cookie(encrypted_value)
        cookies.append({
            "domain": host_key,
            "name": name,
            "path": path,
            "value": value
        })

    conn.close()
    os.remove(tmp_db)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2, ensure_ascii=False)

    print(f"âœ… {len(cookies)} Cookies fÃ¼r {domain} exportiert â†’ {out_file}")

def main():
    print("=== Cookie Exporter ===")
    print("[1] Chrome")
    print("[2] Edge")
    print("[3] FireFox")
    choice = input("Bitte Browser wÃ¤hlen (1-2): ").strip()

    if choice == "1":
        browser = "chrome"
    elif choice == "2":
        browser = "edge"
    elif choice == "2":
        print("Firefox has to be implemented, retry!")
    else:
        print("âŒ UngÃ¼ltige Auswahl")
        return

    domain = "kleinanzeigen"
    profile = input("Enter Profilname? (Default, Profile 1, ...): ").strip() or "Default"

    out_file = f"{browser}_{profile}_{domain}_cookies.json"
    export_cookies_for_domain(domain, out_file, profile, browser)

if __name__ == "__main__":
    main()