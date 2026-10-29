# 📧 Inbox Cleaner — Smart Gmail Cleanup Tool (Python)

A Python tool that scans your exported email list and automatically finds **bekar (useless) emails** — promotions, offers, expired OTPs, old newsletters and 1-year-old unread junk — then generates a clean cleanup report. Inspired by a real cleanup of **650+ emails**.

## ✨ Features
- 🏷️ **Auto-classification**: Promotions, Used/Expired OTP, Newsletter, Old Unread, Finance, College, Jobs
- 🛡️ **Protection rules**: Bank statements, fee receipts, college & job mails are never marked for deletion
- 📊 **Markdown report**: Category-wise count + full list of delete candidates
- 🔒 **Safe by design**: Only reports — never deletes anything itself (dry-run philosophy)
- ⚡ No external libraries needed — pure Python 3

## 🚀 Usage
```bash
# 1. Export / prepare a CSV with columns: sender,subject,date,read
#    (sample_emails.csv included as demo)

# 2. Run the cleaner
python inbox_cleaner.py sample_emails.csv

# 3. Custom output file
python inbox_cleaner.py sample_emails.csv --out my_report.md
```

## 📂 Sample Output
```
Category        Count  Action
--------------  -----  --------
PROMOTION          4   DELETE
USED_OTP           2   DELETE
OLD_UNREAD         1   DELETE
FINANCE            2   KEEP (protected)
COLLEGE            1   KEEP (protected)
```

## 🧠 Classification Logic (priority order)
1. **Protected** — bank/payment/statement/invoice, college/admission, job/internship keywords → KEEP
2. **Used OTP** — OTP/verification-code mails older than 1 day → DELETE (OTP sirf minutes valid hota hai!)
3. **Promotion** — sale/offer/discount/contest keywords → DELETE
4. **Old Unread** — unread & older than 365 days → DELETE
5. **Newsletter** — digest/newsletter & unread & older than 180 days → DELETE
6. Everything else → KEEP

## 📁 Project Structure
```
inbox-cleaner-python/
├── inbox_cleaner.py   # main script
├── sample_emails.csv  # demo data
└── README.md
```

## 👨‍💻 Author
**Tanish Chauhan** — MCA @ ABES Engineering College
