"""
Lead Capture -> CRM automation demo.
Usage: python lead_pipeline.py sample_leads.csv

Pipeline: form CSV -> validate/clean -> dedupe -> append to CRM (csv)
          -> print Slack-style alert per new lead.

Learning path (TODOs):
  1. Swap crm_leads.csv for real HubSpot / Airtable API calls
  2. Swap print() alerts for a real Slack incoming webhook
  3. Add company enrichment (e.g. Clearbit-style API)
"""

import csv
import os
import re
import sys
from datetime import datetime, timezone

CRM_FILE = "crm_leads.csv"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_lead(row):
    return {
        "name": row.get("name", "").strip(),
        "email": row.get("email", "").strip().lower(),
        "company": row.get("company", "").strip(),
        "message": row.get("message", "").strip(),
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "new",
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python lead_pipeline.py sample_leads.csv")
        sys.exit(1)

    try:
        with open(CRM_FILE, newline="") as f:
            existing = {r["email"].strip().lower() for r in csv.DictReader(f)}
    except FileNotFoundError:
        existing = set()

    new_leads = []
    with open(sys.argv[1], newline="") as f:
        for row in csv.DictReader(f):
            lead = clean_lead(row)
            if not lead["name"] or not EMAIL_RE.match(lead["email"]):
                print(f"SKIP invalid lead: {row}")
                continue
            if lead["email"] in existing:
                print(f"SKIP duplicate: {lead['email']}")
                continue
            existing.add(lead["email"])
            new_leads.append(lead)

    if new_leads:
        write_header = not os.path.exists(CRM_FILE)
        with open(CRM_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=new_leads[0].keys())
            if write_header:
                writer.writeheader()
            writer.writerows(new_leads)

    for lead in new_leads:
        # TODO: replace with a real Slack webhook POST
        print(
            f"[Slack #sales] New lead: {lead['name']} ({lead['company']}) "
            f"<{lead['email']}> - \"{lead['message']}\""
        )

    print(f"Done: {len(new_leads)} new lead(s) added to {CRM_FILE}.")


if __name__ == "__main__":
    main()
