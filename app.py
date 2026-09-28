import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session

from database.db import (
    get_db,
    init_db,
    seed_db,
    create_user,
    get_user_by_id,
    get_expense_summary,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-not-for-production")


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")
        if "@" not in email:
            return render_template("register.html", error="Please enter a valid email address.")
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters long.")

        try:
            user_id = create_user(name, email, password)
        except sqlite3.IntegrityError:
            return render_template("register.html", error="An account with that email already exists.")

        session["user_id"] = user_id
        return redirect(url_for("landing"))

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = get_user_by_id(user_id)
    if user is None:
        session.pop("user_id", None)
        return redirect(url_for("login"))

    summary = get_expense_summary(user_id)
    member_since = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")

    return render_template(
        "profile.html",
        user=user,
        member_since=member_since,
        expense_count=summary["expense_count"],
        total_spent=summary["total_spent"],
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
