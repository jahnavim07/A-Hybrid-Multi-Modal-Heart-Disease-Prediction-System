"""
SQLite Database Setup and Operations
"""
import sqlite3
from datetime import datetime
from config import DATABASE_PATH


def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            sex INTEGER,
            cp INTEGER,
            trestbps INTEGER,
            chol INTEGER,
            fbs INTEGER,
            restecg INTEGER,
            thalach INTEGER,
            exang INTEGER,
            oldpeak REAL,
            slope INTEGER,
            ca INTEGER,
            thal INTEGER,
            prediction INTEGER,
            risk_score INTEGER,
            ecg_result TEXT,
            ecg_image_path TEXT,
            final_result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Cardiologists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cardiologists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT,
            hospital TEXT,
            city TEXT,
            experience_years INTEGER,
            rating REAL,
            phone TEXT,
            email TEXT,
            image_url TEXT,
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            cardiologist_id INTEGER,
            appointment_date TEXT,
            appointment_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cardiologist_id) REFERENCES cardiologists(id)
        )
    """)
    
    # Contact messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    
    # Seed cardiologists if empty
    cursor.execute("SELECT COUNT(*) FROM cardiologists")
    if cursor.fetchone()[0] == 0:
        seed_cardiologists(conn)
    
    conn.close()
    print("Database initialized successfully!")


def seed_cardiologists(conn):
    """Seed the database with top cardiologists from India."""
    cardiologists = [
        {
            "name": "Dr. Naresh Trehan",
            "specialty": "Cardiovascular & Thoracic Surgery",
            "hospital": "Medanta - The Medicity",
            "city": "Gurugram, Delhi NCR",
            "experience_years": 45,
            "rating": 4.9,
            "phone": "+91-124-4141414",
            "email": "naresh.trehan@medanta.org",
            "image_url": "https://ui-avatars.com/api/?name=Naresh+Trehan&background=00a8b5&color=fff&size=200",
            "bio": "Padma Bhushan awardee, founder of Medanta. Pioneer in coronary artery bypass and heart transplant surgeries in India."
        },
        {
            "name": "Dr. Devi Prasad Shetty",
            "specialty": "Cardiac Surgery",
            "hospital": "Narayana Health",
            "city": "Bangalore",
            "experience_years": 35,
            "rating": 4.9,
            "phone": "+91-80-71222222",
            "email": "devi.shetty@narayanahealth.org",
            "image_url": "https://ui-avatars.com/api/?name=Devi+Shetty&background=1a1f71&color=fff&size=200",
            "bio": "Padma Bhushan awardee, performed India's first neonatal heart surgery. Known for affordable healthcare mission."
        },
        {
            "name": "Dr. Ramakanta Panda",
            "specialty": "Cardiovascular & Thoracic Surgery",
            "hospital": "Asian Heart Institute",
            "city": "Mumbai",
            "experience_years": 40,
            "rating": 4.8,
            "phone": "+91-22-66986698",
            "email": "ramakanta.panda@asianheart.com",
            "image_url": "https://ui-avatars.com/api/?name=Ramakanta+Panda&background=f26522&color=fff&size=200",
            "bio": "Performed over 20,000 heart surgeries with 99.6% success rate. Operated on former PM Dr. Manmohan Singh."
        },
        {
            "name": "Dr. T.S. Kler",
            "specialty": "Interventional Cardiology",
            "hospital": "Fortis Escorts Heart Institute",
            "city": "New Delhi",
            "experience_years": 38,
            "rating": 4.8,
            "phone": "+91-11-47135000",
            "email": "ts.kler@fortisescorts.in",
            "image_url": "https://ui-avatars.com/api/?name=TS+Kler&background=00a8b5&color=fff&size=200",
            "bio": "Chairman of Fortis Heart & Vascular Institute. Pioneer in interventional cardiology with 35,000+ angioplasties."
        },
        {
            "name": "Dr. Ashok Seth",
            "specialty": "Interventional Cardiology",
            "hospital": "Fortis Escorts Heart Institute",
            "city": "New Delhi",
            "experience_years": 40,
            "rating": 4.9,
            "phone": "+91-11-47135100",
            "email": "ashok.seth@fortisescorts.in",
            "image_url": "https://ui-avatars.com/api/?name=Ashok+Seth&background=1a1f71&color=fff&size=200",
            "bio": "Padma Bhushan awardee, performed first successful coronary angioplasty in India. Over 55,000 procedures performed."
        },
        {
            "name": "Dr. K. Srinath Reddy",
            "specialty": "Preventive Cardiology",
            "hospital": "Public Health Foundation of India",
            "city": "New Delhi",
            "experience_years": 42,
            "rating": 4.7,
            "phone": "+91-11-46046000",
            "email": "ksrinath.reddy@phfi.org",
            "image_url": "https://ui-avatars.com/api/?name=Srinath+Reddy&background=f26522&color=fff&size=200",
            "bio": "Former President of World Heart Federation. Leading authority on cardiovascular disease prevention."
        },
        {
            "name": "Dr. V. Bhaskar Rao",
            "specialty": "Cardiothoracic Surgery",
            "hospital": "Apollo Hospitals",
            "city": "Chennai",
            "experience_years": 30,
            "rating": 4.7,
            "phone": "+91-44-28293333",
            "email": "bhaskar.rao@apollohospitals.com",
            "image_url": "https://ui-avatars.com/api/?name=Bhaskar+Rao&background=00a8b5&color=fff&size=200",
            "bio": "Senior Consultant in Cardiothoracic Surgery. Expert in minimally invasive cardiac surgery and valve repairs."
        },
        {
            "name": "Dr. C.N. Manjunath",
            "specialty": "Interventional Cardiology",
            "hospital": "Sri Jayadeva Institute of Cardiovascular Sciences",
            "city": "Bangalore",
            "experience_years": 32,
            "rating": 4.8,
            "phone": "+91-80-22977700",
            "email": "cn.manjunath@jayadevacardiology.com",
            "image_url": "https://ui-avatars.com/api/?name=CN+Manjunath&background=1a1f71&color=fff&size=200",
            "bio": "Director of India's largest cardiac hospital. Performed over 40,000 coronary interventions."
        },
        {
            "name": "Dr. P. Rajasekhar",
            "specialty": "Interventional Cardiology",
            "hospital": "Apollo Hospitals",
            "city": "Hyderabad",
            "experience_years": 28,
            "rating": 4.7,
            "phone": "+91-40-23607777",
            "email": "rajasekhar.p@apollohospitals.com",
            "image_url": "https://ui-avatars.com/api/?name=P+Rajasekhar&background=f26522&color=fff&size=200",
            "bio": "Chief Interventional Cardiologist. Expertise in complex coronary interventions and structural heart disease."
        },
        {
            "name": "Dr. Kunal Sarkar",
            "specialty": "Cardiac Surgery",
            "hospital": "Medica Superspecialty Hospital",
            "city": "Kolkata",
            "experience_years": 30,
            "rating": 4.8,
            "phone": "+91-33-66520000",
            "email": "kunal.sarkar@medicahospitals.in",
            "image_url": "https://ui-avatars.com/api/?name=Kunal+Sarkar&background=00a8b5&color=fff&size=200",
            "bio": "Chief Cardiac Surgeon. Pioneered robotic cardiac surgery in Eastern India."
        },
        {
            "name": "Dr. Sameer Mehrotra",
            "specialty": "Interventional Cardiology",
            "hospital": "Wockhardt Hospital",
            "city": "Mumbai",
            "experience_years": 25,
            "rating": 4.6,
            "phone": "+91-22-26570200",
            "email": "sameer.mehrotra@wockhardthospitals.com",
            "image_url": "https://ui-avatars.com/api/?name=Sameer+Mehrotra&background=1a1f71&color=fff&size=200",
            "bio": "Senior Interventional Cardiologist. Expert in TAVI and percutaneous valve repairs."
        },
        {
            "name": "Dr. H.K. Chopra",
            "specialty": "Preventive Cardiology",
            "hospital": "Moolchand Medcity",
            "city": "New Delhi",
            "experience_years": 42,
            "rating": 4.7,
            "phone": "+91-11-42000000",
            "email": "hk.chopra@moolchandhealthcare.com",
            "image_url": "https://ui-avatars.com/api/?name=HK+Chopra&background=f26522&color=fff&size=200",
            "bio": "Chief Cardiologist. President of Cardiological Society of India. Pioneer in heart failure management."
        }
    ]
    
    cursor = conn.cursor()
    for doc in cardiologists:
        cursor.execute("""
            INSERT INTO cardiologists (name, specialty, hospital, city, experience_years, rating, phone, email, image_url, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc["name"], doc["specialty"], doc["hospital"], doc["city"],
            doc["experience_years"], doc["rating"], doc["phone"], doc["email"],
            doc["image_url"], doc["bio"]
        ))
    conn.commit()
    print(f"Seeded {len(cardiologists)} cardiologists into database.")


