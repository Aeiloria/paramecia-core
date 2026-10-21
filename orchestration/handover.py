#!/usr/bin/env python3
"""Evidence-based role exchange recorded in GitHub Issues; no LLM or canon writes."""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chicago")
ROLES = {
    "Felix.null": "Engine, CI and deterministic execution",
    "Cedar Finch": "Implementation, repair and cross-team dependencies",
    "Veyr Quill": "Canon status, provenance and review gates",
    "Vance": "Consent thresholds and stop conditions",
    "Ash Mercer": "Care, safety and support capacity",
    "Juniper": "Archive integrity, change history and handovers",
    "Bell Lantern": "Welcome, access and community experience",
}
CIRCLES = [
    ("Systems and engineering", ["Felix.null", "Cedar Finch"]),
    ("Canon and worldbuilding", ["Veyr Quill", "Juniper"]),
    ("Consent, thresholds and care", ["Vance", "Ash Mercer"]),
    ("Community and onboarding", ["Bell Lantern", "Juniper"]),
]

def api(method, path, payload=None):
    repo = os.environ["GH_REPOSITORY"]
    url = "https://api.github.com/repos/" + repo + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + os.environ["GH_TOKEN"],
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "aeiloria-handover-v01",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)

def session_at(local, event, requested):
    if event == "workflow_dispatch":
        if requested not in {"morning", "evening", "weekly"}:
            raise ValueError("Invalid session")
        return requested
    if local.weekday() == 4 and local.hour == 15:
        return "weekly"
    if local.hour == 8:
        return "morning"
    if local.hour == 19:
        return "evening"
    return None

def lines_for_changes(commits, pulls):
    recent = ["- " + c["sha"][:9] + ": " + c["commit"]["message"].splitlines()[0] for c in commits[:8]]
    prs = ["- #" + str(p["number"]) + " " + p["title"] + " (" + p["state"] + ")" for p in pulls[:12]]
    return "\n".join(recent) or "- No commits returned", "\n".join(prs) or "- No open PRs returned"

def report(session, local, commits, pulls, previous):
    change_lines, pr_lines = lines_for_changes(commits, pulls)
    marker = "<!-- aeiloria-session:" + local.strftime("%Y-%m-%d") + ":" + session + " -->"
    s = [marker, "# " + session.title() + " evidence handover", "",
         "**Date:** " + local.isoformat(timespec="minutes"),
         "**Status:** YELLOW / evidence review only. No specialist agent execution is asserted.", "",
         "## Repository evidence (read-only)", "**Recent commits**", change_lines,
         "", "**Open pull requests**", pr_lines, "",
         "## Specialist relay"]
    if session == "weekly":
        idx = (local.isocalendar().week - 1) % len(CIRCLES)
        title, team = CIRCLES[idx]
        s += ["**Weekly circle:** " + title, "**Participants proposed:** " + ", ".join(team),
              "Agenda: review prior handover; choose at most 3 decisions; identify blockers; assign review owners.",
              "Meeting status: PROPOSED, not held or attended."]
    for role, mandate in ROLES.items():
        s += ["### " + role, "- Responsibility: " + mandate,
              "- Evidence: repository items above; no direct autonomous action verified.",
              "- Pending: human or connected agent review, with linked evidence before marking GREEN."]
    s += ["", "## Safety and decisions",
          "- 🔴 RED: halt any unauthorized action or consent violation.",
          "- 🟡 YELLOW: open decisions, missing provenance, unverified tests.",
          "- 🟢 GREEN: only after linked evidence and required approval.",
          "- Canon promotion: **never automatic**. No core or canon files changed by this workflow.",
          "", "## Incoming handover", previous or "No earlier handover comment found.",
          "", "## Outgoing handover",
          "- Compare actual changes against current priorities.",
          "- Attach links to completed work and tests.",
          "- Assign an accountable human or connected agent for any action.",
          "- Carry unresolved items forward without silently closing them."]
    return "\n".join(s)

def main():
    now = dt.datetime.now(TZ)
    session = session_at(now, os.environ.get("EVENT_NAME", ""), os.environ.get("REQUESTED_SESSION", ""))
    if not session:
        print("Outside configured local session hours; nothing to do.")
        return
    today = now.date().isoformat()
    issues = api("GET", "/issues?state=open&per_page=100")
    title = "Aeiloria handover | " + today
    issue = next((x for x in issues if x.get("title") == title and "pull_request" not in x), None)
    if not issue:
        issue = api("POST", "/issues", {"title": title, "body":
            "Append-only operational handover for " + today +
            ". This is not a canon source. Evidence and approvals remain external."})
    number = issue["number"]
    comments = api("GET", "/issues/" + str(number) + "/comments?per_page=100")
    marker = "<!-- aeiloria-session:" + today + ":" + session + " -->"
    if any(marker in x.get("body", "") for x in comments):
        print("Already recorded:", session, today)
        return
    last = next((c["body"] for c in reversed(comments) if "aeiloria-session:" in c.get("body", "")), "")
    previous = ("Previous recorded session: " + last.splitlines()[1][:160]) if last else ""
    since = urllib.parse.quote((now - dt.timedelta(days=2)).astimezone(dt.timezone.utc).isoformat())
    commits = api("GET", "/commits?since=" + since + "&per_page=20")
    pulls = api("GET", "/pulls?state=open&per_page=30")
    body = report(session, now, commits, pulls, previous)
    api("POST", "/issues/" + str(number) + "/comments", {"body": body})
    print("Recorded", session, "at issue", number)

if __name__ == "__main__":
    try:
        main()
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, KeyError) as exc:
        print("Handover failed:", str(exc), file=sys.stderr)
        sys.exit(1)
