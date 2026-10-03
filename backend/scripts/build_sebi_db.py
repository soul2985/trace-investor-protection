"""
Script to parse official SEBI Excel lists into an indexed JSON database.
Snapshot date: October 03, 2026
"""
import os
import json
import xlrd

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

def normalize_reg_no(reg_no):
    return clean_str(reg_no).replace(" ", "").replace("-", "").upper()

def parse_sebi_file(file_path, category_name):
    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}")
        return []
    
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    records = []
    
    # Data begins at row 3 (0-indexed)
    for r in range(3, sheet.nrows):
        name = clean_str(sheet.cell_value(r, 0))
        reg_no = normalize_reg_no(sheet.cell_value(r, 1))
        contact = clean_str(sheet.cell_value(r, 2))
        email = clean_str(sheet.cell_value(r, 4))
        telephone = clean_str(sheet.cell_value(r, 5))
        city = clean_str(sheet.cell_value(r, 7))
        state = clean_str(sheet.cell_value(r, 8))
        pincode = clean_str(sheet.cell_value(r, 9))
        valid_from = clean_str(sheet.cell_value(r, 17))
        valid_to = clean_str(sheet.cell_value(r, 18))
        
        if reg_no:
            records.append({
                "reg_no": reg_no,
                "name": name,
                "type": category_name,
                "contact_person": contact,
                "email": email,
                "telephone": telephone,
                "city": city,
                "state": state,
                "pincode": pincode,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "snapshot_date": "October 03, 2026"
            })
    return records

def build_database():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sebi_dir = os.path.join(base_dir, "SEBI")
    data_dir = os.path.join(base_dir, "backend", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    ia_file = os.path.join(sebi_dir, "Investment Adviser as on Oct 03 2026.xls")
    ra_file = os.path.join(sebi_dir, "Research Analyst as on Oct 03 2026.xls")
    
    ia_records = parse_sebi_file(ia_file, "Investment Adviser")
    ra_records = parse_sebi_file(ra_file, "Research Analyst")
    
    all_records = ia_records + ra_records
    
    # Build lookup dictionaries
    by_reg_no = {}
    by_name = []
    
    for rec in all_records:
        r_no = rec["reg_no"]
        by_reg_no[r_no] = rec
        by_name.append({
            "name_lower": rec["name"].lower(),
            "contact_lower": rec["contact_person"].lower(),
            "reg_no": r_no,
            "type": rec["type"]
        })
        
    output_data = {
        "snapshot_date": "October 03, 2026",
        "total_records": len(all_records),
        "ia_count": len(ia_records),
        "ra_count": len(ra_records),
        "by_reg_no": by_reg_no,
        "name_index": by_name
    }
    
    out_path = os.path.join(data_dir, "sebi_registry.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated SEBI database at {out_path}")
    print(f"Total: {len(all_records)} (IA: {len(ia_records)}, RA: {len(ra_records)})")
    return out_path

if __name__ == "__main__":
    build_database()