def save_patient_record(data):
    """
    Save a patient record to the database.
    
    Args:
        data: Dictionary containing patient data
        
    Returns:
        int: The ID of the inserted record
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO patients (
            name, age, sex, cp, trestbps, chol, fbs, restecg,
            thalach, exang, oldpeak, slope, ca, thal,
            prediction, risk_score, ecg_result, ecg_image_path, final_result, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name", "Anonymous"),
        data["age"],
        data["sex"],
        data["cp"],
        data["trestbps"],
        data["chol"],
        data["fbs"],
        data["restecg"],
        data["thalach"],
        data["exang"],
        data["oldpeak"],
        data["slope"],
        data["ca"],
        data["thal"],
        data["prediction"],
        data.get("risk_score"),
        data.get("ecg_result"),
        data.get("ecg_image_path"),
        data.get("final_result"),
        datetime.now()
    ))
    
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return patient_id


def get_patient_by_id(patient_id):
    """Get a patient record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    
    conn.close()
    return dict(patient) if patient else None


def get_all_patients():
    """Get all patient records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    patients = cursor.fetchall()
    
    conn.close()
    return [dict(p) for p in patients]


# -------------------------
# Cardiologist Functions
# -------------------------

def get_all_cardiologists(city=None):
    """Get all cardiologists, optionally filtered by city."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if city:
        cursor.execute("SELECT * FROM cardiologists WHERE city LIKE ? ORDER BY rating DESC", (f"%{city}%",))
    else:
        cursor.execute("SELECT * FROM cardiologists ORDER BY rating DESC")
    
    cardiologists = cursor.fetchall()
    conn.close()
    return [dict(c) for c in cardiologists]


