#!/usr/bin/env python3
"""
Morning standup assistant — Claude-powered daily briefing.

Paste your weekly schedule and priorities into the variables below, then run:
    python morning_standup.py

Requires: pip install anthropic
"""

from __future__ import annotations

import sys
from datetime import datetime

import anthropic

# -----------------------------------------------------------------------------
# API configuration
# -----------------------------------------------------------------------------
# Paste your Anthropic API key here, or set the ANTHROPIC_API_KEY environment
# variable and leave this string empty to read from the environment.

ANTHROPIC_API_KEY = "ANTHROPIC_API_KEY_REMOVED"

# -----------------------------------------------------------------------------
# Master life architecture context — updated weekly as situation evolves
# -----------------------------------------------------------------------------
MASTER_CONTEXT = """
DAVID YETI — LIFE ARCHITECTURE CONTEXT
Updated: May 2026

THE DESTINATION: QLA Green Light + Securtopia Independence.
Filter for every decision: does this move me closer to independence?

THREE YEAR RULE: Cisco outer boundary May 2027. Exit on your terms not theirs.

CISCO SITUATION: SDR Grade 6. Base $80,500. OTE $107,333.
Layoffs hit May 14 — survived. Six AI/Security engineering roles posted internally closing June 12-14.
PRIMARY TARGET: AI Security Engineer under Domenica Casale.
SECONDARY TARGET: Security Engineer in S&TO under Wilson Mendez.
DECISION: If no internal promotion by Vegas August 23 — exit Cisco September 2026.

INCOME PATHS:
Path A (internal): Cisco AI Security Engineer $105K + J2 async $70K + Securtopia $10K = $185K
Path B (external): Compliance Engineer $90K + J2 async $70K + Securtopia $10K = $170K
Both paths lead to the same destination. Let the market decide which vehicle.

CISA EXAM: June 5, 2026. 19 days away. 30 questions every morning without exception.
This credential unlocks J2 and changes the market response the day it passes.

GITHUB PORTFOLIO: github.com/DavidYeti/ai-governance-toolkit
Project 1: ISO 42001 Control Checker — LIVE
Project 2: AI Tool Intake Form Automation — LIVE
Project 3: Morning Standup Bot — IN PROGRESS
Show Joe Buchanan these projects at 10AM Monday.

THIS WEEK'S CRITICAL MEETINGS:
Monday 10AM: Joe Buchanan — SE Director — show GitHub, ask about Domenica connection
Monday 2:30PM: Brian — stretch assignment professional close — thank him, ask for portal access
Tuesday: Devin Patterson — mentor — get feedback on GitHub before hiring manager meetings

SECURTOPIA: First client not yet landed. No-cost actions available now.
Capability statement, TerraVault case studies, pricing doc, MetLife contract — build this week.

QLA GREEN LIGHT STATUS: ~$5,500/month today. Target $15K/month from J1+J2+J3.
Emergency fund: $18K Fidelity SPAXX. Target $5K Phase 1 from FedEx income.
Credit: In repair. Collection letters sent. Target 720+.

GSU: ACCEPTED. Fall 2026 semester. REPP program. Tuition reimbursement through Cisco.

BOOK: COMPLETE. All chapters done including family bonus section.

STANDING NON-NEGOTIABLES:
1. CISA 30 questions first every morning — 7 days a week
2. Check and action J2 applications
3. One Securtopia deliverable
4. Protect family evening check-ins for 30 minutes every evening
5. Once summer starts, on May 22nd work from cisco office every monday - friday 9:00AM - 4:00PM
6. Sunday = 3 hours of uninterrupted family time
7. Once Securtopia is live, submit two proposals per day for government contracts
"""

# -----------------------------------------------------------------------------
# Weekly inputs — update these at the start of each week
# -----------------------------------------------------------------------------

# Plain-text schedule for the whole week. Organize by day; include times and
# context that help Claude understand what matters (meetings, deadlines, travel).
# Example format:
#   Monday
#   9:00 AM — Team standup
#   2:00 PM — Budget review
#   Tuesday
#   ...

WEEKLY_SCHEDULE = """
Monday
10:00 AM — Joe Buchanan meeting — Solutions Engineering Director — show GitHub AI governance projects
2:30 PM — Brian meeting — stretch assignment close — 15 minutes — thank him and ask about portal access

Tuesday
Time TBD — Devin Patterson meeting — butterfly mentorship — show ISO 42001 gap assessment tool

Wednesday through Friday
TBD — CISA study, J2 applications, Securtopia build
"""

# Your top three focus outcomes for the week (order matters: #1 is highest).
WEEKLY_PRIORITIES = [
    "CISA 30 questions every morning — exam June 5 is 19 days away",
    "AI security engineer campaign — message Domenica Casale and Wilson Mendez Monday",
    "Close Brian meeting professionally — keep Surya relationship active",
]

