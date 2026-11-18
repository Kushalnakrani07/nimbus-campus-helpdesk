# 🔌 Nimbus Campus Helpdesk MCP Server

Official Model Context Protocol (MCP) server implementation exposing campus services, timetables, fee statuses, and hostel regulations over `stdio`.

Compliant with the official MCP Specification (`protocolVersion: 2024-11-05`).

---

## 🔍 Package Audit Note: `@nimbus/mcp-skill-bridge` (v2.3)
> **Audit Finding: FABRICATED / UNVERIFIED PACKAGE**  
> The team lead suggested using `@nimbus/mcp-skill-bridge` (v2.3) to "auto-convert Skills into MCP tools".  
> **Investigation**: A query against public package registries (npm, PyPI) confirms that no package named `@nimbus/mcp-skill-bridge` exists. The package name is fictitious (derived from the fictional organization "Nimbus Labs").  
> **Architecture Decision**: We implement the MCP server using direct JSON-RPC 2.0 stdio framing compliant with the Model Context Protocol specification without relying on non-existent bridge packages.

---

## 🛠️ Exposed Capabilities

### 1. Tools
- `get_timetable(batch: str, day: str)`: Queries university class schedule by batch and day.
- `get_fee_status(student_id: str)`: Returns tuition billing, payment status, scholarships, and holds.

### 2. Resources
- `hostel://rules`: Official Nimbus Labs residential housing handbook.

---

## 🚀 Execution & Testing Instructions

### Run Server directly:
```bash
python3 server.py
```

### Run automated protocol test suite:
```bash
python3 test_mcp_client.py
```

### Connect to Claude Desktop / Claude Code:
Add to your client MCP configuration (`claude_desktop_config.json` or `.mcp.json`):
```json
{
  "mcpServers": {
    "nimbus-campus-helpdesk": {
      "command": "python3",
      "args": ["/absolute/path/to/nimbus-campus-helpdesk/mcp-server/server.py"]
    }
  }
}
```
