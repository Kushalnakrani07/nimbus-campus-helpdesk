#!/usr/bin/env python3
"""
CLI Helper to filter and inspect Nimbus Labs academic timetable.
Used by the timetable-helper skill.
"""
import csv
import sys
import os
import json
from typing import List, Dict, Optional

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "timetable.csv")

def load_timetable(path: str = CSV_PATH) -> List[Dict[str, str]]:
    resolved_path = os.path.abspath(path)
    if not os.path.exists(resolved_path):
        raise FileNotFoundError(f"Timetable CSV not found at {resolved_path}")
    with open(resolved_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def query_schedule(batch: str, day: Optional[str] = None, course: Optional[str] = None) -> List[Dict[str, str]]:
    records = load_timetable()
    results = []
    batch_clean = batch.strip().upper()
    day_clean = day.strip().capitalize() if day else None
    course_clean = course.strip().upper() if course else None

    for row in records:
        if row["batch_id"].upper() != batch_clean:
            continue
        if day_clean and row["day_of_week"].capitalize() != day_clean:
            continue
        if course_clean and (course_clean not in row["course_code"].upper() and course_clean not in row["course_name"].upper()):
            continue
        results.append(row)
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: parse_timetable.py <BATCH> [DAY] [COURSE_QUERY]")
        print("Example: parse_timetable.py CSE-2026-A Monday")
        sys.exit(1)

    batch = sys.argv[1]
    day = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    course = sys.argv[3] if len(sys.argv) > 3 else None

    results = query_schedule(batch, day, course)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
