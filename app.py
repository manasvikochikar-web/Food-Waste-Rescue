import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "users.db")
_db_initialized = False


def use_postgres():
    return bool(DATABASE_URL)


def get_db():
    if use_postgres():
        import psycopg2

        url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(url)

    return sqlite3.connect(DATABASE_PATH)


def init_db():
    conn = get_db()
    try:
        if use_postgres():
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        password TEXT NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    )
                    """
                )
        else:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


def ensure_db():
    global _db_initialized
    if _db_initialized:
        return True
    try:
        init_db()
        _db_initialized = True
        return True
    except Exception:
        app.logger.exception("Database initialization failed")
        return False


@app.route("/health")
def health():
    return "ok", 200


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")

    if not all([username, email, phone, password]):
        return redirect(url_for("index"))

    if not ensure_db():
        return redirect(url_for("index"))

    conn = get_db()
    if use_postgres():
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, phone, password)
                VALUES (%s, %s, %s, %s)
                """,
                (username, email, phone, password),
            )
    else:
        conn.execute(
            """
            INSERT INTO users (username, email, phone, password)
            VALUES (?, ?, ?, ?)
            """,
            (username, email, phone, password),
        )
    conn.commit()
    conn.close()

    return redirect(url_for("main_page"))


@app.route("/main")
def main_page():
    return render_template("main.html")


@app.route("/donate")
def donate():
    return render_template("donate.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
