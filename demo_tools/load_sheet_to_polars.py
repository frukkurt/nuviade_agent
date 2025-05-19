from dotenv import load_dotenv
import os

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import polars as pl
from langchain_core.documents import Document
import re
from langchain_core.tools import tool

load_dotenv()

# Access variables using os.environ
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")
# Access variables using os.environ
SCOPES = [os.environ.get("SHEET_SCOPES")]


credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
gc = gspread.authorize(credentials)

# ==============================
# 🔹 ฟังก์ชันดึงข้อมูลจาก Google Sheets เป็น Polars DataFrame
def extract_file_id(url):
    pattern = r'/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


# ==============================
def load_sheet_to_polars(sheet_url):
    """
    รับ URL ของ Google Sheets แล้วดึงข้อมูลทั้งหมดออกมาเป็น Polars DataFrame
    """
    sheet_url_extract = extract_file_id(sheet_url)
    templateurl = f"https://docs.google.com/spreadsheets/d/{sheet_url_extract}"
    print(templateurl)
    # 🔹 เปิด Google Sheets ตาม URL
    sheet = gc.open_by_url(templateurl)
    worksheet = sheet.get_worksheet(0)  # เลือก Sheet แรก (index 0)

    # 🔹 ดึงข้อมูลทั้งหมดจาก Sheet
    data = worksheet.get_all_values()

    if not data:
        print("❌ ไม่พบข้อมูลใน Google Sheets ที่ระบุ")
        return None
    
    # 🔹 แปลงข้อมูลเป็น Polars DataFrame
    df = pl.DataFrame(data[1:], schema=data[0])
    # 🔹 สร้าง Document List
    document_list = [Document(page_content=str(row)) for row in df.iter_rows(named=True)]

    if not document_list:
        print("❌ ไม่พบข้อมูลที่สามารถแปลงเป็น Document ได้")
        return None
    
    return document_list

@tool
def google_sheet(url) -> int:
    """ใช้สำหรับดึงข้อมูลจาก Google Sheets URL"""
    response = load_sheet_to_polars(url)

    return response