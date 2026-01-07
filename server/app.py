import os
from flask import Flask, render_template, session, redirect, request, jsonify
from Token import Tokenizer
from Parser import Parser
from database import init_db, get_db
from flask_cors import CORS


# Point to the root directory (one level up from /server)
base_dir = os.path.abspath('..')
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')



app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

CORS(app)
app.secret_key = "my_secret_key"

@app.route('/')
def index():
    if session.get("fullname"):
        return render_template('index.html')  # main page
    return render_template('landing.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/process')
def process():
    # Path to test form image
    path = "../form_images/onboarding_form.png"

    # Tokenize the uploaded file
    tokenizer = Tokenizer(path)

    try:
        tokens, height_width_dim = tokenizer.tokenize_file()
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    # Parse tokens
    parser = Parser()
    accepted, errors = parser(tokens)

    if not accepted:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    # Serialize tokens
    serialized_tokens = [
        {
            "id": token.id,
            "type": token.type,
            "value": token.value,
            "x": token.bbox[0],
            "y": token.bbox[1],
            "w": token.bbox[2],
            "h": token.bbox[3],
            "page": token.page
        }
        for token in tokens
    ]

    return jsonify({
        "success": True,
        "height_width_dim": height_width_dim,
        "tokens": serialized_tokens,
        "mappings": parser.mappings
    }), 200


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # MATCH landing.js
    fullname = data.get("name")
    email = data.get("email")
    password = data.get("password")
    session["fullname"] = fullname


    print("SIGNUP DATA:", fullname, email)  # DEBUG (you can remove later)

    if not fullname or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (fullname, email, password)
            VALUES (?, ?, ?)
            """,
            (fullname, email, password)
        )
        db.commit()
    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"error": "User already exists"}), 409
    finally:
        db.close()

    return jsonify({
        "message": "Signup successful",
        "token": "dummy-token-for-now"
    }), 200


@app.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.get_json()

    # 🔍 DEBUG: see exactly what frontend sends
    print("LOGIN RAW JSON:", data)

    email = data.get("email")
    password = data.get("password")

    print("EMAIL:", email)
    print("PASSWORD:", password)

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    cursor = db.cursor()

    cursor.execute("SELECT fullname, email, password FROM users")
    print("ALL USERS IN DB:", cursor.fetchall())

    cursor.execute(
        "SELECT fullname FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cursor.fetchone()

    print("LOGIN QUERY RESULT:", user)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    session["fullname"] = user[0]

    print("SESSION AFTER LOGIN:", dict(session))

    return jsonify({
        "message": "Login successful"
    }), 200


    
    

# @app.route('/submit', methods=["POST"])
# def submit():
#     print("Got here!")
#
#     names = [
#         "fullname",
#         "dateofbirth",
#         "gender",
#         "nationality",
#         "email",
#         "phonenumber",
#         "alternatephone",
#         "address",
#         "highesteducationlevel",
#         "school",
#         "course",
#         "yeargraduated",
#         "currentemployer",
#         "jobtitle",
#         "yearsofexperience",
#         "monthlysalary",
#         "sssnumber",
#         "tinnumber",
#         "philhealthnumber",
#         "pagibignumber"
#     ]
#
#     for name in names:
#         session[name] = request.form.get(name)
#
#     return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)