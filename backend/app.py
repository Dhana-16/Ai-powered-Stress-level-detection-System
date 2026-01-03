from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db and models
from models import db, User, Report

# Initialize db with this app
db.init_app(app)

with app.app_context():
    db.create_all()  #

model = joblib.load("../model/stress_model.pkl")

FEATURE_COLUMNS = [
    "Gender",
    "Country",
    "Occupation",
    "self_employed",
    "family_history",
    "treatment",
    "Days_Indoors",
    "Growing_Stress",
    "Changes_Habits",
    "Mental_Health_History",
    "Mood_Swings",
    "Coping_Struggles",
    "Work_Interest",
    "Social_Weakness",
    "mental_health_interview",
    "care_options"
]


from werkzeug.security import check_password_hash
from flask import request, redirect, url_for, flash
from models import User, db
from flask import session
from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return redirect(url_for("home"))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.full_name   # ✅ IMPORTANT
            session["user_email"] = user.email

            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        accepted_terms = request.form.get("accepted_terms")

        if not full_name or not email or not password:
            flash("All fields are required")
            return redirect(url_for("register"))

        if not accepted_terms:
            flash("You must accept the Neural Data Processing Protocol")
            return redirect(url_for("register"))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            accepted_terms=True
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/")
def index():
    return render_template("index.html")   # ✅ FIXED

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")
@app.route("/category")
def category():
    return render_template("category.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name")
    )

@app.route("/housewife")
def housewife():
    return render_template("housewife.html")
@app.route("/kids")
def kids():
    return render_template("kids.html")
@app.route("/reports")
def reports():
    if "user_name" not in session:
        return redirect("/login")

    return render_template(
        "reports.html",
        user_name=session["user_name"]
    )

@app.route("/api/reports")
def get_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()

    data = []
    for r in reports:
        data.append({
            "id": r.id,
            "user": r.user_name,
            "location": r.location,
            "category": r.category,
            "img": r.image,
            "score": r.stress_score,
            "timestamp": r.created_at.strftime("%d %b %Y")
        })

    return jsonify(data)
@app.route("/api/upload", methods=["POST"])
def upload_report():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    report = Report(
        user_name=session.get("user_name", "Anonymous"),
        location=data.get("location"),
        category=data.get("category"),
        image=data.get("image"),
        stress_score=data.get("score", 0)
    )

    db.session.add(report)
    db.session.commit()

    return jsonify({"status": "success"})

@app.route("/result")
def result():
    return render_template("result.html")
@app.route("/student")
def student():
    return render_template("student.html")
@app.route("/tips")
def tips():
    return render_template("tips.html")
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    try:
        features = [data[col] for col in FEATURE_COLUMNS]
        features = np.array(features, dtype=float).reshape(1, -1)

        prediction = model.predict(features)[0]

        stress_levels = {
            0: "Low Stress",
            1: "Medium Stress",
            2: "High Stress"
        }

        return jsonify({
            "stress_level": stress_levels[prediction]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/artist_ques")
def artist_ques():
    return render_template("artist_ques.html")
@app.route("/artist")
def artist():
    return render_template("artist.html")
@app.route("/athlete_ques")
def athlete_ques():
    return render_template("athlete_ques.html")
@app.route("/athlete")
def athlete():
    return render_template("athlete.html")
@app.route("/business_ques")
def business_ques():
    return render_template("business_ques.html")
@app.route("/business")
def business():
    return render_template("business.html")
@app.route("/cog_load_monitor")
def cog_load_monitor():
    return render_template("cog_load_monitor.html")
@app.route("/college_ques")
def college_ques():
    return render_template("college_ques.html")
@app.route("/college")
def college():
    return render_template("college.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/doctor")
def doctor():
    return render_template("doctor.html")
@app.route("/doctor_ques")
def doctor_ques():
    return render_template("doctors_ques.html")
@app.route("/engineer_ques")
def engineer_ques():
    return render_template("engineer_ques.html")
@app.route("/engineer")
def engineer():
    return render_template("engineer.html")
@app.route("/exam")
def exam():
    return render_template("exam.html")
@app.route("/familyissues_ques")
def familyissues_ques():
    return render_template("familyissues_ques.html")
@app.route("/familyissues")
def familyissues():
    return render_template("familyissues.html")
@app.route("/farmer_dashboard")
def farmer_dashboard():
    return render_template("farmer_dashboard.html")
@app.route("/farmer_ques")
def farmer_ques():
    return render_template("farmer_ques.html")
@app.route("/student_ques")
def student_ques():
    return render_template("student_ques.html")
@app.route("/farmer")
def farmer():
    return render_template("farmer.html")
@app.route("/housewives_ques")
def housewives_ques():
    return render_template("housewives_ques.html")
@app.route("/it")
def it():
    return render_template("it.html")
@app.route("/it_ques")
def it_ques():
    return render_template("it_ques.html")
@app.route("/kids_ques")
def kids_ques():
    return render_template("kids_ques.html")
@app.route("/musician_ques")
def musician_ques():
    return render_template("musician_ques.html")
@app.route("/musician")
def musician():
    return render_template("musician.html")
@app.route("/senior_ques")
def senior_ques():
    return render_template("senior_ques.html")
@app.route("/senior")
def senior():
    return render_template("senior.html")
@app.route("/services")
def services():
    return render_template("services.html")
@app.route("/ssa")
def ssa():
    return render_template("ssa.html")
@app.route("/start_promodo")
def start_promodo():
    return render_template("start_promodo.html")
@app.route("/teacher_ques")
def teacher_ques():
    return render_template("teacher_ques.html")
@app.route("/teacher")
def teacher():
    return render_template("teacher.html")
@app.route("/unemployed_ques")
def unemployed_ques():
    return render_template("unemployed_ques.html")
@app.route("/unemployed")
def unemployed():
    return render_template("unemployed.html")
@app.route("/stressreduce")
def stressreduce():
    return render_template("stressreduce.html")
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")
@app.route("/goals")
def goals():
    return render_template("goals.html")
@app.route("/settings")
def settings():
    return render_template("settings.html")
if __name__ == "__main__":
    app.run(debug=True)
