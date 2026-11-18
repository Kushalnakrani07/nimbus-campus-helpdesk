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
├── skill/                         # Timetable triage skill
│   └── timetable-helper/
├── plugin/                        # Plugin manifest and packaging assets
│   └── campus-helpdesk/
└── mcp-server/                    # FastMCP server exposing tools & resources
    └── server.py
```

---

## 🚀 4-Phase Implementation Roadmap

| Phase | Component | Status | Description |
| :--- | :--- | :---: | :--- |
| **Phase 1** | **Repository Structure & Mock Data** | ✅ Complete | Directory scaffolding, mock JSON datasets, and starter documentation |
| **Phase 2** | **Agent Skill (`/skill`)** | ✅ Complete | `SKILL.md` triage logic, categorization schemas, and evaluation test prompts |
| **Phase 3** | **Plugin Packaging (`/plugin`)** | ✅ Complete | Packaging manifest (`plugin.json`), metadata, and local installation CLI commands |
| **Phase 4** | **MCP Server (`/mcp-server`)** | ✅ Complete | Official Python MCP implementation exposing tools over STDIO |

---

## 📚 Official Documentation & References

- **Model Context Protocol (MCP) Specification**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **MCP Python SDK (`FastMCP`)**: [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- **Anthropic Claude Code Documentation**: [https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
- **Git Worktree Documentation**: [https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

## Skill Evaluation Suite
This branch introduces automated pytest fixtures for timetable-helper skill.

## High-Performance MCP Transport Options
This branch migrates stdio to streaming HTTP SSE transport for cloud deployment.
