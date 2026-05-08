import re
import csv
import datetime
from pathlib import Path
import pdfplumber


DEFAULT_PDF_PATH = "../data/jrc_blood_donation_report_raw.pdf"
DEFAULT_CSV_PATH = "../data/BloodDonation.csv"

PREFECTURES = [
    "北海道", "青森", "岩手", "宮城", "秋田", "山形", "福島", "茨城", "栃木", "群馬", 
    "埼玉", "千葉", "東京", "神奈川", "新潟", "富山", "石川", "福井", "山梨", "長野", 
    "岐阜", "静岡", "愛知", "三重", "滋賀", "京都", "大阪", "兵庫", "奈良", "和歌山", 
    "鳥取", "島根", "岡山", "広島", "山口", "徳島", "香川", "愛媛", "高知", "福岡", 
    "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄"
]

def extract_and_parse_tables(pdf_path: Path) -> list[list]:
    results = []

    # 縦は罫線、横は文字の行
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "text" 
    }

    with pdfplumber.open(pdf_path) as document:
        for page in document.pages:
            tables = page.extract_tables(table_settings)
            
            for table in tables:
                for row in table:
                    if not row:
                        continue # 空の行はスキップ
                    
                    # 改行除去とNoneを空文字に変換
                    cells = [str(c).replace('\n', '').strip() if c is not None else "" for c in row]
                    
                    # 左から5列目までの中で都道府県名を探す
                    pref_name = None
                    data_cells = []
                    
                    for i, cell in enumerate(cells[:5]):
                        clean_cell = cell.replace(' ', '')
                        if clean_cell in PREFECTURES:
                            pref_name = clean_cell
                            # 都道府県が見つかったら、それより右側を取得
                            data_cells = cells[i+1:]
                            break

                    if not pref_name:
                        continue
                    
                    processed_nums = []
                    for dc in data_cells:
                        # 数字（カンマ含む）だけを抽出
                        nums = re.findall(r'[\d,]+', dc)
                        if not nums:
                            processed_nums.append(0)  # 0埋め
                        else:
                            processed_nums.append(int(nums[0].replace(',', '')))
                    
                    # 0埋め
                    while len(processed_nums) < 15:
                        processed_nums.append(0)
                        
                    donor_counts = [
                        processed_nums[0],
                        processed_nums[2],
                        processed_nums[4],
                        processed_nums[6],
                        processed_nums[9],
                        processed_nums[11],
                        processed_nums[13]
                    ]
                    
                    results.append([pref_name] + donor_counts)
                    
    return results

def write_to_csv(parsed_data: list[list], output_path: Path):
    now = datetime.datetime.today()
    first_day_of_this_month = now.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - datetime.timedelta(days=1)
    
    year = str(last_day_of_last_month.year)
    month = str(last_day_of_last_month.month)
    
    rows = []
    for row in parsed_data:
        pref_name = row[0]
        counts = row[1:]
        pref_id = str(PREFECTURES.index(pref_name) + 1)
        rows.append([year, month, pref_id] + counts)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

if __name__ == "__main__":
    pdf_path = Path(DEFAULT_PDF_PATH)
    csv_path = Path(DEFAULT_CSV_PATH)

    parsed_data = extract_and_parse_tables(pdf_path)

    # print(parsed_data)

    write_to_csv(parsed_data, csv_path)