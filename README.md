# Lead Capture → CRM Automation (Demo)

Every website form submission becomes an enriched lead in the CRM — with an instant Slack alert so sales can follow up in minutes, not days.

## The problem
Leads sit unread in an inbox. By the time someone follows up, the prospect already chose a competitor.

## How it works
1. Visitor submits the website contact form (simulated here with a CSV)
2. Lead data is cleaned and validated (bad emails skipped, duplicates ignored)
3. Lead is added to the CRM (`crm_leads.csv` stands in for HubSpot/Airtable)
4. Instant notification printed for the #sales channel (wire up a real Slack webhook next)
5. Every lead is timestamped so slow follow-ups are easy to spot

## Try it (Python demo)
```bash
python lead_pipeline.py sample_leads.csv
```
Outputs `crm_leads.csv` (your "CRM") and prints the Slack-style alerts.

## No-code version
The same flow builds in ~30 minutes in n8n / Make / Zapier:
Form webhook → data cleanup → HubSpot "create contact" → Slack message.

## Roadmap
- [ ] Real HubSpot API integration
- [ ] Company enrichment (Clearbit-style)
- [ ] Auto-assign leads round-robin to sales reps

*Built while learning automation — feedback welcome!*
