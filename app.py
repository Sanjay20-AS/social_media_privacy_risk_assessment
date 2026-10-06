from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from risk_engine import assess_privacy_risk
from report import build_report
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = "development-only-secret-change-me"

QUESTIONS = [
    {"id":"profile_visibility","category":"Profile Visibility","question":"Is your social-media profile publicly visible to anyone?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"personal_info","category":"Personal Information","question":"Do you publicly display your full name plus other identifying personal details?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"contact_info","category":"Contact Information","question":"Are your personal phone number or personal email publicly visible?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"location","category":"Location Exposure","question":"Do you regularly publish your current or routine locations?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"work_education","category":"Work / Education","question":"Do you publicly expose detailed workplace, school, class, or schedule information?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"birthday","category":"Birthday Exposure","question":"Is your full date of birth publicly visible?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"family_relationships","category":"Family / Relationships","question":"Do you publicly expose family members, relationship status, or household details?","type":"choice","options":[("yes","No restrictions"),("no","Limited"),("unknown","Not sure")]},
    {"id":"post_visibility","category":"Post Visibility","question":"Are most of your posts visible to a broad/public audience?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"connection_controls","category":"Friend / Follower Controls","question":"Do you accept connection/follower requests from people you do not know?","type":"choice","options":[("yes","Often"),("no","Rarely/Never"),("unknown","Not sure")]},
    {"id":"tagging","category":"Tagging Permissions","question":"Can other users tag or mention you without review/approval?","type":"choice","options":[("yes","Yes"),("no","No / review first"),("unknown","Not sure")]},
    {"id":"third_party_apps","category":"Third-Party App Access","question":"Do you have old or unnecessary third-party apps connected to your account?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"authentication","category":"Account Authentication","question":"Do you use a unique strong password for the account?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"mfa","category":"MFA","question":"Is multi-factor authentication enabled?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"password_reuse","category":"Password Reuse Awareness","question":"Do you reuse the same password across multiple services?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"login_alerts","category":"Login Alerts","question":"Are login/security alerts enabled?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"unknown_requests","category":"Unknown Connections","question":"Do you interact with or accept requests from unknown accounts?","type":"choice","options":[("yes","Often"),("no","Rarely/Never"),("unknown","Not sure")]},
    {"id":"suspicious_links","category":"Suspicious Links / Messages","question":"Would you click unexpected links/messages before verifying the sender?","type":"choice","options":[("yes","Possibly/Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"photo_metadata","category":"Photo Metadata Awareness","question":"Do you understand that photos/files can contain metadata such as location/device information?","type":"choice","options":[("yes","I understand and manage it"),("no","I do not manage it"),("unknown","Not sure")]},
    {"id":"historical_posts","category":"Historical Posts","question":"Have you reviewed or removed old posts that reveal sensitive information?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
    {"id":"social_engineering","category":"Social Engineering Exposure","question":"Could public information about you reveal answers to security questions, routines, or likely passwords?","type":"choice","options":[("yes","Yes"),("no","No"),("unknown","Not sure")]},
]

@app.route("/")
def index():
    return render_template("index.html", questions=QUESTIONS)

@app.post("/assess")
def assess():
    answers = {q["id"]: request.form.get(q["id"], "unknown") for q in QUESTIONS}
    result = assess_privacy_risk(answers)
    session["result"] = result
    session["answers"] = answers
    return render_template("results.html", result=result, generated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))

@app.get("/demo")
def demo():
    demo_path = Path("data/synthetic_profiles.json")
    profiles = json.loads(demo_path.read_text(encoding="utf-8"))
    return render_template("demo.html", profiles=profiles)

@app.post("/demo/<profile_id>")
def demo_assess(profile_id):
    profiles = json.loads(Path("data/synthetic_profiles.json").read_text(encoding="utf-8"))
    profile = next((p for p in profiles if p["id"] == profile_id), None)
    if not profile:
        flash("Synthetic profile not found.")
        return redirect(url_for("demo"))
    result = assess_privacy_risk(profile["answers"])
    session["result"] = result
    return render_template("results.html", result=result, generated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))

@app.get("/report")
def report():
    result = session.get("result")
    if not result:
        return redirect(url_for("index"))
    pdf_path = build_report(result)
    return send_file(pdf_path, as_attachment=True, download_name="privacy-risk-report.pdf")

@app.get("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
