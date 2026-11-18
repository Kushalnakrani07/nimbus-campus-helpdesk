---
name: timetable-helper
description: Answers student and faculty queries regarding Nimbus Labs academic timetables, class schedules, lecture halls, and instructor allocations using verified schedule data.
---

# Timetable Helper Skill

## Purpose
Enables the agent to provide accurate, verified academic schedules for Nimbus Labs university courses across batches, days, and instructors.

## Operational Workflow
1. **Identify Query Parameters**:
   - Extract `batch_id` (e.g., `CSE-2026-A`, `CSE-2026-B`). If missing, ask the user to clarify their batch before querying.
   - Extract `day_of_week` (e.g., `Monday`, `Friday`).
   - Extract optional `course_code` or `course_name` (e.g., `CS301`, `Operating Systems`).

2. **Retrieve Schedule**:
   - Query schedule data by executing `scripts/parse_timetable.py <BATCH> [DAY] [COURSE]` or reading `data/timetable.csv`.
   - Refer to [csv_columns.md](file:///Users/kushalnakrani/Documents/antigravity/scratch/service-request-management-system/nimbus-campus-helpdesk/skill/timetable-helper/references/csv_columns.md) for data schema definitions.

3. **Format Response**:
   - Display sessions chronologically with start/end time, course code, course title, instructor, and room location.
   - Refer to [edge_cases.md](file:///Users/kushalnakrani/Documents/antigravity/scratch/service-request-management-system/nimbus-campus-helpdesk/skill/timetable-helper/references/edge_cases.md) for handling vacant slots and edge cases.

## Strict Anti-Fabrication Rule
- **NEVER** hallucinate or invent classes, times, room numbers, or professors that are absent from `data/timetable.csv`.
- If a queried course does not appear in the verified records, explicitly answer:
  > "Course '[Course Name]' was not found in the official schedule for batch [Batch]. No matching classes are listed in the university registry."
