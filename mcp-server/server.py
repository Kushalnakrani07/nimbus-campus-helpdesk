#!/usr/bin/env python3
"""
Official Model Context Protocol (MCP) Server for Nimbus Labs Campus Helpdesk.
Specification Version: 2024-11-05 (JSON-RPC 2.0 over STDIO)

Exposes:
- Tools:
    1. get_timetable(batch: str, day: str)
    2. get_fee_status(student_id: str)
- Resources:
    1. hostel://rules (Hostel Rules & Residential Regulations)
"""

import sys
import json
import os
import csv
from typing import Any, Dict, List, Optional

SERVER_NAME = "nimbus-campus-mcp-server"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TIMETABLE_CSV = os.path.join(BASE_DIR, "..", "skill", "timetable-helper", "data", "timetable.csv")
FEE_JSON = os.path.join(DATA_DIR, "fee_status.json")
HOSTEL_RULES_MD = os.path.join(DATA_DIR, "hostel_rules.md")

def log(msg: str):
    """Log diagnostics to stderr to prevent corrupting stdout JSON-RPC stream."""
    sys.stderr.write(f"[{SERVER_NAME}] {msg}\n")
    sys.stderr.flush()

# --- Tool Implementations ---

def get_timetable(batch: str, day: str) -> Dict[str, Any]:
    """Retrieve schedule for a given batch and day."""
    if not batch or not batch.strip():
        raise ValueError("Missing required parameter: 'batch'")
    if not day or not day.strip():
        raise ValueError("Missing required parameter: 'day'")

    batch_clean = batch.strip().upper()
    day_clean = day.strip().capitalize()

    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day_clean not in valid_days:
        raise ValueError(f"Invalid day '{day}'. Allowed values: {', '.join(valid_days)}")

    if not os.path.exists(TIMETABLE_CSV):
        raise FileNotFoundError(f"Timetable database not found at {TIMETABLE_CSV}")

    results = []
    with open(TIMETABLE_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["batch_id"].upper() == batch_clean and row["day_of_week"].capitalize() == day_clean:
                results.append(row)

    if not results:
        return {
            "found": False,
            "message": f"No scheduled sessions found for batch '{batch_clean}' on '{day_clean}'.",
            "sessions": []
        }

    return {
        "found": True,
        "batch": batch_clean,
        "day": day_clean,
        "total_sessions": len(results),
        "sessions": results
    }

def get_fee_status(student_id: str) -> Dict[str, Any]:
    """Query fee payment, balance due, and registration holds for a student ID."""
    if not student_id or not student_id.strip():
        raise ValueError("Missing required parameter: 'student_id'")

    sid_clean = student_id.strip().upper()

    if not os.path.exists(FEE_JSON):
        raise FileNotFoundError(f"Fee records database not found at {FEE_JSON}")

    with open(FEE_JSON, mode="r", encoding="utf-8") as f:
        db = json.load(f)

    for record in db.get("records", []):
        if record["student_id"].upper() == sid_clean:
            return {
                "status": "success",
                "student_id": record["student_id"],
                "student_name": record["student_name"],
                "term": record["term"],
                "tuition_billed": record["tuition_billed"],
                "scholarship_applied": record["scholarship_applied"],
                "amount_paid": record["amount_paid"],
                "balance_due": record["balance_due"],
                "payment_status": record["payment_status"],
                "holds": record.get("holds", []),
                "receipt_reference": record.get("receipt_reference")
            }

    raise KeyError(f"Student ID '{sid_clean}' was not found in the student accounts registry.")

# --- Tool & Resource Schemas ---

TOOLS = [
    {
        "name": "get_timetable",
        "description": "Retrieves the scheduled university classes, lecture halls, and instructors for a specific student batch and day of the week.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "batch": {
                    "type": "string",
                    "description": "The academic batch identifier (e.g. 'CSE-2026-A' or 'CSE-2026-B')."
                },
                "day": {
                    "type": "string",
                    "description": "The day of the week (e.g. 'Monday', 'Tuesday', 'Friday')."
                }
            },
            "required": ["batch", "day"]
        }
    },
    {
        "name": "get_fee_status",
        "description": "Retrieves the financial clearance, outstanding balance, scholarship credits, and registration holds for a student.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "The unique student identification code (e.g. 'NIMBUS-STU-001')."
                }
            },
            "required": ["student_id"]
        }
    }
]

RESOURCES = [
    {
        "uri": "hostel://rules",
        "name": "Nimbus Labs Hostel Rules & Regulations",
        "description": "Official residential housing handbook including curfew hours, guest policies, quiet hours, and safety rules.",
        "mimeType": "text/markdown"
    }
]

# --- Protocol Dispatcher ---

def handle_request(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    log(f"Handling request method='{method}' id={req_id}")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION
                }
            }
        }

    elif method == "notifications/initialized":
        log("Client acknowledged initialization handshake.")
        return None

    elif method == "ping":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {}
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            if tool_name == "get_timetable":
                result = get_timetable(arguments.get("batch"), arguments.get("day"))
            elif tool_name == "get_fee_status":
                result = get_fee_status(arguments.get("student_id"))
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool '{tool_name}' not found."
                    }
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ],
                    "isError": False
                }
            }
        except Exception as e:
            log(f"Execution error in tool '{tool_name}': {e}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: {str(e)}"
                        }
                    ],
                    "isError": True
                }
            }

    elif method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "resources": RESOURCES
            }
        }

    elif method == "resources/read":
        uri = params.get("uri")
        if uri == "hostel://rules":
            if os.path.exists(HOSTEL_RULES_MD):
                with open(HOSTEL_RULES_MD, mode="r", encoding="utf-8") as f:
                    content = f.read()
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "text/markdown",
                                "text": content
                            }
                        ]
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32002,
                        "message": "Resource file not found on disk."
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32602,
                    "message": f"Resource URI '{uri}' not found."
                }
            }

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not recognized by server."
            }
        }

def main():
    log("Nimbus Campus Helpdesk MCP Server starting up over STDIO...")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError as err:
            log(f"Malformed JSON-RPC request: {err}")
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(err)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
