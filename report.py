from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from pathlib import Path
from datetime import datetime
import tempfile

def build_report(result):
    path = Path(tempfile.gettempdir()) / "privacy-risk-report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    styles["Title"].alignment = TA_CENTER
    story = [
        Paragraph("Social Media Privacy Risk Assessment", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"<b>Privacy Risk Score:</b> {result['score']}/100", styles["Heading2"]),
        Paragraph(f"<b>Risk Level:</b> {result['level']}", styles["Heading2"]),
        Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]),
        Spacer(1, 16),
        Paragraph("Category Scores", styles["Heading2"]),
    ]
    data = [["Category", "Score"]]
    data += [[k, f"{v}/100"] for k, v in result["category_scores"].items()]
    table = Table(data, colWidths=[330, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#172033")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("PADDING",(0,0),(-1,-1),7),
    ]))
    story += [table, Spacer(1, 16), Paragraph("Detected Weaknesses", styles["Heading2"])]
    if result["weaknesses"]:
        for w in result["weaknesses"]:
            story.append(Paragraph(f"<b>{w['control']}</b> — {w['message']}", styles["BodyText"]))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No high-impact weaknesses were detected by this educational rule set.", styles["BodyText"]))
    story += [Spacer(1, 12), Paragraph("Recommendations", styles["Heading2"])]
    for rec in result["recommendations"]:
        story.append(Paragraph("• " + rec, styles["BodyText"]))
        story.append(Spacer(1, 4))
    story += [
        Spacer(1, 12),
        Paragraph("Important limitation", styles["Heading2"]),
        Paragraph("This is an educational privacy-risk framework. It does not access, scan, scrape, enumerate, identify, or track real social-media accounts. A high score indicates higher estimated exposure under the selected rules; it is not a guarantee that an account will be compromised, nor a guarantee that a low score is completely safe.", styles["BodyText"])
    ]
    doc.build(story)
    return str(path)
