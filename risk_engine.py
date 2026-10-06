"""
Defensive, transparent risk-scoring engine.

The engine never identifies people, searches social media, scrapes accounts,
or accesses external services. It only evaluates voluntarily supplied answers.
Higher scores mean higher privacy/security exposure.
"""

CATEGORIES = {
    "Profile Visibility": ["profile_visibility", "post_visibility"],
    "Personal Information": ["personal_info", "birthday", "family_relationships"],
    "Contact / Location Exposure": ["contact_info", "location", "work_education"],
    "Social Graph Controls": ["connection_controls", "tagging", "unknown_requests"],
    "Application Access": ["third_party_apps"],
    "Authentication": ["authentication", "mfa", "password_reuse", "login_alerts"],
    "Threat Awareness": ["suspicious_links", "photo_metadata", "historical_posts", "social_engineering"],
}

# Per-answer exposure points. The scoring deliberately rewards safer settings.
RULES = {
    "profile_visibility": {"yes": 7, "no": 0, "unknown": 4},
    "personal_info": {"yes": 6, "no": 0, "unknown": 3},
    "contact_info": {"yes": 7, "no": 0, "unknown": 3},
    "location": {"yes": 7, "no": 0, "unknown": 3},
    "work_education": {"yes": 5, "no": 0, "unknown": 2},
    "birthday": {"yes": 4, "no": 0, "unknown": 2},
    "family_relationships": {"yes": 5, "no": 0, "unknown": 2},
    "post_visibility": {"yes": 6, "no": 0, "unknown": 3},
    "connection_controls": {"yes": 5, "no": 0, "unknown": 2},
    "tagging": {"yes": 4, "no": 0, "unknown": 2},
    "third_party_apps": {"yes": 6, "no": 0, "unknown": 3},
    "authentication": {"yes": 0, "no": 7, "unknown": 4},
    "mfa": {"yes": 0, "no": 8, "unknown": 4},
    "password_reuse": {"yes": 7, "no": 0, "unknown": 3},
    "login_alerts": {"yes": 0, "no": 4, "unknown": 2},
    "unknown_requests": {"yes": 5, "no": 0, "unknown": 2},
    "suspicious_links": {"yes": 6, "no": 0, "unknown": 3},
    "photo_metadata": {"yes": 0, "no": 4, "unknown": 2},
    "historical_posts": {"yes": 4, "no": 0, "unknown": 2},
    "social_engineering": {"yes": 6, "no": 0, "unknown": 3},
}

RECOMMENDATIONS = {
    "profile_visibility": "Review profile visibility and use the narrowest audience that still meets your needs.",
    "personal_info": "Remove unnecessary identifiers and avoid publishing information that can be combined for impersonation.",
    "contact_info": "Keep personal phone numbers and email addresses out of public profile fields where possible.",
    "location": "Avoid posting real-time locations, recurring routines, or future travel plans publicly.",
    "work_education": "Share only the level of workplace/school detail needed for your purpose.",
    "birthday": "Hide your full date of birth; consider limiting birthday information to trusted contacts.",
    "family_relationships": "Reduce public exposure of family, household, and relationship details.",
    "post_visibility": "Audit audience settings and prefer limited audiences for posts containing personal context.",
    "connection_controls": "Restrict who can send requests or follow you and review unfamiliar connections.",
    "tagging": "Enable tag/mention review and restrict who can tag or mention you.",
    "third_party_apps": "Review connected applications and revoke access that is old, unused, or unnecessary.",
    "authentication": "Use a unique, long password/passphrase and store it in a reputable password manager.",
    "mfa": "Enable MFA, preferably using an authenticator app or passkey when supported.",
    "password_reuse": "Stop reusing passwords and use unique credentials for every important service.",
    "login_alerts": "Enable login alerts and review security notifications promptly.",
    "unknown_requests": "Treat unexpected connection requests as untrusted until independently verified.",
    "suspicious_links": "Verify unexpected links through a separate trusted channel before opening them.",
    "photo_metadata": "Review photo/file metadata settings and remove sensitive metadata before public sharing when appropriate.",
    "historical_posts": "Perform a historical-post audit and remove or restrict old sensitive content.",
    "social_engineering": "Avoid exposing routines, security-question answers, recovery clues, or highly predictable personal details.",
}

def level_for(score):
    if score <= 20:
        return "LOW"
    if score <= 40:
        return "MODERATE"
    if score <= 70:
        return "HIGH"
    return "CRITICAL"

def assess_privacy_risk(answers):
    raw = {}
    total = 0
    for key, mapping in RULES.items():
        value = answers.get(key, "unknown")
        points = mapping.get(value, mapping["unknown"])
        raw[key] = points
        total += points

    max_score = sum(max(v.values()) for v in RULES.values())
    score = round((total / max_score) * 100)
    score = max(0, min(100, score))

    category_scores = {}
    category_max = {}
    for category, keys in CATEGORIES.items():
        current = sum(raw[k] for k in keys)
        maximum = sum(max(RULES[k].values()) for k in keys)
        category_scores[category] = round((current / maximum) * 100) if maximum else 0
        category_max[category] = maximum

    weaknesses = []
    recommendations = []
    for key, points in raw.items():
        if points >= max(RULES[key].values()) * 0.55:
            weaknesses.append({
                "control": key.replace("_", " ").title(),
                "exposure_points": points,
                "message": RECOMMENDATIONS[key]
            })
            recommendations.append(RECOMMENDATIONS[key])

    # Prioritize high-impact recommendations while keeping the report readable.
    recommendations = list(dict.fromkeys(recommendations))
    checklist = [
        ("Profile audience reviewed", "Review who can see your profile and posts."),
        ("Contact details minimized", "Remove public personal phone/email where unnecessary."),
        ("Location sharing reduced", "Avoid real-time location and routine exposure."),
        ("Tags/mentions controlled", "Enable approval/review before tags appear."),
        ("Connected apps audited", "Remove unused third-party access."),
        ("Unique password used", "Use a unique password/passphrase."),
        ("MFA enabled", "Enable multi-factor authentication or a passkey."),
        ("Login alerts enabled", "Turn on alerts for new/unusual sign-ins."),
        ("Historical posts audited", "Review older posts for sensitive exposure."),
        ("Phishing awareness practiced", "Verify unexpected links/messages before interacting."),
        ("Photo metadata considered", "Check whether shared media contains sensitive metadata."),
        ("Social-engineering clues minimized", "Avoid public recovery clues and predictable personal details."),
    ]

    return {
        "score": score,
        "level": level_for(score),
        "category_scores": category_scores,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "checklist": checklist,
        "methodology": {
            "answer_count": len(RULES),
            "maximum_raw_points": max_score,
            "formula": "Normalized weighted exposure points: (observed points / maximum points) × 100",
            "interpretation": "Higher score = higher estimated privacy/security exposure."
        }
    }