# Short statements you believe in; Claude picks one that fits today's tone.
PERSONAL_MANTRAS = [
    "Protect the morning — that's when the real work happens.",
    "Family time is not negotiable; everything else bends around it.",
    "Done beats perfect when the stakes are learning, not production.",
]

# -----------------------------------------------------------------------------
# Day selection
# -----------------------------------------------------------------------------
# None = use today's weekday automatically (recommended).
# Or set explicitly, e.g. "Monday", "Tuesday", … to preview another day's briefing.

TARGET_DAY: str | None = None

# -----------------------------------------------------------------------------
# Standing daily non-negotiables (same every day)
# -----------------------------------------------------------------------------

STANDING_NON_NEGOTIABLES = [
    "CISA 30 questions first every morning",
    "Check J2 applications",
    "Complete one Securtopia task",
    "Protect family evening time",
]

CLAUDE_MODEL = "claude-sonnet-4-5"
MAX_OUTPUT_TOKENS = 1200


def resolve_briefing_day(target_day: str | None) -> str:
    """Return the weekday name to brief on (auto-detect or override)."""
    if target_day is None:
        return datetime.now().strftime("%A")
    normalized = target_day.strip().title()
    valid = {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    }
    if normalized not in valid:
        print(
            f"Invalid TARGET_DAY '{target_day}'. "
            f"Use a full weekday name or None for today.",
            file=sys.stderr,
        )
        sys.exit(1)
    return normalized


def build_briefing_prompt(
    briefing_day: str,
    master_context: str,
    weekly_schedule: str,
    weekly_priorities: list[str],
    personal_mantras: list[str],
    non_negotiables: list[str],
) -> str:
    """Assemble context for Claude into a single user message."""
    priorities_block = "\n".join(
        f"  {index}. {item}" for index, item in enumerate(weekly_priorities, start=1)
    )
    mantras_block = "\n".join(f"  - {m}" for m in personal_mantras)
    non_negotiables_block = "\n".join(f"  - {n}" for n in non_negotiables)

    return f"""--- LIFE ARCHITECTURE CONTEXT ---
{master_context.strip()}

You are my trusted morning advisor. Today is {briefing_day}.

Write a personalized morning briefing for me in connected prose — warm, direct, and specific. Speak to me as "you." Do not use bullet lists or markdown headers. Do not dump the whole week's calendar; focus only on what matters for {briefing_day} and how it connects to the week. Use the life architecture context above so your advice reflects my full situation — career goals, deadlines, and constraints — not just today's calendar.

Include, woven naturally into the narrative:
1. A warm, direct greeting.
2. Today's priority events and commitments from my weekly schedule (only {briefing_day}).
3. A clear recommendation for how to structure the day — what to protect, what to sequence, and why, based on what is most important today.
4. A reminder of my weekly priorities (all three) and how today's work should advance them.
5. My standing daily non-negotiables.
6. Exactly one personal mantra from my list — choose the one that best fits today's tone and challenges; weave it in naturally at the end.

Think for me: tell me what actually matters today and why, not just what is on the calendar.

--- WEEKLY SCHEDULE (all days; extract only {briefing_day}) ---
{weekly_schedule.strip()}

--- WEEKLY PRIORITIES ---
{priorities_block}

--- PERSONAL MANTRAS (choose one) ---
{mantras_block}

--- STANDING DAILY NON-NEGOTIABLES ---
{non_negotiables_block}
"""


def generate_morning_briefing(prompt: str, api_key: str) -> str:
    """Call Claude and return the briefing text."""
    client = anthropic.Anthropic(api_key=api_key or None)
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main() -> None:
    api_key = ANTHROPIC_API_KEY.strip()
    if not api_key:
        import os

        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print(
            "Set ANTHROPIC_API_KEY at the top of morning_standup.py "
            "or export ANTHROPIC_API_KEY in your environment.",
            file=sys.stderr,
        )
        sys.exit(1)

    briefing_day = resolve_briefing_day(TARGET_DAY)
    prompt = build_briefing_prompt(
        briefing_day=briefing_day,
        master_context=MASTER_CONTEXT,
        weekly_schedule=WEEKLY_SCHEDULE,
        weekly_priorities=WEEKLY_PRIORITIES,
        personal_mantras=PERSONAL_MANTRAS,
        non_negotiables=STANDING_NON_NEGOTIABLES,
    )

    print(f"Generating morning briefing for {briefing_day}...\n")
    briefing = generate_morning_briefing(prompt, api_key)
    print(briefing)


if __name__ == "__main__":
    main()
