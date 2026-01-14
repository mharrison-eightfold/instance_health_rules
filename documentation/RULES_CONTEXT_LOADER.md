# 📋 Rules Context Loader - Instance Health Rules Documentation

**Quick Context for AI Agents** | Last Updated: Jan 14, 2026

---

## 🎯 **What Is This?**

This document covers the **Instance Health Rules documentation and enhancement work** - a parallel workstream focused on documenting, enhancing, and expanding the Instance Health rule set for the Eightfold platform.

**This is SEPARATE from the main app development** (see [DE_heath_report_app repository](https://github.com/mharrison-eightfold/DE_heath_report_app) for app work).

---

## 🔧 **AI Agent: GitHub Operations - Use MCP Tool**

### ⚠️ CRITICAL: Git CLI Does NOT Have Authentication

The environment does NOT have git credentials configured:
- ❌ No `.gitconfig` file
- ❌ No `.git-credentials` file
- ❌ No GitHub CLI (`gh`) installed
- ❌ No `GITHUB_TOKEN` environment variable

**Git CLI commands like `git push` will FAIL with authentication errors.**

### ✅ ALWAYS Use MCP GitHub Tool for File Operations

The **MCP GitHub tool** has its own OAuth authentication and should be used for ALL GitHub operations:

| Operation | MCP Tool to Use | Example |
|-----------|-----------------|---------|
| Push files | `mcp_MCP-GITHUB_push_files` | Push multiple files in one commit |
| Update file | `mcp_MCP-GITHUB_create_or_update_file` | Update existing file with SHA |
| Get file | `mcp_MCP-GITHUB_get_file_contents` | Read file and get SHA |
| Create branch | `mcp_MCP-GITHUB_create_branch` | Create new branch |
| Create PR | `mcp_MCP-GITHUB_create_pull_request` | Create pull request |
| List commits | `mcp_MCP-GITHUB_list_commits` | View commit history |

### Example: Pushing a File

```
1. First, get the current file SHA (if updating):
   mcp_MCP-GITHUB_get_file_contents(owner, repo, path, branch)

2. Then update with the SHA:
   mcp_MCP-GITHUB_create_or_update_file(owner, repo, path, content, message, branch, sha)

3. Or push new files:
   mcp_MCP-GITHUB_push_files(owner, repo, branch, files, message)
```

### Handling Large Files

For files larger than ~50KB, the MCP tool may truncate content. Workarounds:
1. **Split into multiple commits** - Push file in sections
2. **Read file locally, push via MCP** - Use `cat` to read, then MCP to push
3. **Use create_or_update_file with SHA** - More reliable for updates

### Repository Information

| Repository | Owner | Use For |
|------------|-------|---------|
| `instance_health_rules` | mharrison-eightfold | Rules documentation |
| `DE_heath_report_app` | mharrison-eightfold | App development |

---

## 🤖 **AI Agent: Technical Reference as Primary Knowledge Source**

### ⚠️ IMPORTANT: For ANY Query Related to Instance Health Rules

**ALWAYS consult the Technical Reference first** for any question, task, or query related to Instance Health rules, including but not limited to:

- ❓ Rule descriptions, purposes, or impacts
- 🔧 Configuration paths and schemas
- 🐛 Troubleshooting rule failures
- 📊 Data quality thresholds
- 🔗 Feature mappings and dependencies
- 📝 Resolution steps and Admin Console paths
- 💻 Code references and implementation details
- 🏷️ Rule categorization (Config Health, Data Health, Operational Health)
- ✅ Checkpoint assignments

### Primary Knowledge Document

**File**: `documentation/INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` (3,971+ lines)

This comprehensive document contains:
- **Rule Logic**: Actual codebase implementation for each rule
- **Configuration Schemas**: Exact config structure being checked
- **Resolution Steps**: Step-by-step instructions to fix failures
- **Config Locations**: Admin Console paths and config names
- **Feature Mappings**: Which product features each rule validates
- **Code References**: File paths in the Eightfold codebase
- **Confluence Links**: Official documentation references
- **Thresholds**: Data quality thresholds (typically 95%)

---

## 📝 **AI Agent: Updating the Technical Reference**

### When to Update the Technical Reference

**UPDATE the `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` when you learn NEW information about rules**, including:

1. **New Rule Details**: When you discover rule logic, configs, or resolution steps not already documented
2. **Corrections**: When you find inaccuracies in existing documentation
3. **New Rules**: When new rules are added to the platform
4. **Config Schema Changes**: When configuration structures change
5. **New Resolution Steps**: When you learn better or updated fix instructions
6. **Code Path Updates**: When implementation files move or change
7. **Threshold Changes**: When data quality thresholds are updated
8. **Feature Mappings**: When rules are associated with different product features
9. **Confluence Updates**: When official documentation links change

### How to Update the Technical Reference

1. **Identify the Section**: Find the appropriate section for the rule/topic
2. **Preserve Existing Format**: Match the existing documentation style
3. **Include All Details**:
   - Rule ID
   - Feature Mapping
   - Config Location
   - Rule Logic (if available)
   - Configuration Schema
   - Technical Description
   - Resolution Steps
4. **Add Code References**: Include file paths when known
5. **Commit with Clear Message**: Describe what was added/changed
6. **Use MCP GitHub Tool**: Push changes using `mcp_MCP-GITHUB_create_or_update_file`

### Update Format Examples

**For a new rule:**
```markdown
### new_rule_id

**Feature Mapping:** [Product Feature]  
**Config Location:** `config_name`

#### Rule Logic
```python
# Code showing how the rule evaluates
```

#### Configuration Schema
```json
{
  "field": "value"
}
```

#### Technical Description
[What the rule does and why it matters]

#### Resolution Steps
1. Navigate to: Admin Console → [Path]
2. Configure: [Specific settings]
3. Verify: [How to confirm it's fixed]
```

**For updating existing rule information:**
```markdown
<!-- Add to the existing rule section -->

**Additional Notes:**
- [New information learned]
- [Updated resolution steps]
- [Configuration changes]
```

### What NOT to Update

- ❌ Don't remove existing information unless it's confirmed incorrect
- ❌ Don't change the document structure significantly
- ❌ Don't add speculative information - only confirmed details
- ❌ Don't duplicate information already present

---

## 📋 **Rule Description Format Standard**

All rule descriptions should follow this **Purpose / Impact / To Fix** format:

```
**Purpose:** [What the rule validates and why it exists]

**Impact:** [What breaks or fails if this rule is not passing]

**To Fix:** [Step-by-step instructions to resolve the failure]
```

### Example Description

```
**Purpose:** Validates that email configuration exists with valid send_from_domain and reply_to_domain settings for candidate communications.

**Impact:** Without email configuration, recruiters cannot send emails to candidates from the platform.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Configuration. Configure send_from_domain and reply_to_domain with verified domains.
```

---

## 🔍 **How to Use the Technical Reference**

### For Any Rule-Related Query:

1. **Search by Rule ID**: Look for the exact rule_id (e.g., `employee_level_quality`)
2. **Search by Feature**: Look in the relevant product section (TM Core, TA PCS, etc.)
3. **Search by Config**: Look for the config name (e.g., `ijp_config`, `scheduling_config`)

### For Rule Descriptions:

1. **Find the Rule**: Search for the rule_id in the technical reference
2. **Extract Key Details**:
   - Feature Mapping (e.g., "Smart Scheduling", "Internal Mobility")
   - Config Location (e.g., `scheduling_config`, `ijp_config`)
   - Rule Logic (from codebase)
   - Configuration Schema
3. **Generate Description**:
   - **Purpose**: What does this rule check and why?
   - **Impact**: What happens if this fails?
   - **To Fix**: What Admin Console path and specific steps?
4. **Reference Resolution Steps**: Use the exact steps from the technical reference

### For Troubleshooting:

1. **Find the Rule**: Locate the rule in the technical reference
2. **Check Resolution Steps**: Follow the documented fix instructions
3. **Review Config Schema**: Understand what values are expected
4. **Check Code Reference**: For deeper debugging, locate the implementation file

### Key Sections in Technical Reference

| Section | Content | Use For |
|---------|---------|---------|
| Talent Management - Core Rules | TM data quality, Career Hub config | TM Core queries |
| Talent Management - Leader Experience Rules | Succession, HRBP, Team View | TM Leader queries |
| Talent Acquisition - Core Rules | Scheduling, Feedback, Pipeline | TA Core queries |
| Talent Acquisition - PCS Rules | Career Site, Smart Apply | TA PCS queries |
| PCS Configuration Guide | Detailed PCS settings | PCS feature understanding |
| Career Hub Configuration Guide | Career Hub config structure | TM config understanding |
| AI/ML Recommendation Rules | Internal Mobility, Mentors | AI rule queries |
| Security Rules | Loopback, Data Retention | Security rule queries |
| Analytics Data Quality Rules | Employee/Position/Application quality | Analytics rule queries |
| Integrations Rules | Sync lag, Webhooks, Field mappings | Integration rule queries |
| Code Reference Guide | File paths for all rules | Implementation lookups |
| Stage Mapping Guide | Stage group configuration | Stage mapping issues |
| Debugging Data Quality Issues | Troubleshooting steps | Data quality problems |

### Supplementary Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `RAG_KNOWLEDGE_BASE.md` | Delivery Excellence methodology, checkpoints | DE process questions |
| `RULE_VERIFICATION_REPORT.md` | Rule verification status | Validating rule accuracy |
| `TA_TM_PCS_product_health_rules_v3.tsv` | Latest rule descriptions (172 rules) with Config Reference | Quick rule lookup |

---

## ⚠️ **CRITICAL: CORRECT REPOSITORY**

### **THIS REPOSITORY: Rules Documentation ONLY**

**Repository Info:**
- ✅ Repository: `mharrison-eightfold/instance_health_rules`
- ✅ URL: https://github.com/mharrison-eightfold/instance_health_rules
- ✅ Working Directory (Cloud): `/home/ec2-user/instance_health_rules`
- ✅ Working Directory (Local Mac): `~/Developer/instance_health_rules`

**What Goes Here:**
- ✅ Rules documentation (`documentation/RULES_CONTEXT_LOADER.md`)
- ✅ Technical reference (`documentation/INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`)
- ✅ AI knowledge base (`documentation/RAG_KNOWLEDGE_BASE.md`)
- ✅ Rule data files (`documentation/*.tsv`)
- ✅ Rule processing tools (`tools/process_new_136_rules.py`, `tools/enhance_*.py`)

### **SEPARATE REPOSITORY: Implementation Health App**

**App Code Goes Here:**
- 🚀 Repository: `mharrison-eightfold/DE_heath_report_app`
- 🚀 URL: https://github.com/mharrison-eightfold/DE_heath_report_app
- 🚀 Working Directory (Cloud): `/home/ec2-user/de_app_1`
- 🚀 Working Directory (Local Mac): `~/Developer/de_app_1`

**What Goes There:**
- 🚀 Backend code (`backend/` - Flask API, services)
- 🚀 Frontend code (`frontend/` - UI, dashboards)
- 🚀 App scripts (`scripts/` - startup scripts)
- 🚀 App tools (`tools/` - implementation_health_report.py)
- 🚀 App documentation (`APP_CONTEXT_LOADER.md`, setup guides)

### **NEVER COMMIT:**
- ❌ **App code to rules repo** (use DE_heath_report_app repo instead)
- ❌ **Rules docs to app repo** (use instance_health_rules repo instead)
- ❌ To EightfoldAI/vscode or any main Eightfold repositories

**Before ANY git operation, verify:**
```bash
git remote -v
# For rules work: mharrison-eightfold/instance_health_rules
# For app work: mharrison-eightfold/DE_heath_report_app
```

**For pushing files, use MCP GitHub tool (NOT git CLI):**
```
mcp_MCP-GITHUB_push_files or mcp_MCP-GITHUB_create_or_update_file
```

---

## 🆕 **Recent Updates (Jan 8-14, 2026)**

### **Jan 14, 2026** - Rule Description Enhancement & Config Reference Updates

**✅ Created TA_TM_PCS_product_health_rules_v3.tsv** 📋
- **172 rules** with enhanced descriptions AND proper Config Reference column
- Config Reference format: Concise config paths (e.g., `ijp_config → job_bands`, `Employee Sync (HRIS) → profile.data_json.employee.level`)
- Columns: SKU, Product Area, Rule Name, Rule ID, Config Reference, Description, Cursor Generated Description, Code Reference, Current Feature ID, Current Feature Name, Action, New Feature Alignment, Updates to rule logic

**✅ Added MCP GitHub Tool Instructions**
- Documented that git CLI does NOT have authentication
- Instructions to use MCP GitHub tools for ALL file operations
- Examples and tool mapping table

**✅ Enhanced AI Agent Instructions**
- Technical Reference as primary knowledge source for ALL rule queries
- Instructions for updating Technical Reference with new information
- Expanded use cases beyond just descriptions

### **Jan 11-12, 2026** - 136 New Rules & Complete Documentation

**✅ Added 136 New Instance Health Rules** 📋
- **AI Rules (22)**: Position calibration, employee profiles, projects, courses, roles, mentors
- **Security Rules (20)**: SEO, domains, campaigns, email loopback, sync failures, data retention
- **Analytics Rules (56)**: Employee quality, application funnel, position quality, stage mapping
- **TIP/Integrations Rules (38)**: Sync lag, webhooks, custom field mappings, EEOC fields, ATS configs

**Each rule includes:**
- Config Reference: Points to specific configuration paths
- Enhanced Description: Purpose, Impact, and To Fix sections
- Code Reference: Implementation file path (e.g., `www/data_audit/platform_health/...`)

**Files:**
- `new_rules_136_input.tsv` (206 lines) - Raw rule data
- `new_rules_136_with_enhanced_descriptions.tsv` (819 lines) - Enhanced with Cursor-generated descriptions

**✅ Created Comprehensive Technical Reference** 📚
- **File**: `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` (3,971 lines!)
- Comprehensive reference for Solution Architects and Functional Consultants
- 165+ rules with technical details, config schemas, resolution steps
- Includes Confluence documentation integration

---

## 📂 **File Structure**

```
instance_health_rules/                                  # ← THIS REPOSITORY
├── documentation/
│   ├── RULES_CONTEXT_LOADER.md                         # ← THIS FILE (start here!)
│   │
│   ├── INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md    # ← 3,971 lines - PRIMARY KNOWLEDGE SOURCE
│   ├── RAG_KNOWLEDGE_BASE.md                           # ← 415 lines - AI domain knowledge
│   ├── RULE_VERIFICATION_REPORT.md                     # ← 183 lines - Rule verification
│   │
│   ├── TA_TM_PCS_product_health_rules_v3.tsv           # ← 173 lines - Latest with Config Reference
│   ├── TA_TM_PCS_product_health_rules_v2.tsv           # ← 173 lines - Previous version
│   ├── new_rules_136_input.tsv                         # ← 136 new rules (raw)
│   ├── new_rules_136_with_enhanced_descriptions.tsv    # ← 136 new rules (enhanced)
│   ├── PCS_TM_TA_rules_with_cursor_descriptions.tsv    # ← 165 original rules (enhanced)
│   └── instance_health_rules_input.tsv                 # ← Original rule input
│
├── tools/
│   ├── process_new_136_rules.py                        # ← Process 136 new rules
│   ├── enhance_all_rule_descriptions.py                # ← Enhance all descriptions
│   ├── enhance_rule_descriptions.py                    # ← Enhance specific descriptions
│   ├── generate_cursor_descriptions.py                 # ← Generate AI descriptions
│   └── apply_rule_refinements.py                       # ← Apply refinements
│
└── README.md                                            # ← Repository overview
```

---

## 🎓 **New Agent Checklist**

When working on rules documentation:

- [ ] **FIRST: Use MCP GitHub tools for file operations** (git CLI has no auth)
- [ ] **Verify correct repository!** Check `mharrison-eightfold/instance_health_rules`
- [ ] Read this file (`RULES_CONTEXT_LOADER.md`)
- [ ] **For ANY rule query**: Read `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` first
- [ ] **When learning new info**: Update `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`
- [ ] Understand: This is **separate from app development** (app code goes to DE_heath_report_app repository)
- [ ] Understand: 165 original rules + 136 new rules = 301 total documented rules
- [ ] Know the rule categories: Config Health, Data Health, Operational Health
- [ ] Know the 6 checkpoints and their purposes
- [ ] Know where to find technical details: `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`
- [ ] Know where to find remediation guidance: `RAG_KNOWLEDGE_BASE.md`
- [ ] Understand: Each rule has Purpose, Impact, To Fix sections
- [ ] Know: Rules map to actual Eightfold codebase (`www/data_audit/platform_health/...`)
- [ ] Know: Use `mcp_MCP-GITHUB_*` tools for pushing files

---

## 💡 **Key Principles**

1. **Use MCP for GitHub**: Git CLI doesn't have authentication - always use MCP GitHub tools
2. **Rule Criterion**: Only add rules that are **absolutely required** for functionality (not "nice to have")
3. **Ownership**: Product Delivery Team and Partners responsible for 100% config health pass rate
4. **Documentation First**: Every rule must have clear Purpose, Impact, and To Fix guidance
5. **Confluence Integration**: Link to official documentation whenever possible
6. **Code Traceability**: Every rule maps to implementation in Eightfold codebase
7. **AI-Friendly**: Documentation structured for AI analysis and recommendations
8. **Actionable**: Focus on "what to do" not just "what's wrong"
9. **Living Documentation**: Update Technical Reference when new information is learned

---

**You're ready to work on rules documentation! 🚀**

For app development work, see: **[DE_heath_report_app repository](https://github.com/mharrison-eightfold/DE_heath_report_app)**
