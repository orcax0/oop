import os
import subprocess
import getpass
import requests

print("--- 🚀 أداة الأتمتة الشاملة لرفع مواقعك على GitHub ---")

# 1. إدخال البيانات الأساسية
USERNAME = "orcax0"
repo_name = input("اكتب اسم المشروع/المستودع الجديد (مثلاً: orcac-site): ").strip()

if not repo_name:
    print("[-] اسم المستودع لا يمكن أن يكون فارغاً.")
    exit()

# طلب التوكن بأمان
GITHUB_TOKEN = getpass.getpass("اكتب GitHub Personal Access Token الخاص بك (لن يظهر أثناء الكتابة): ")

if not GITHUB_TOKEN:
    print("[-] لم تقم بإدخال التوكن.")
    exit()

# 2. إنشاء المستودع على GitHub أوتوماتيكياً عبر الـ API
print(f"[+] جاري إنشاء المستودع '{repo_name}' على حسابك في GitHub...")
api_url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
data = {
    "name": repo_name,
    "description": "Auto-deployed via Python script",
    "private": False  # خليه عام عشان يشتغل مع GitHub Pages مجاناً
}

response = requests.post(api_url, json=data, headers=headers)

if response.status_code == 201:
    print("[✓] تم إنشاء المستودع بنجاح!")
elif response.status_code == 422:
    print("[!] المستودع موجود مسبقاً على حسابك، سنكمل عملية الرفع عليه مباشرة.")
else:
    print(f"[-] حدث خطأ أثناء إنشاء المستودع: {response.json().get('message', 'خطأ غير معروف')}")
    # نكمل لو المستودع موجود أصلاً

# 3. إعداد مجلد المشروع محلياً ورفع الملفات
remote_url = f"https://{GITHUB_TOKEN}@github.com/{USERNAME}/{repo_name}.git"

commands = [
    ["git", "init"],
    ["git", "remote", "remove", "origin"],  # لو فيه ريموت قديم بنحذفه
    ["git", "remote", "add", "origin", remote_url],
    ["git", "branch", "-M", "main"],
    ["git", "add", "."],
    ["git", "commit", "-m", "Auto deploy via Python script"]
]

print("[+] جاري تجهيز الملفات محلياً...")
for cmd in commands:
    subprocess.run(cmd, capture_output=True, text=True)

# 4. الرفع النهائي (Push)
print("[+] جاري رفع الملفات إلى GitHub...")
push_result = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)

if push_result.returncode == 0:
    print("\n" + "=" * 50)
    print(f"[🎉] تم رفع موقعك بنجاح تام يا بطل!")
    print(f"🌐 رابط موقعك المتوقع على GitHub Pages:")
    print(f"https://{USERNAME}.github.io/{repo_name}/")
    print("=" * 50)
    print("ملاحظة: لو ظهر خطأ 404، ادخل لصفحة الـ Settings -> Pages للمستودع وفعل فرع الـ main لمرة واحدة فقط.")
else:
    print("[-] حدث خطأ أثناء الرفع:")
    print(push_result.stderr)

