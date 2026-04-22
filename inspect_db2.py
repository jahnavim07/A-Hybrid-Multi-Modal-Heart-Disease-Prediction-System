import sqlite3
import json

def get_docs():
    conn = sqlite3.connect("patient_records.db")
    conn.row_factory = sqlite3.Row
    docs = [dict(row) for row in conn.execute("SELECT id, name, image_url FROM cardiologists").fetchall()]
    return docs

if __name__ == "__main__":
    with open("docs.json", "w") as f:
        json.dump(get_docs(), f, indent=2)
    print("Done")
