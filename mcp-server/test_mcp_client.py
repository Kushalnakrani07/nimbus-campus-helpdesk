#!/usr/bin/env python3
"""
Test client for nimbus-campus-mcp-server.
Simulates an MCP client communicating with server.py over stdio.
Logs the exact JSON-RPC 2.0 messages exchanged.
"""

import subprocess
import json
import os
import sys

SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")

def run_tests():
    proc = subprocess.Popen(
        [sys.executable, SERVER_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    test_steps = [
        (
            "1. Client Handshake / Capability Negotiation (initialize)",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "Nimbus-Test-Inspector",
                        "version": "1.0.0"
                    }
                }
            }
        ),
        (
            "2. Tool Discovery (tools/list)",
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
        ),
        (
            "3. Tool Invocation - get_timetable (Success)",
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "get_timetable",
                    "arguments": {
                        "batch": "CSE-2026-A",
                        "day": "Monday"
                    }
                }
            }
        ),
        (
            "4. Tool Invocation - get_fee_status (Success)",
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "get_fee_status",
                    "arguments": {
                        "student_id": "NIMBUS-STU-001"
                    }
                }
            }
        ),
        (
            "5. Tool Invocation - Failure Case (Unknown Student ID)",
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "get_fee_status",
                    "arguments": {
                        "student_id": "STUDENT-NON-EXISTENT"
                    }
                }
            }
        ),
        (
            "6. Resource Discovery (resources/list)",
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "resources/list",
                "params": {}
            }
        ),
        (
            "7. Resource Reading - Hostel Rules (resources/read)",
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "resources/read",
                "params": {
                    "uri": "hostel://rules"
                }
            }
        )
    ]

    print("=" * 70)
    print("🚀 EXECUTING MCP PROTOCOL TEST SUITE")
    print("=" * 70)

    for description, request_payload in test_steps:
        print(f"\n--- {description} ---")
        req_line = json.dumps(request_payload)
        print(f"▶ CLIENT >> {req_line}")
        proc.stdin.write(req_line + "\n")
        proc.stdin.flush()

        resp_line = proc.stdout.readline().strip()
        print(f"◀ SERVER << {resp_line}")

    proc.stdin.close()
    proc.wait()
    stderr_output = proc.stderr.read()
    if stderr_output:
        print("\n--- SERVER STDERR DIAGNOSTICS ---")
        print(stderr_output.strip())

    print("\n" + "=" * 70)
    print("✅ MCP TEST SUITE COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
