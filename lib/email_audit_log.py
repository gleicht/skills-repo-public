#!/usr/bin/env python3
"""Email a book's audit log on demand.

Reads `audit-log.md` from a book folder and emails it via SMTP. On-demand only — run it
when you want the report sent (e.g., "email me the audit log"). Standard library only
(smtplib), so it works with any SMTP provider; a personal Gmail with an app password is
the easiest.

Credentials are read from (env vars override the file):
  - env: AUDIT_SMTP_HOST, AUDIT_SMTP_PORT, AUDIT_SMTP_USER, AUDIT_SMTP_PASS,
         AUDIT_EMAIL_FROM, AUDIT_EMAIL_TO
  - or a JSON file: lib/email_config.json  (gitignored — never committed)
    { "smtp_host": "smtp.gmail.com", "smtp_port": 587,
      "smtp_user": "you@gmail.com", "smtp_pass": "<app password>",
      "email_from": "you@gmail.com", "email_to": "you@example.com" }

Usage:
    python email_audit_log.py --book <folder> [--to addr] [--latest] [--dry-run]

  --book      folder containing audit-log.md (default: current dir)
  --to        recipient (overrides config email_to)
  --subject   custom subject
  --latest    send only the most recent run entry, not the whole log
  --dry-run   compose and print the email; do NOT connect or send (no creds needed)
"""

import argparse
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime
from email.message import EmailMessage

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    cfg = {}
    path = os.path.join(HERE, "email_config.json")
    if os.path.isfile(path):
        try:
            cfg = json.loads(open(path, encoding="utf-8").read())
        except ValueError:
            print("warning: email_config.json is not valid JSON; ignoring", file=sys.stderr)
    env = {
        "smtp_host": os.environ.get("AUDIT_SMTP_HOST"),
        "smtp_port": os.environ.get("AUDIT_SMTP_PORT"),
        "smtp_user": os.environ.get("AUDIT_SMTP_USER"),
        "smtp_pass": os.environ.get("AUDIT_SMTP_PASS"),
        "email_from": os.environ.get("AUDIT_EMAIL_FROM"),
        "email_to": os.environ.get("AUDIT_EMAIL_TO"),
    }
    for k, v in env.items():
        if v:
            cfg[k] = v
    return cfg


def latest_entry(text):
    parts = text.split("\n## ")
    if len(parts) <= 1:
        return text
    return "## " + parts[-1]


def main():
    ap = argparse.ArgumentParser(description="Email a book's audit log on demand.")
    ap.add_argument("--book", default=".")
    ap.add_argument("--to", default=None)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    book = os.path.abspath(args.book)
    log_path = os.path.join(book, "audit-log.md")
    if not os.path.isfile(log_path):
        print(f"error: no audit-log.md in {book}", file=sys.stderr)
        return 2
    body = open(log_path, encoding="utf-8").read()
    if args.latest:
        body = latest_entry(body)

    cfg = load_config()
    to_addr = args.to or cfg.get("email_to")
    subject = args.subject or (f"Audit log — {os.path.basename(book)} — "
                               f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")

    msg = EmailMessage()
    msg["From"] = cfg.get("email_from") or cfg.get("smtp_user") or "book-machine"
    msg["To"] = to_addr or "(unset)"
    msg["Subject"] = subject
    msg.set_content(body)

    if args.dry_run:
        print("--- DRY RUN (not sent) ---")
        print(f"From: {msg['From']}\nTo: {msg['To']}\nSubject: {msg['Subject']}")
        print("--- body (first 25 lines) ---")
        print("\n".join(body.splitlines()[:25]))
        print(f"--- [{len(body)} chars total] ---")
        return 0

    missing = [k for k in ("smtp_host", "smtp_port", "smtp_user", "smtp_pass") if not cfg.get(k)]
    if missing or not to_addr:
        print("error: email not configured. Create lib/email_config.json (see "
              "email_config.example.json) or set the AUDIT_SMTP_* env vars. "
              f"Missing: {', '.join(missing + ([] if to_addr else ['recipient']))}",
              file=sys.stderr)
        return 2

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(cfg["smtp_host"], int(cfg["smtp_port"]), timeout=30) as s:
            s.starttls(context=ctx)
            s.login(cfg["smtp_user"], cfg["smtp_pass"])
            s.send_message(msg)
    except Exception as e:
        print(f"error: send failed: {e}", file=sys.stderr)
        return 1

    print(f"audit log emailed to {to_addr} ({len(body)} chars).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
