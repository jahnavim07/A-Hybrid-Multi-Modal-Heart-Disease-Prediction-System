import sqlite3
import os


DB_PATH = "patient_records.db"

def inspect_db():
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print(f"\n--- Database Inspection: {DB_PATH} ---\n")

    if not tables:
        print("No tables found in the database.")
        conn.close()
        return

    for table in tables:
        table_name = table[0]
        if table_name == "sqlite_sequence":
            continue
            
        print(f"Table: {table_name}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  Row Count: {count}")
        
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        print(f"  Columns: {', '.join(col_names)}")
        
        # Show sample data (first 3 rows)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        rows = cursor.fetchall()
        
        if rows:
            print("  Sample Data:")
            for row in rows:
                print(f"    {row}")
        else:
            print("  (Table is empty)")
        
        print("-" * 40)

    conn.close()

if __name__ == "__main__":
    inspect_db()
