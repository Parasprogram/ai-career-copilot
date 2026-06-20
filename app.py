from flask import Flask, render_template, request, redirect, session
from sqlalchemy import inspect, text

from db import engine, Base, SessionLocal
import models
import PyPDF2
import docx
import json
from ai import analyze_resume

app = Flask(__name__, template_folder="template", static_folder="static")
app.secret_key="secret@12345"

Base.metadata.create_all(bind=engine)

def init_db():
    models.Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "reports" in inspector.get_table_names():
        report_columns = {column["name"] for column in inspector.get_columns("reports")}
        if "file_name" not in report_columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE reports ADD COLUMN file_name VARCHAR(255) NULL"))
        if "goal" not in report_columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE reports ADD COLUMN goal VARCHAR(255) NULL"))


init_db()

@app.route("/")

def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    db=SessionLocal()
    
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        
        existing_user=db.query(models.User).filter_by(email=email).first()
        if existing_user:
            return "User already exists."
        
        user=models.User(email=email, password=password)
        db.add(user)
        db.commit()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    db=SessionLocal()
    
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        
        user=db.query(models.User).filter_by(email=email, password=password).first()
        if user:
            session["user"]=user.email
            return redirect("/dashboard")
        else:
            return "Invalid credentials."
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    result=None
    
    if request.method=="POST":
        user_goal=request.form.get("goal")
        resume_text=request.form.get("resume")
        
        file = request.files.get("file")
        
        # file handling
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    return f"Error processing PDF: {str(e)}"
            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    return f"Error processing DOCX: {str(e)}"
            
        if resume_text and user_goal:
            try:
                result=analyze_resume(resume_text, user_goal)
                
                #save to db
                db = SessionLocal()
                user=db.query(models.User).filter_by(email=session["user"]).first()
                
                report=models.Report(
                    user_id=user.id,
                    goal=user_goal,
                    resume_text=resume_text,
                    result=json.dumps(result)
                )     
                
                db.add(report)
                db.commit()
            except Exception as e:
                return f"AI Error: {str(e)}"

        return render_template(
            "dashboard.html",
            user=session["user"],
            result=result
        )

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )

@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db=SessionLocal()
    user=db.query(models.User).filter_by(email=session["user"]).first()
    
    reports=db.query(models.Report).filter_by(user_id=user.id).all()
    
    # convert result from json string to dict
    for report in reports:
        try:
            report.parsed_result = json.loads(report.result)
        except json.JSONDecodeError:
            report.parsed_result = []

    return render_template("history.html", reports=reports)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__=="__main__":
    init_db()
    app.run(debug=True)