# Timetable CSV Data Dictionary

This document describes the schema and validation constraints for `data/timetable.csv`.

| Column | Type | Allowed Values / Format | Description |
| :--- | :--- | :--- | :--- |
| `batch_id` | String | `CSE-2026-A`, `CSE-2026-B`, etc. | Academic section/batch identifier |
| `day_of_week` | String | `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday` | Day the session occurs (Title case) |
| `course_code` | String | Format: `^[A-Z]{2,4}[0-9]{3}(-L)?$` (e.g. `CS301`, `CS301-L`) | Official university course catalog code |
| `course_name` | String | Text | Full title of the course |
| `instructor` | String | Text | Name of the primary faculty instructor |
| `start_time` | String | `HH:MM` (24-hour format, e.g. `09:00`) | Scheduled start time |
| `end_time` | String | `HH:MM` (24-hour format, e.g. `10:30`) | Scheduled conclusion time |
| `room` | String | `Hall-XXX`, `Lab-XXX`, `Auditorium-X` | Physical campus room location |
| `class_type` | Enum | `Lecture`, `Practical`, `Seminar`, `Tutorial` | Nature of the academic session |
