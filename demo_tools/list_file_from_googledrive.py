from dotenv import load_dotenv
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
from langchain_core.tools import tool

# Load environment variables from .env file
load_dotenv()

# Access variables using os.environ
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")
# Access variables using os.environ
SCOPES = [os.environ.get("DRIVE_SCOPES")]

# file_path= SERVICE_ACCOUNT_FILE
# if os.path.exists(file_path):
#     if os.path.isfile(file_path):
#         print(f"ไฟล์ '{file_path}' มีอยู่จริงครับ!")
#     else:
#         print(f"'{file_path}' มีอยู่จริง แต่มันไม่ใช่ไฟล์ (อาจจะเป็นโฟลเดอร์หรืออย่างอื่น)")
# else:
#     print(f"หาไฟล์ '{file_path}' ไม่เจอครับ")

# สร้าง credentials จาก Service Account
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# สร้าง service สำหรับ Google Drive API
service = build('drive', 'v3', credentials=creds)

def list_files_from_folder_url(folder_url):
    """
    รับ URL ของ Google Drive Folder และแสดงรายการไฟล์ภายในโฟลเดอร์นั้น พร้อมลิงก์ URL ของไฟล์
    """
    # 🔹 ดึง Folder ID จาก URL
    folder_id = None
    match = re.search(r'/folders/([a-zA-Z0-9-_]+)', folder_url)
    if match:
        folder_id = match.group(1)
    else:
        return "❌ ไม่พบ Folder ID จาก URL ที่ระบุ"
    
    # 🔍 ค้นหาไฟล์ใน Folder ที่ระบุ
    query = f"'{folder_id}' in parents"
    results = service.files().list(
        q=query,
        pageSize=100,  # จำนวนไฟล์ต่อหน้า
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    # ==============================
    # 🔹 สร้างข้อความสำหรับ Return
    # ==============================
    if not items:
        return 'ไม่พบไฟล์ในโฟลเดอร์นี้'
    else:
        output = f'📂 ไฟล์ทั้งหมดในโฟลเดอร์ ({folder_url}):\n'
        for item in items:
            file_link = f"https://drive.google.com/file/d/{item['id']}/view?usp=sharing"
            output += f"📄 {item['name']} (ID: {item['id']}, Type: {item['mimeType']})\n   🔗 URL: {file_link}\n"
        return output
    
@tool
def google_drive_file(url) -> int:
    """ใช้สำหรับดึงรายการไฟล์จาก Google Drive Folder URL"""
    print(url)
    return list_files_from_folder_url(url)
