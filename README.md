# 🎓 Nimbus Labs Campus Helpdesk Agent

An academic reference implementation of an autonomous campus IT & services helpdesk agent, powered by Anthropic Agent Skills, Plugins, and the Model Context Protocol (MCP).

---

## 📂 Repository Layout

```text
nimbus-campus-helpdesk/
├── README.md                      # Project documentation and phase tracking
├── mock-data/                     # Ground-truth mock dataset for campus systems
│   ├── wifi_status.json           # Real-time campus AP health, SSIDs, and outages
│   ├── library_hours.json         # Facility operational hours, exceptions, and policies
│   └── it_tickets.json            # ITSM service tickets, statuses, and categories
├── skill/                         # Phase 2: Agent skill instructions and triage prompt
│   └── .gitkeep
├── plugin/                        # Phase 3: Plugin manifest and packaging assets
│   └── .gitkeep
└── mcp-server/                    # Phase 4: FastMCP server exposing tools & resources
    └── .gitkeep
```

---

## 🚀 4-Phase Implementation Roadmap

| Phase | Component | Status | Description |
| :--- | :--- | :---: | :--- |
| **Phase 1** | **Repository Structure & Mock Data** | ✅ Complete | Directory scaffolding, mock JSON datasets, and starter documentation |
| **Phase 2** | **Agent Skill (`/skill`)** | ⏳ Pending Approval | `SKILL.md` triage logic, categorization schemas, and evaluation test prompts |
| **Phase 3** | **Plugin Packaging (`/plugin`)** | ⏳ Pending Approval | Packaging manifest (`plugin.json`), metadata, and local installation CLI commands |
| **Phase 4** | **MCP Server (`/mcp-server`)** | ⏳ Pending Approval | Official Python `mcp` SDK / `FastMCP` implementation exposing tools over STDIO |

---

## 📊 Mock Datasets Overview

All data files use strictly synthetic test data (no PII, credentials, or production tokens):

1. **`mock-data/wifi_status.json`**:
   - Campus SSIDs: `Nimbus-Secure-WiFi`, `Nimbus-Guest-Web`, `Nimbus-IoT-Devices`
   - Zone monitoring: Library (`ZONE-LIB-01`), Science Complex (`ZONE-SCI-02` - degraded), Residence Halls (`ZONE-DORM-03`), Student Commons (`ZONE-STU-04`).
2. **`mock-data/library_hours.json`**:
   - Weekly opening/closing schedules, desk support hours, exam period 24/7 exceptions, and study room reservation policies.
3. **`mock-data/it_tickets.json`**:
   - Normalized ticket schema with mock requester IDs (`USER-MOCK-901` to `904`), statuses (`open`, `in-progress`, `resolved`), and priority levels.

---

## 📚 Official Documentation & References

- **Model Context Protocol (MCP) Specification**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **MCP Python SDK (`FastMCP`)**: [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- **Anthropic Claude Code Documentation**: [https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
- **Git Directory Tracking Conventions**: [https://git-scm.com/docs/gitignore](https://git-scm.com/docs/gitignore)

## Skill Evaluation Suite
This branch introduces automated pytest fixtures for timetable-helper skill.