def get_cardiologist_by_id(cardiologist_id):
    """Get a cardiologist by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cardiologists WHERE id = ?", (cardiologist_id,))
    cardiologist = cursor.fetchone()
    
    conn.close()
    return dict(cardiologist) if cardiologist else None


# -------------------------
# Appointment Functions
# -------------------------

def save_appointment(data):
    """Save an appointment to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO appointments (patient_name, email, phone, cardiologist_id, appointment_date, appointment_time, reason, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
    """, (
        data["patient_name"],
        data.get("email"),
        data.get("phone"),
        data.get("cardiologist_id"),
        data.get("appointment_date"),
        data.get("appointment_time"),
        data.get("reason"),
        datetime.now()
    ))
    
    appointment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return appointment_id


def get_all_appointments():
    """Get all appointments with cardiologist details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT a.*, c.name as doctor_name, c.hospital, c.city
        FROM appointments a
        LEFT JOIN cardiologists c ON a.cardiologist_id = c.id
        ORDER BY a.created_at DESC
    """)
    appointments = cursor.fetchall()
    
    conn.close()
    return [dict(a) for a in appointments]


# -------------------------
# Contact Message Functions
# -------------------------

def save_contact_message(data):
    """Save a contact message to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO contact_messages (name, email, phone, message, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data.get("email"),
        data.get("phone"),
        data.get("message"),
        datetime.now()
    ))
    
    message_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return message_id


def get_all_contact_messages():
    """Get all contact messages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    
    conn.close()
    return [dict(m) for m in messages]


if __name__ == "__main__":
    init_db()

