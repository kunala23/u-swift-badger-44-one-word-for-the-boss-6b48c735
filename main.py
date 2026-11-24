#!/usr/bin/env python3
"""One Word for the Boss — pick the single best word for a boss.

The judge compares two words on five things, most important first:
1. it is a single word a person would actually use about their boss,
2. it is funny on its own,
3. it rings true about a real boss habit,
4. it is fresh, not the first word anyone reaches for,
5. it travels across workplaces without explanation.

This program scores a shortlist of candidate words on criteria 2-5
(criterion 1 is enforced as a hard gate: one token, 1-30 characters),
picks the highest scorer with a deterministic tie-break, and writes
exactly that word to /output/entry.txt.
"""

import os
import sys

# Candidate words, each scored 0-10 on (funny, true, fresh, travels).
# The scores are the author's own judgement about office life.
CANDIDATES = {
    # A seagull manager swoops in, squawks loudly, makes a mess and
    # flies off again. Colleagues repeat it at lunch because it lands.
    "Seagull": (9, 9, 8, 8),
    # Nothing sticks to them: blame slides off, credit sticks instead.
    "Teflon": (8, 9, 9, 9),
    # Rules the office like a small kingdom, cape optional.
    "Overlord": (8, 7, 7, 8),
    # Present in the org chart, absent everywhere else.
    "Ghost": (7, 8, 6, 8),
    # Every question bounces; every decision waits for a reply.
    "Unreachable": (6, 8, 5, 9),
    # Turns a five-minute question into a recurring hour-long meeting.
    "Meetingmaker": (7, 8, 6, 7),
    # Every decision, approval and email queues behind one person.
    "Bottleneck": (6, 9, 5, 8),
    # Shields the team from the rain above; rarely thanked for it.
    "Umbrella": (5, 7, 7, 7),
    # Watches every keystroke. True, but the first word anyone says.
    "Micromanager": (5, 9, 2, 9),
    # Lives as a date on the calendar, not as a person in the room.
    "Deadline": (4, 6, 4, 7),
}

# Judge order: funny and true matter most, then fresh, then travels.
WEIGHTS = (3, 3, 2, 1)


def score(word):
    """Weighted score for one candidate word."""
    marks = CANDIDATES[word]
    return sum(mark * weight for mark, weight in zip(marks, WEIGHTS))


def is_valid_word(word):
    """Gate: a single word, 1-30 characters, not only whitespace."""
    if not word or len(word) > 30:
        return False
    if word != word.strip() or not word.strip():
        return False
    if any(ch.isspace() for ch in word):
        return False
    return True


def pick_word():
    """Best candidate; ties break on funny, then true, then fresh,
    then alphabetically, so the result is the same on every run."""
    valid = [w for w in CANDIDATES if is_valid_word(w)]
    if not valid:
        raise ValueError("no valid candidate word")
    funny, true, fresh, travels = 0, 1, 2, 3
    return sorted(
        valid,
        key=lambda w: (
            -score(w),
            -CANDIDATES[w][funny],
            -CANDIDATES[w][true],
            -CANDIDATES[w][fresh],
            w,
        ),
    )[0]


def main():
    word = pick_word()
    if not is_valid_word(word):
        print(f"picked word failed the gate: {word!r}", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(word)
    print(f"wrote entry: {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
