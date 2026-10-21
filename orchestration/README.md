# Aeiloria Agent Handover v0.1 (review proposal)

This is a **connected, evidence-only coordinator**. GitHub Actions schedules session reports, reads commit and open-PR metadata, and appends role-specific relay notes to dated GitHub Issues. **It does not run independent LLM agents, invite people to meetings, or change canon.**

## Schedule (America/Chicago)
- Every day 08:00: morning intake
- Every day 19:00: evening exchange
- Friday 15:00: rotating specialist gathering **agenda**, not a meeting
- Manual Actions > Aeiloria agent handover > Run workflow > session

The workflow lists multiple UTC schedule hours to account for daylight saving changes and checks the actual Chicago hour in the script. GitHub scheduled workflows may be delayed. Reports are deduplicated by date and session marker.

## Evidence and permission boundaries
- Uses GitHub's provided token; no external API key.
- `contents: read`, `pull-requests: read`, `issues: write`.
- Does not write files, merge PRs, run tests, promote canon, or claim anyone attended a gathering.
- Reports are new issue comments and should be treated as audit trail, not canonical source.
- The role paragraphs are **routing placeholders**, not simulated evidence of independently operating agents.

## Connecting real autonomous agents (separate gated phase)
1. Choose and provision a trusted agent runner and its credentials.
2. Give each agent a queue (issue label or assignment), explicit inputs, output schema, limits and least-privilege token.
3. Require machine-verifiable evidence links and human approval on sensitive actions.
4. Keep an append-only event ledger with event IDs, correlation IDs, actor ID, timestamps, input/output hashes, stop states and replay tests.
5. Review prompt-injection, exfiltration, budget and escalation risks before enabling agent write tools.

## Acceptance checks
- Manual run posts exactly one dated issue comment for that session.
- Re-run does not duplicate the session comment.
- Wrong local cron hour makes no issue.
- No edits to `canon/` or direct merges.
- Missing GitHub API permissions fail loudly.
- A new week rotates the gathering subject.
- Verify a live run and comments before claiming production operational.

No canon promotion. No silent rewrite. RED halts actions.
