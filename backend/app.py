from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,
            date_of_birth TEXT,
            gender TEXT,
            nationality TEXT,

            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            alternate_phone TEXT,
            address TEXT NOT NULL,

            education_level TEXT,
            school TEXT,
            course TEXT,
            year_graduated INTEGER,

            employer TEXT,
            position TEXT,
            experience INTEGER,
            salary INTEGER,

            sss_number TEXT,
            tin_number TEXT,
            philhealth_number TEXT,
            pagibig_number TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return "CFG Auto-Fill Backend is running."


@app.route("/save-profile", methods=["POST"])
def save_profile():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profiles (
            full_name, date_of_birth, gender, nationality,
            email, phone, alternate_phone, address,
            education_level, school, course, year_graduated,
            employer, position, experience, salary,
            sss_number, tin_number, philhealth_number, pagibig_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("fullName"),
        data.get("dateOfBirth"),
        data.get("gender"),
        data.get("nationality"),
        data.get("email"),
        data.get("phone"),
        data.get("alternatePhone"),
        data.get("address"),
        data.get("educationLevel"),
        data.get("school"),
        data.get("course"),
        data.get("yearGraduated"),
        data.get("employer"),
        data.get("position"),
        data.get("experience"),
        data.get("salary"),
        data.get("sssNumber"),
        data.get("tinNumber"),
        data.get("philhealthNumber"),
        data.get("pagibigNumber")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Profile saved successfully"}), 201


@app.route("/get-profile", methods=["GET"])
def get_profile():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()
    conn.close()

    if profile is None:
        return jsonify({}), 404

    return jsonify(dict(profile))


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
