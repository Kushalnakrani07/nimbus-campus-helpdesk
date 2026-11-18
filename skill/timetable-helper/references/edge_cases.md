# Timetable Query Edge Cases & Fallback Rules

### 1. Batch Not Specified
If the user asks "What class do I have at 9 AM?" without specifying their batch:
- **Action**: Do NOT assume a default batch. Politely ask the user for their batch identifier (e.g., `CSE-2026-A` or `CSE-2026-B`).

### 2. No Class Scheduled for Slot or Day
If the user queries for a day with no classes (e.g. Sunday) or a time slot with no session:
- **Action**: State clearly: "No classes are scheduled for [Batch] on [Day] at [Time]."
- List the next immediate scheduled session for that batch if known.

### 3. Strict Non-Fabrication Rule (Adversarial Defense)
If a user asks about a course that does not exist in `timetable.csv` (e.g., "When is quantum robotics with Dr. Octopus?"):
- **Action**: Under NO circumstances should the agent extrapolate, hallucinate, or construct a plausible-sounding schedule.
- Explicitly output:
  > "Course '[Course Name]' was not found in the official Nimbus Labs academic schedule for [Batch]. Please verify the course code in the campus catalog."

### 4. Case-Insensitive Matching
- Batch IDs should be case-insensitive (e.g. `cse-2026-a` -> `CSE-2026-A`).
- Days of the week should normalize to standard Title Case (`monday` -> `Monday`).
