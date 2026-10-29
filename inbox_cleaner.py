#!/usr/bin/env python3
"""
Inbox Cleaner - Smart Email Cleanup Tool
-----------------------------------------
Scans a CSV of emails (sender, subject, date, read) and classifies each mail:
DELETE candidates  -> promotions, used/expired OTPs, old newsletters, 1yr+ old unread
PROTECTED (KEEP)   -> finance, college, job mails (kabhi delete nahi honge)

Usage:
    python inbox_cleaner.py sample_emails.csv [--out report.md]
"""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime

PROTECTED = {
    "FINANCE": ["bank", "statement", "payment", "invoice", "fee receipt", "upi", "refund", "transaction"],
    "COLLEGE": ["abes", "admission", "college", "uptac", "university", "exam", "semester"],
    "JOBS":    ["job alert", "internship", "placement", "hiring", "interview"],
}
PROMO_WORDS = ["sale", "offer", "% off", "discount", "coupon", "deal", "contest", "win", "free gift", "hurry", "last chance"]
OTP_WORDS = ["otp", "verification code", "one time password", "one-time password"]
NEWSLETTER_WORDS = ["newsletter", "digest", "weekly update", "unsubscribe"]


def age_days(date_str: str) -> int:
    try:
        d = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return 0
    return (datetime.now().date() - d).days


def classify(row: dict) -> tuple[str, str]:
    """Return (category, action) where action is KEEP or DELETE."""
    text = f"{row.get('sender','')} {row.get('subject','')}".lower()
    unread = row.get("read", "yes").strip().lower() in ("no", "unread", "false")
    age = age_days(row.get("date", ""))

    # 1) Protected categories first - ye kabhi delete nahi honge
    for cat, words in PROTECTED.items():
        if any(w in text for w in words) and not any(o in text for o in OTP_WORDS):
            return cat, "KEEP"

    # 2) Used / expired OTP (OTP minutes mein expire ho jata hai)
    if any(o in text for o in OTP_WORDS) and age > 1:
        return "USED_OTP", "DELETE"

    # 3) Promotions & offers
    if any(p in text for p in PROMO_WORDS):
        return "PROMOTION", "DELETE"

    # 4) 1 saal se purane unread mails
    if unread and age > 365:
        return "OLD_UNREAD", "DELETE"

    # 5) Purane unread newsletters
    if any(n in text for n in NEWSLETTER_WORDS) and unread and age > 180:
        return "NEWSLETTER", "DELETE"

    return "PERSONAL", "KEEP"


def main() -> None:
    ap = argparse.ArgumentParser(description="Inbox Cleaner - bekar email finder")
    ap.add_argument("csv_file", help="CSV with columns: sender,subject,date,read")
    ap.add_argument("--out", default="cleanup_report.md", help="Output report file")
    args = ap.parse_args()

    with open(args.csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    groups: dict[str, list] = defaultdict(list)
    counts: Counter = Counter()
    for r in rows:
        cat, action = classify(r)
        groups[action].append((cat, r))
        counts[(cat, action)] += 1

    lines = ["# 📧 Inbox Cleanup Report\n",
             f"Total emails scanned: **{len(rows)}**\n",
             "| Category | Count | Action |", "|---|---|---|"]
    for (cat, action), n in sorted(counts.items()):
        lines.append(f"| {cat} | {n} | {action} |")

    lines.append("\n## 🗑️ Delete Candidates\n")
    for cat, r in groups.get("DELETE", []):
        lines.append(f"- [{cat}] **{r.get('subject','')}** — {r.get('sender','')} ({r.get('date','')})")

    lines.append("\n## 🛡️ Protected / Kept\n")
    for cat, r in groups.get("KEEP", []):
        lines.append(f"- [{cat}] **{r.get('subject','')}** — {r.get('sender','')} ({r.get('date','')})")

    report = "\n".join(lines) + "\n"
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    delete_n = sum(n for (_, a), n in counts.items() if a == "DELETE")
    print(report)
    print(f"✅ Report saved to {args.out} | Delete candidates: {delete_n}/{len(rows)}")


if __name__ == "__main__":
    main()
