# 📋 Rules Context Loader - Instance Health Rules Documentation

**Quick Context for AI Agents** | Last Updated: Jan 15, 2026

---

## 🎯 **What Is This?**

This document covers the **Instance Health Rules documentation and enhancement work** - a parallel workstream focused on documenting, enhancing, and expanding the Instance Health rule set for the Eightfold platform.

**This is SEPARATE from the main app development** (see [DE_heath_report_app repository](https://github.com/mharrison-eightfold/DE_heath_report_app) for app work).

---

## 🔬 **AI Agent: Rule Evaluation Methodology**

### When to Use This Methodology

Use this process when the user provides:
- A new set of rules to evaluate
- Ticket data for evidence mapping
- Request to improve existing rules
- Request to suggest new rules
- Request to prioritize rules

### The Complete Rule Evaluation Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    RULE EVALUATION PROCESS                       │
├─────────────────────────────────────────────────────────────────┤
│  1. LOAD CONTEXT → Rules Context Loader + Technical Reference   │
│  2. ANALYZE TICKETS → Review JIRA/ticket data, identify patterns│
│  3. MAP EVIDENCE → Link tickets to existing rules               │
│  4. PRIORITIZE → Rate all rules P0/P1/P2/P3/Remove              │
│  5. GAP ANALYSIS → Find missing rules from ticket patterns      │
│  6. PROPOSE NEW → Create new rules with evidence (sparingly!)   │
│  7. DOCUMENT → Executive summary, TSV files, MD knowledge docs  │
│  8. VALIDATE → Optional: Live JQL queries against projects      │
└─────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Load Context

**Required Documents:**
1. `RULES_CONTEXT_LOADER.md` (this file)
2. `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` (primary knowledge source)

**Actions:**
- Understand rule structure (SKU, Product Area, Rule ID, Config Reference, Description)
- Know the rule categories (Config Health, Data Health, Operational Health)
- Know the product areas (TA Core, TA PCS, TM Core, TM Leader, AI/TIP, Security, Analytics)

---

### Step 2: Analyze Ticket Data

**Supported Formats:**
- TSV files (preferred)
- CSV files
- Google Sheets (export to TSV first)

**Key Columns to Analyze:**

| Column | Purpose |
|--------|---------|
| Issue Key | JIRA ticket ID (e.g., IMPL-199330) |
| Issue Type | Bug, Partner Support, Action Item |
| RCA Reason | Root Cause Analysis category |
| Product | Which product area affected |
| Implementing Team | Which team handles it |
| Summary | Brief description |
| Labels | Tags for categorization |
| Customer/Project | Which implementation |

**Analysis Commands:**
```bash
# Count total tickets
wc -l < tickets.tsv

# Get column headers
head -1 tickets.tsv | tr '\t' '\n' | nl

# RCA distribution
cut -f[RCA_COLUMN] tickets.tsv | sort | uniq -c | sort -rn | head -20

# Product area distribution
cut -f[PRODUCT_COLUMN] tickets.tsv | sort | uniq -c | sort -rn | head -20

# Search for specific issues
grep -i "configuration" tickets.tsv | wc -l
grep -i "email" tickets.tsv | head -10
```

**Key Metrics to Extract:**
- Total ticket count
- Date range
- Issue type distribution (Bug vs Support vs Action Item)
- RCA reason distribution (especially "Configuration Issue")
- Product area impact
- Implementing team distribution
- Common labels

---

### Step 3: Map Evidence to Existing Rules

**Evidence Format:**
```
Evidence column should contain only JIRA ticket keys, e.g.:
IMPL-199330, IMPL-199342, IMPL-199374
```

**Search Strategy:**

For each rule category, search tickets using relevant keywords:

| Rule Category | Search Keywords |
|---------------|-----------------|
| Email/SMS | email, sms, communication, send, notification |
| Scheduling | scheduling, calendar, availability, slots, interview |
| Career Hub | career hub, ijp, internal mobility, job bands |
| PCS/Career Site | career site, pcs, apply, application, branding |
| Integration/Sync | sync, integration, workday, webhook, hris |
| Calibration | calibration, calibrate, position, match |
| Permissions | permission, access, role, visibility |
| Branding | logo, color, theme, brand, css |
| Data Quality | quality, missing, incomplete, threshold |

**Mapping Process:**
1. Search tickets for each rule's keywords
2. Read ticket summaries to confirm relevance
3. Add JIRA keys to Evidence column
4. Track rules without evidence for Step 4

---

### Step 4: Prioritize Rules

**Priority Rating Scale:**

| Priority | Definition | Go-Live Blocker? | Action |
|----------|------------|------------------|--------|
| **P0** | Critical - Blocking functionality or security issues | Yes | Must fix before go-live |
| **P1** | High - Core functionality significantly impacted | Usually | Fix before go-live if possible |
| **P2** | Medium - Important but workarounds exist | No | Fix post go-live |
| **P3** | Low - Nice to have / edge cases / minor impact | No | Backlog |
| **Remove** | No value / causes false positives / deprecated | No | Remove from rule set |

**P0 Examples:**
- Loopback email not configured (emails fail)
- Career site completely inaccessible
- SSO broken
- Data sync completely failing

**P1 Examples:**
- Email templates misconfigured (some emails work)
- Stage mapping incomplete (funnel metrics wrong)
- Scheduling config missing slots (limited availability)

**P2 Examples:**
- Branding colors not set (uses defaults)
- Optional features not configured
- Data quality below threshold but above minimum

**P3 Examples:**
- Analytics dashboard tweaks
- Edge case configurations
- Non-customer-facing settings

**Remove Examples:**
- Static text that has no functional impact
- Personal preference metrics
- Deprecated features no longer used

**Decision Framework:**
```
Is it blocking core functionality? → P0
Is it impacting user experience significantly? → P1
Is it important but has workarounds? → P2
Is it nice to have but optional? → P3
Does it cause more noise than value? → Remove
```

---

### Step 5: Gap Analysis for New Rules

> ⚠️ **CRITICAL PHILOSOPHY: The goal is NOT more rules, but the RIGHT rules.**
> 
> Creating new rules is NOT preferable to having no new rules. Every new rule adds:
> - Maintenance overhead
> - Potential for false positives
> - Additional noise for implementation teams
> 
> Only propose a new rule if there is **clear, repeated evidence** that the rule would prevent real issues.

**Identify Patterns NOT Covered by Existing Rules:**

1. **High-frequency ticket categories** without corresponding rules
2. **Recurring configuration issues** from ticket RCA data
3. **New product features** that need configuration validation
4. **Integration points** that commonly fail

**Gap Analysis Questions:**
- What configuration issues appear repeatedly in tickets?
- What breaks most often during implementations?
- What would catch issues earlier if validated?
- What customer-facing functionality lacks a rule?

#### Handling Customer-Specific Requirements

**⚠️ IMPORTANT: Distinguish Between Default vs Customer-Specific Issues**

When analyzing tickets, you must determine if the issue was caused by:

| Issue Type | Description | Rule Approach |
|------------|-------------|---------------|
| **Default Configuration Miss** | The platform default was wrong or missing | ✅ Good candidate for a rule |
| **Customer-Specific Requirement** | Customer wanted something different from default | ⚠️ Requires special handling |
| **Implementation Error** | Implementer made a mistake | ✅ Good candidate for a rule |
| **Product Bug** | Platform code issue | ❌ Not a config rule - engineering fix |

**For Customer-Specific Requirements:**

1. **Can the rule check for non-default values?**
   - If yes: Create a rule that validates non-default values are properly configured
   - Example: "If `custom_branding = true`, then `brand_colors` must be set"

2. **Does the rule have access to customer requirements?**
   - Usually NO - rules only see configuration, not the customer's SOW or requirements doc
   - If the rule cannot validate accuracy against customer requirements, it may not be possible to create

3. **Types of customer-specific rules that CAN work:**
   ```
   ✅ "If feature X is enabled, config Y must be set" (conditional checks)
   ✅ "Non-empty value required when override is enabled"
   ✅ "Custom field mappings must exist if custom sync is enabled"
   ✅ "If using non-default template, template must be valid"
   ```

4. **Types that CANNOT work:**
   ```
   ❌ "Customer's specific logo matches their brand guidelines"
   ❌ "Email text matches customer's requested wording"
   ❌ "Workflow stages match customer's hiring process"
   ❌ "Custom field values are correct per SOW"
   ```

**Decision Tree for Customer-Specific Issues:**

```
Was the issue due to customer-specific requirements?
│
├─ NO → Normal rule evaluation (proceed to Step 6)
│
└─ YES → Can the rule check config without knowing the requirement?
         │
         ├─ YES (e.g., "non-default value must be set") 
         │       → Create conditional rule
         │
         └─ NO (e.g., "must match SOW specifications")
                 → NOT suitable for automated rule
                 → Document as "requires manual review"
                 → Consider adding to implementation checklist instead
```

---

### Step 6: Propose New Rules

> ⚠️ **REMINDER: Less is more. Only propose rules with strong justification.**

**Before Proposing ANY New Rule, Ask:**

1. **Is there repeated evidence?** (Multiple tickets, not just one)
2. **Would this rule prevent real issues?** (Not just theoretical)
3. **Can the rule actually validate correctness?** (Has access to needed data)
4. **Is it a default config issue or customer-specific?** (See Step 5)
5. **Would this rule cause false positives?** (Noise vs value)
6. **Does an existing rule already cover this?** (Avoid duplicates)

**If the answer to any of these is "No" or "Uncertain" → Do NOT propose the rule**

**New Rule Format:**

```tsv
SKU	Product Area	Rule Name	Rule ID	Config Reference	Cursor Generated Description	New Feature Alignment	Evidence	Status
[SKU]	[Area]	[Name]	[rule_id]	[config_path]	[Purpose/Impact/To Fix]	[Feature]	[JIRA Keys]	NEW
```

**Description Format:**
```
**Purpose:** [What the rule validates and why]

**Impact:** [What breaks if this rule fails]

**To Fix:** [Step-by-step resolution]
```

**New Rule Priority Assignment:**
- P0: Would prevent critical failures
- P1: Would catch significant issues early
- P2: Would improve configuration quality
- P3: Would catch edge cases

**When to Mark as "NOT RECOMMENDED" Instead of Creating Rule:**

| Scenario | Action |
|----------|--------|
| Issue is customer-specific and rule can't validate accuracy | Mark as "Manual Review Required" |
| Only 1-2 tickets for this issue | Insufficient evidence - don't create rule |
| Rule would require access to external requirements | Mark as "Cannot Automate" |
| High risk of false positives | Mark as "Risk Outweighs Benefit" |
| Issue is better handled by training | Mark as "Process/Training Issue" |

**Example New Rule:**
```
SKU: Talent Acquisition Core
Product Area: Communications
Rule Name: A2P 10DLC SMS Registration
Rule ID: sms_a2p_10dlc_registered
Config Reference: sms_config → a2p_registration
Description: **Purpose:** Validates SMS sender is registered for A2P 10DLC compliance...
Evidence: IMPL-199330, IMPL-199342
Status: NEW
```

**Example "NOT RECOMMENDED" Entry:**
```
SKU: Talent Acquisition Core
Product Area: Branding
Rule Name: Custom Logo Matches Brand Guidelines
Rule ID: N/A
Config Reference: branding_config → logo
Justification: Cannot automate - rule has no access to customer's brand guidelines. 
               Logo presence can be validated, but accuracy requires manual review.
Status: NOT RECOMMENDED - Manual Review Required
```

---

### Step 7: Document Findings

**Create These Files:**

| File | Purpose | Format |
|------|---------|--------|
| `TICKET_DATA_SCOPE_SUMMARY.md` | Summary of ticket data analyzed | Markdown |
| `INSTANCE_HEALTH_RULES_TICKET_ANALYSIS.md` | Detailed findings | Markdown |
| `All rules with Priority.tsv` | Rules with Priority column added | TSV |
| `SUGGESTED_NEW_RULES.tsv` | New proposed rules | TSV |
| `EXECUTIVE_SUMMARY_RULES_EVALUATION.md` | Summary for stakeholders | Markdown |

**Ticket Data Scope Summary Should Include:**
- Data source
- Total tickets
- Date range
- Issue type distribution
- Status distribution
- RCA reason distribution
- Product areas covered
- Implementing teams
- Key observations

**Executive Summary Should Include:**
- Overview of analysis goals
- Key findings from ticket analysis
- Rule evaluation methodology
- Results (priority distribution)
- New rules proposed
- **Issues identified as NOT suitable for rules** (customer-specific, manual review needed)
- Recommendations

---

### Step 8: Validate (Optional)

**Use Jira MCP for Live Queries:**
```
mcp_Atlassian-MCP-Server_searchJiraIssuesUsingJql
```

**Example JQL Queries:**
```jql
# Bugs for specific project
project = "Customer Implementations" AND issuetype = bug AND "Project Name" = "PROJECT_NAME"

# Configuration issues
project = IMPL AND "RCA Reason" = "Configuration Issue - Implementation"

# Recent tickets for product
project = IMPL AND created >= 2024-01-01 AND product = "TA"
```

**Validate Findings:**
- Confirm ticket patterns with live data
- Check if issues are still occurring
- Identify additional evidence for rules

---

## 📊 **Reference: Evaluation Metrics from Jan 2026 Exercise**

### Ticket Analysis Summary

| Metric | Value |
|--------|-------|
| Total Tickets Analyzed | 3,019 |
| Issue Types | 64% Bugs, 36% Partner Support |
| Configuration Issues | 352 tickets (11.7%) |
| Health Check Exemptions | 32 tickets (1.1%) |

### RCA Distribution (Top 5)

| RCA Category | Tickets | % |
|--------------|---------|---|
| Product Bug | 597 | 19.8% |
| ENG Support Required | 551 | 18.3% |
| Configuration Issue - Implementation | 352 | 11.7% |
| New Implementation Request | 256 | 8.5% |
| Gap in Product Understanding | 203 | 6.7% |

### Rule Evaluation Results

| Priority | Count | % |
|----------|-------|---|
| P0 | 12 | 3.9% |
| P1 | 62 | 20.1% |
| P2 | 186 | 60.4% |
| P3 | 46 | 14.9% |
| Remove | 2 | 0.6% |

### New Rules Proposed

| Priority | Count |
|----------|-------|
| P0 (Critical) | 3 |
| P1 (High) | 8 |
| P2 (Medium) | 11 |
| P3 (Low) | 3 |
| **Total** | **25** |

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

## 🆕 **Recent Updates (Jan 8-15, 2026)**

### **Jan 15, 2026** - Rule Evaluation Methodology Added

**✅ Added Complete Rule Evaluation Methodology** 📋
- 8-step process for evaluating rules with ticket data
- Priority rating scale (P0/P1/P2/P3/Remove) with definitions
- Evidence mapping process
- Gap analysis for new rules
- Documentation requirements
- Reference metrics from Jan 2026 exercise

**✅ Added New Rule Creation Philosophy** ⚠️
- "The goal is NOT more rules, but the RIGHT rules"
- Guidance on distinguishing default vs customer-specific issues
- Decision tree for customer-specific requirements
- Criteria for when NOT to create a rule
- "NOT RECOMMENDED" status for issues that can't be automated

**Exercise Results:**
- 308 rules evaluated
- 64 rules with ticket evidence
- 292 rules prioritized based on product/code analysis
- 25 new rules proposed
- 2 rules marked for removal

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
- [ ] **For rule evaluation**: Follow the 8-step Rule Evaluation Methodology
- [ ] **For new rules**: Remember - the goal is RIGHT rules, not MORE rules
- [ ] **When learning new info**: Update `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`
- [ ] Understand: This is **separate from app development** (app code goes to DE_heath_report_app repository)
- [ ] Understand: 165 original rules + 136 new rules = 301 total documented rules
- [ ] Know the rule categories: Config Health, Data Health, Operational Health
- [ ] Know the 6 checkpoints and their purposes
- [ ] Know the priority scale: P0 (critical) → P3 (low) → Remove
- [ ] Know when NOT to create a rule: customer-specific, manual review needed, insufficient evidence
- [ ] Know where to find technical details: `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`
- [ ] Know where to find remediation guidance: `RAG_KNOWLEDGE_BASE.md`
- [ ] Understand: Each rule has Purpose, Impact, To Fix sections
- [ ] Know: Rules map to actual Eightfold codebase (`www/data_audit/platform_health/...`)
- [ ] Know: Use `mcp_MCP-GITHUB_*` tools for pushing files

---

## 💡 **Key Principles**

1. **Use MCP for GitHub**: Git CLI doesn't have authentication - always use MCP GitHub tools
2. **Less is More**: The goal is the RIGHT rules, not MORE rules - avoid rule proliferation
3. **Rule Criterion**: Only add rules that are **absolutely required** for functionality (not "nice to have")
4. **Customer-Specific Awareness**: Distinguish between default config issues (can automate) vs customer-specific requirements (often can't automate)
5. **Ownership**: Product Delivery Team and Partners responsible for 100% config health pass rate
6. **Documentation First**: Every rule must have clear Purpose, Impact, and To Fix guidance
7. **Evidence-Based**: Link rules to supporting tickets/issues when possible
8. **Priority-Driven**: Assign P0-P3 ratings based on go-live impact
9. **Confluence Integration**: Link to official documentation whenever possible
10. **Code Traceability**: Every rule maps to implementation in Eightfold codebase
11. **AI-Friendly**: Documentation structured for AI analysis and recommendations
12. **Actionable**: Focus on "what to do" not just "what's wrong"
13. **Living Documentation**: Update Technical Reference when new information is learned

---

**You're ready to work on rules documentation! 🚀**

For app development work, see: **[DE_heath_report_app repository](https://github.com/mharrison-eightfold/DE_heath_report_app)**
