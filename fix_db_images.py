import sqlite3
import shutil
import os

db_path = "patient_records.db"
static_dir = "static"
doc7_source = r"C:\Users\nagah\.gemini\antigravity\brain\5784579d-cf94-428e-9b18-baace42e3535\doc7_1774251615198.png"
doc7_dest = os.path.join(static_dir, "doc7.png")

# Copy doc7 image
if os.path.exists(doc7_source):
    shutil.copy(doc7_source, doc7_dest)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update Doc 7
cursor.execute("UPDATE cardiologists SET image_url = '/static/doc7.png' WHERE id = 7")

# Update Docs 8-12 with UI Avatars
avatars = [
    (8, "https://ui-avatars.com/api/?name=CN+Manjunath&background=1a1f71&color=fff&size=200"),
    (9, "https://ui-avatars.com/api/?name=P+Rajasekhar&background=f26522&color=fff&size=200"),
    (10, "https://ui-avatars.com/api/?name=Kunal+Sarkar&background=00a8b5&color=fff&size=200"),
    (11, "https://ui-avatars.com/api/?name=Sameer+Mehrotra&background=1a1f71&color=fff&size=200"),
    (12, "https://ui-avatars.com/api/?name=HK+Chopra&background=f26522&color=fff&size=200")
]

for doc_id, url in avatars:
    cursor.execute("UPDATE cardiologists SET image_url = ? WHERE id = ?", (url, doc_id))

conn.commit()
conn.close()
print("Database updated with correct images!")
