import sqlite3

DB_NAME = "app.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # --------------------------------------------------
    # USERS TABLE (AUTH + PROFILE)
    # --------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT,

        dateofbirth TEXT,
        gender TEXT,
        nationality TEXT,
        phone TEXT,
        alternatephone TEXT,
        address TEXT,
        education TEXT,
        school TEXT,
        course TEXT,
        yeargraduated TEXT,
        employer TEXT,
        jobtitle TEXT,
        experience TEXT,
        salary TEXT,
        sss TEXT,
        tin TEXT,
        philhealth TEXT,
        pagibig TEXT
    )
    """)

    # --------------------------------------------------
    # DOCUMENTS TABLE
    # --------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --------------------------------------------------
    # TOKENS TABLE (OCR OUTPUT)
    # --------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        token_type TEXT,
        token_value TEXT,
        x INTEGER,
        y INTEGER,
        w INTEGER,
        h INTEGER,
        page INTEGER,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """)

    # --------------------------------------------------
    # MAPPINGS TABLE (CFG PARSER OUTPUT)
    # --------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mappings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        section TEXT,
        label TEXT,
        x INTEGER,
        y INTEGER,
        w INTEGER,
        h INTEGER,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """)

    conn.commit()
    conn.close()
