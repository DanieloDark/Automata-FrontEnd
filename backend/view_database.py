import sqlite3
from pathlib import Path
import csv

DB_NAME = "database.db"
EXPORT_DIR = "exports"

# Frontend → Database mapping
FIELD_MAPPING = {
    "fullName": "full_name",
    "dateOfBirth": "date_of_birth",
    "gender": "gender",
    "nationality": "nationality",
    "email": "email",
    "phone": "phone",
    "address": "address",
    "educationLevel": "education",
    "school": "school",
    "course": "course",
    "yearGraduated": "year_graduated",
    "employer": "employer",
    "position": "position",
    "experience": "experience",
    "salary": "salary",
    "sssNumber": "sss_number",
    "tinNumber": "tin_number",
    "philhealthNumber": "philhealth_number",
    "pagibigNumber": "pagibig_number",
}

def main():
    db_path = Path(DB_NAME)

    if not db_path.exists():
        print(f"Database file '{DB_NAME}' not found.")
        return

    print(f"Opening database in READ-ONLY mode: {DB_NAME}")

    # Explicit read-only connection
    conn = sqlite3.connect(f"file:{DB_NAME}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create export folder
    Path(EXPORT_DIR).mkdir(exist_ok=True)

    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t["name"] for t in cursor.fetchall() if not t["name"].startswith("sqlite_")]

    print("\nTables found:")
    for t in tables:
        print(f"  - {t}")

    print("\n" + "=" * 60)

    # Process each table
    for table in tables:
        print(f"\nTABLE: {table}")
        print("-" * 60)

        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        if not rows:
            print("  (No records)")
            continue

        # Print records
        for i, row in enumerate(rows, start=1):
            print(f"\n  Record {i}")
            for key in row.keys():
                print(f"     {key}: {row[key]}")

        # Export to CSV
        csv_path = Path(EXPORT_DIR) / f"{table}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            for row in rows:
                writer.writerow(row)

        print(f"\nExported to {csv_path}")

    # Show field mapping
    print("\n" + "=" * 60)
    print("Frontend → Database Field Mapping")
    print("-" * 60)

    for frontend, backend in FIELD_MAPPING.items():
        print(f"  {frontend:<20} → {backend}")

    conn.close()
    print("\nInspection complete (SAFE / READ-ONLY).")

if __name__ == "__main__":
    main()
