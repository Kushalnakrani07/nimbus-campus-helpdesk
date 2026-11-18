#!/usr/bin/env python3
"""
Pre-tool-call security hook for campus-helpdesk plugin.
Blocks any file modification or write command targeted at protected directories
(such as /mock-data/ or /skill/ data files).
"""
import sys
import json
import re

PROTECTED_PATHS = [
    r"mock-data/.*",
    r".*\.mcp\.json$",
    r"skill/.*/data/.*\.csv$"
]

def check_payload(payload: dict) -> bool:
    tool_name = payload.get("tool_name", "")
    tool_args = payload.get("tool_arguments", {})

    # Intercept file write or edit tools
    if tool_name in ["write_file", "edit_file", "create_file"]:
        target_path = tool_args.get("path") or tool_args.get("Path", "")
        for pattern in PROTECTED_PATHS:
            if re.search(pattern, target_path):
                print(f"[SECURITY HOOK BLOCKED] Unauthorized write attempt to protected path: '{target_path}'.", file=sys.stderr)
                return False

    # Intercept shell commands attempting destructive actions on protected paths
    if tool_name in ["run_command", "bash"]:
        cmd = tool_args.get("command") or tool_args.get("CommandLine", "")
        if any(kw in cmd for kw in ["rm ", "truncate ", "> mock-data/", "> skill/"]):
            print(f"[SECURITY HOOK BLOCKED] Potentially destructive command detected: '{cmd}'.", file=sys.stderr)
            return False

    return True

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            sys.exit(0)
        data = json.loads(raw_input)
        if not check_payload(data):
            sys.exit(1) # Return non-zero to abort execution
        sys.exit(0)
    except Exception as e:
        print(f"[SECURITY HOOK ERROR] Hook verification error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
