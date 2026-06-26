import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "users.db")


def use_postgres():
    return bool(DATABASE_URL)


def get_db_connection():
    if use_postgres():
        import psycopg2

        url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(url)

    return sqlite3.connect(DATABASE_PATH)


def init_db():
    conn = get_db_connection()
    if use_postgres():
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    password TEXT NOT NULL
                )
                """
            )
    else:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (username TEXT, email TEXT, phone TEXT, password TEXT)
            """
        )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    conn = get_db_connection()
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
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (username, email, phone, password),
        )
    conn.commit()
    conn.close()

    return redirect(url_for("main_page"))


@app.route("/main")
def main_page():
    return render_template("main.html")


@app.route("/donate.html")
def donate():
    return render_template("donate.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
