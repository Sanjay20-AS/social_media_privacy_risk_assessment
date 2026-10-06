# Social Media Privacy Risk Assessment Framework

A defensive, educational cybersecurity project for assessing **privacy and security exposure** from voluntarily supplied answers about social-media settings and habits.

> **Safety boundary:** This project does not scrape social-media platforms, enumerate accounts, access private profiles, bypass privacy settings, identify real people, or collect private information about real individuals.

## Features

- 0–100 Privacy Risk Score
- Risk levels: LOW, MODERATE, HIGH, CRITICAL
- Category-wise risk scoring
- Explainable rule-based scoring engine
- Detected privacy weaknesses
- Personalized recommendations
- Privacy/security checklist
- PDF report generation
- Synthetic fictional demo profiles
- Unit tests
- Responsive web UI
- Privacy-by-design project documentation

## Risk interpretation

| Score | Level |
|---:|---|
| 0–20 | LOW |
| 21–40 | MODERATE |
| 41–70 | HIGH |
| 71–100 | CRITICAL |

Higher score = higher estimated exposure/risk.

This is an **educational risk framework**, not a guarantee that an account will or will not be compromised.

## Categories

1. Profile visibility
2. Personal-information exposure
3. Contact-information exposure
4. Location exposure
5. Workplace/education exposure
6. Birthday exposure
7. Family/relationship information
8. Post visibility
9. Friend/follower controls
10. Tagging permissions
11. Third-party application access
12. Account authentication
13. MFA usage
14. Password reuse awareness
15. Login alerts
16. Unknown connection requests
17. Suspicious links/messages
18. Photo metadata awareness
19. Historical posts
20. Social-engineering exposure

## Architecture

```text
Browser
   |
   v
Flask Web Application
   |
   +--> Questionnaire
   |
   +--> Risk Engine
   |      +--> weighted rules
   |      +--> category normalization
   |      +--> recommendations
   |
   +--> Results Dashboard
   |
   +--> PDF Report Generator
   |
   +--> Synthetic Demo Dataset
```

## Scoring model

Each answer produces exposure points. The total is normalized:

`score = (observed exposure points / maximum possible exposure points) × 100`

The score is then mapped to the four risk levels.

The rules are intentionally transparent so that a student can explain the methodology during a viva/project review.

## Run locally

### 1. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

Open:

`http://127.0.0.1:5000`

## Run tests

```bash
pytest -q
```

## Safe demonstration workflow

1. Open **Synthetic Demos**.
2. Select a fictional profile.
3. Generate the assessment.
4. Review category scores.
5. Download the PDF report.
6. Modify the synthetic answers or use the questionnaire with non-sensitive demo data.
7. Explain the scoring rules in `risk_engine.py`.

## GitHub structure

```text
social_media_privacy_risk_assessment/
├── app.py
├── risk_engine.py
├── report.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   └── synthetic_profiles.json
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── demo.html
│   └── about.html
├── static/
│   └── style.css
└── tests/
    └── test_risk_engine.py
```

## Security/privacy design decisions

- No external social-media API integration.
- No scraping.
- No credentials.
- No password collection.
- No private messages.
- No account identifiers.
- No real-person profiling.
- Synthetic profiles only for demonstrations.
- Rule-based scoring is explainable and auditable.
- The application states its limitations to avoid presenting risk scores as guarantees.

## Suggested future enhancements

- SQLite persistence for anonymized assessment records.
- Admin dashboard showing only aggregate synthetic/demo statistics.
- CSV/JSON export of anonymous assessment results.
- Configurable scoring rules stored in JSON/YAML.
- OWASP-aligned secure coding checklist.
- Security headers and CSRF protection for production deployment.
- Accessibility improvements.
- Role-based access for a classroom deployment.
- Docker containerization.
- CI pipeline running unit tests.
- Static analysis using Bandit and Ruff.
- Synthetic aggregate analytics using generated data only.

## Disclaimer

This project is intended for cybersecurity education, privacy awareness, and defensive risk assessment. Do not use it to monitor, profile, scrape, enumerate, or investigate real people or accounts.
