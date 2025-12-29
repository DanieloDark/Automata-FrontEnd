from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE_NAME = "database.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)


    conn.commit()
    conn.close()


@app.route("/")
def index():
    return "CFG Auto-Fill Backend is running."

@app.route("/clear-profile", methods=["POST"])
def clear_profile():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles")
    conn.commit()
    conn.close()
    return "", 204


@app.route("/save-profile", methods=["POST"])
def save_profile():

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles")
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

    # Convert snake_case → camelCase
    return jsonify({
        "fullName": profile["full_name"],
        "dateOfBirth": profile["date_of_birth"],
        "gender": profile["gender"],
        "nationality": profile["nationality"],
        "email": profile["email"],
        "phone": profile["phone"],
        "alternatePhone": profile["alternate_phone"],
        "address": profile["address"],
        "educationLevel": profile["education_level"],
        "school": profile["school"],
        "course": profile["course"],
        "yearGraduated": profile["year_graduated"],
        "employer": profile["employer"],
        "position": profile["position"],
        "experience": profile["experience"],
        "salary": profile["salary"],
        "sssNumber": profile["sss_number"],
        "tinNumber": profile["tin_number"],
        "philhealthNumber": profile["philhealth_number"],
        "pagibigNumber": profile["pagibig_number"]
    })

@app.route("/upload-document", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (filename, file_path, file_type) VALUES (?, ?, ?)",
        (filename, file_path, file.mimetype)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Document uploaded successfully"}), 201


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
