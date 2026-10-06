from risk_engine import assess_privacy_risk

def test_low_profile():
    answers = {k:"no" for k in [
        "profile_visibility","personal_info","contact_info","location","work_education",
        "birthday","family_relationships","post_visibility","connection_controls","tagging",
        "third_party_apps","password_reuse","unknown_requests","suspicious_links",
        "historical_posts","social_engineering"
    ]}
    answers.update({"authentication":"yes","mfa":"yes","login_alerts":"yes","photo_metadata":"yes"})
    result = assess_privacy_risk(answers)
    assert 0 <= result["score"] <= 20
    assert result["level"] == "LOW"

def test_high_profile():
    answers = {k:"yes" for k in [
        "profile_visibility","personal_info","contact_info","location","work_education",
        "birthday","family_relationships","post_visibility","connection_controls","tagging",
        "third_party_apps","password_reuse","unknown_requests","suspicious_links",
        "social_engineering"
    ]}
    answers.update({"authentication":"no","mfa":"no","login_alerts":"no","photo_metadata":"no","historical_posts":"no"})
    result = assess_privacy_risk(answers)
    assert result["score"] >= 71
    assert result["level"] == "CRITICAL"

def test_score_bounds():
    result = assess_privacy_risk({})
    assert 0 <= result["score"] <= 100
    assert result["level"] in {"LOW","MODERATE","HIGH","CRITICAL"}
