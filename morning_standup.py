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

from dotenv import load_dotenv
load_dotenv()

# -----------------------------------------------------------------------------
# API configuration
# -----------------------------------------------------------------------------
# Paste your Anthropic API key here, or set the ANTHROPIC_API_KEY environment
# variable and leave this string empty to read from the environment.

ANTHROPIC_API_KEY = ""

# -----------------------------------------------------------------------------
# Master life architecture context — updated weekly as situation evolves
# -----------------------------------------------------------------------------
MASTER_CONTEXT = """

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


# Your top three focus outcomes for the week (order matters: #1 is highest).
WEEKLY_PRIORITIES = [
 ,
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
   ,
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

Write a concise morning briefing for me. Maximum 250 words. Use short paragraphs of 2-3 sentences each. Be direct and specific. No fluff, no repetition, no long explanations. Structure it exactly like this:

ONE sentence greeting tied to today's biggest priority.

TODAY — 2-3 sentences on what matters most today and why.

THIS WEEK — 2-3 sentences on the weekly priorities and how today connects.

NON-NEGOTIABLES — One line each for the standing daily commitments.

MANTRA — One sentence. The most relevant personal mantra for today.

That is it. Nothing else. Tight, actionable, direct.

Use the life architecture context above so your advice reflects my full situation — career goals, deadlines, and constraints — not just today's calendar.

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
