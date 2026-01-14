# 📋 Rules Context Loader - Instance Health Rules Documentation

**Quick Context for AI Agents** | Last Updated: Jan 14, 2026

---

## 🎯 **What Is This?**

This document covers the **Instance Health Rules documentation and enhancement work** - a parallel workstream focused on documenting, enhancing, and expanding the Instance Health rule set for the Eightfold platform.

**This is SEPARATE from the main app development** (see [DE_heath_report_app repository](https://github.com/mharrison-eightfold/DE_heath_report_app) for app work).

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
| `TA_TM_PCS_product_health_rules_v2.tsv` | Latest rule descriptions (172 rules) | Quick rule lookup |

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

---

## 🆕 **Recent Updates (Jan 8-14, 2026)**

### **Jan 14, 2026** - Rule Description Enhancement & TSV Updates

**✅ Created TA_TM_PCS_product_health_rules_v2.tsv** 📋
- **172 rules** with enhanced descriptions
- Columns: SKU, Product Area, Rule Name, Rule ID, Config Reference, Description, Cursor Generated Description, Current Feature ID, Current Feature Name, Action to be taken, Feature Alignment, Updated Description, Updates to rule logic
- Rules organized by:
  - **TA Core** (34 rules): Email, SMS, WhatsApp, Pipeline, Scheduling, Feedback
  - **TA CRM Add-ons** (11 rules): Event Recruiting, Smart Campaigns, Talent Communities
  - **TA PCS** (57 rules): Career Site, Smart Apply, Job Alerts, Branding
  - **TM Core** (44 rules): Career Hub, Courses, Data Health, Internal Mobility
  - **TM Leader Experience** (25 rules): Succession Planning, My Team, Projects

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
- Includes Confluence documentation integration:
  - [Instance Health Documentation](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2190936431/Instance+Health)
  - [Platform Health Check](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2063663155/Platform+Health+Check)
  - [Product Go Live and Implementation Phase Management](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2402025554)
  - [Analytics Data Quality - Ongoing Assurance](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2528608431)
  - [Instance Health Exemption Request Process](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2997944353)

**Sections included:**
1. Architecture Overview
2. Rule Types and Ownership (Config Health vs Data Health)
3. Implementation Phase Requirements
4. Talent Management - Core Rules (20+ rules)
5. Talent Management - Leader Experience Rules
6. Talent Acquisition - Core Rules (30+ rules)
7. Talent Acquisition - PCS Rules
8. PCS Configuration Guide
9. Configuration Schema Reference
10. Career Hub Configuration Guide
11. Pipeline & Workflow Configuration
12. Diversity Configuration Guide
13. Event Recruiting Configuration
14. Communities Configuration
15. Profile Masking Configuration
16. Stage Mapping Guide
17. Debugging Data Quality Issues
18. Scheduling Configuration Guide
19. Calibration Configuration Guide
20. Internal Mobility Configuration Guide
21. Succession Planning Configuration Guide
22. Stage Transition Map Configuration
23. Interview Feedback Configuration Guide
24. Communication Configuration Guide
25. Config Health Recommendation Framework
26. AI/ML Recommendation Rules (22 rules)
27. Security Rules (20 rules)
28. Analytics Data Quality Rules (56 rules)
29. Integrations Rules (38 rules)
30. Talent Intelligence Platform Rules
31. Code Reference Guide

**✅ Created RAG Knowledge Base** 🤖
- **File**: `RAG_KNOWLEDGE_BASE.md` (415 lines)
- Domain knowledge for AI systems to generate accurate analysis
- Delivery Excellence methodology documentation
- Checkpoint-based implementation approach
- Remediation guides for common issues

**Sections:**
1. Overview: Delivery Excellence Program
   - DE Models (Partner Led vs EF Led)
   - Implementation Phases (Not Started → Hypercare)
   - Key Metrics (Pass Rate, Checkpoint Completion, Health Score)
2. Checkpoints & Health Rules
   - Checkpoint 1: Pre-project Readiness
   - Checkpoint 2: Design Review (11 rules)
   - Checkpoint 3: Build Review
   - Checkpoint 4: Testing Review
   - Checkpoint 5: Launch Review
   - Checkpoint 6: Hypercare Review
3. Common Issues & Remediation
4. Best Practices & Recommendations

**✅ Rule Verification Report** ✅
- **File**: `RULE_VERIFICATION_REPORT.md` (183 lines)
- Rule verification and validation documentation
- Mapping of rules to Eightfold codebase
- Verification status and findings

**✅ TSV Files with Enhanced Descriptions**
- `TA_TM_PCS_product_health_rules_v2.tsv` (173 lines) - Latest consolidated rules
- `PCS_TM_TA_rules_with_cursor_descriptions.tsv` (166 lines) - Original 165 rules enhanced
- `instance_health_rules_input.tsv` (167 lines) - Original rule input data

---

### **Jan 8-10, 2026** - Documentation Enhancement Phase

**✅ Enhanced All 165 Rule Descriptions**
- Upgraded descriptions with clear Purpose, Impact, and To Fix sections
- Added Confluence documentation references
- Improved technical accuracy based on EF codebase review
- Created comprehensive Code Reference Guide mapping rules to implementation files

**Commits:**
```
4d6c944 - Complete enhancement of all 165 rule descriptions
c566e40 - Enhance 145 rule descriptions with clearer purpose, impact, and fix instructions
933dbbc - docs: add comprehensive TA/TM configuration guides from Confluence
ec89de4 - docs: add comprehensive PCS Configuration Guide from Confluence
280d9c0 - docs: add comprehensive TA module documentation from Confluence
c7e6852 - docs: enhance technical reference with Confluence documentation
bcce091 - docs: create comprehensive technical reference and enhance rule descriptions
5b56d20 - docs: verify and refine rule descriptions based on EF codebase review
6fcbd7c - docs: add Cursor Generated Descriptions for all 165 instance health rules
```

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
│   ├── TA_TM_PCS_product_health_rules_v2.tsv           # ← 173 lines - Latest consolidated rules
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

**Separate Repository (App Code):**
```
DE_heath_report_app/                                    # ← App development repository
├── backend/                                            # ← Flask API
├── frontend/                                           # ← Web UI
├── scripts/                                            # ← Startup scripts
├── tools/                                              # ← App tools (NOT rules tools)
└── documentation/
    └── APP_CONTEXT_LOADER.md                           # ← App context loader
```

---

## 🎯 **What Are Instance Health Rules?**

Instance Health is a tool in the Eightfold Admin Console (`/integrations/implementation_health`) that evaluates the health of any instance (group_id) before:
- **UAT handover** on sandbox
- **Go-live and production cutover**

### Rule Categories

**1. Config Health Rules** 🛠️
- Lightweight rules evaluated **real-time**
- Based on current config state for any group_id
- **Mandatory to pass** - absolutely required for functionality
- **Owned by**: Product Delivery Team and Partners
- Examples: Calendar configured, PCS domain configured, stage mapping defined

**2. Data Health Rules** 📊
- Ensure **data quality** of the instance
- Evaluated **once daily** (manual reload available)
- **Mandatory** for different product areas to function
- Examples: Employee has skills, positions have location, application data complete

**3. Operational Health Rules** ⚙️
- Runtime operational metrics
- System performance and reliability checks

---

## 📋 **Rule Documentation Format**

Each rule in the technical reference includes:

### Basic Information
- **Rule ID**: Unique identifier (e.g., "2.01", "employee_level_quality")
- **Rule Name**: Human-readable name
- **Product Area**: Talent Management, Talent Acquisition, or Talent Experience
- **Feature Mapping**: Which product feature this validates

### Technical Details
- **Rule Logic**: How the rule evaluates pass/fail (from actual codebase)
- **Configuration Schema**: The exact config structure being checked
- **Code Reference**: File path in Eightfold codebase
- **Confluence Reference**: Link to official documentation

### Practical Information
- **Description**: What the rule does and why it matters
- **Purpose**: Why this rule exists
- **Impact of Failure**: What breaks if this rule fails
- **Resolution Steps**: Exactly what to configure to make the rule pass

---

## 🎓 **The 136 New Rules Breakdown**

### AI/ML Rules (22 rules)
**Focus**: AI recommendation quality and data requirements

**Key Rules:**
- `internal_positions_calibrated_rule` - Positions must be calibrated for recommendations
- `internal_positions_with_location_rule` - Positions must have location for geo-matching
- `internal_positions_with_skills_rule` - Positions must have skills (minimum 1)
- `internal_positions_with_multiple_skills_rule` - Positions must have 3+ skills
- `employee_profile_completeness_rule` - Employee profiles must be complete
- `employee_skills_populated_rule` - Employees must have skills for matching
- `project_data_quality_rule` - Project data must be complete
- `course_catalog_completeness_rule` - Course catalog must be populated
- `role_library_quality_rule` - Role library must have complete definitions
- `mentor_matching_data_rule` - Mentor profiles must be complete

**Why These Matter:**
AI recommendations (jobs, learning, mentors) require high-quality, complete data. Missing or incomplete data leads to poor recommendations and low user engagement.

### Security Rules (20 rules)
**Focus**: Security configurations and data protection

**Key Rules:**
- `seo_configuration_rule` - SEO settings properly configured
- `custom_domain_ssl_rule` - Custom domains have valid SSL certificates
- `campaign_tracking_security_rule` - Campaign tracking configured securely
- `email_loopback_configured_rule` - Email loopback prevents spam
- `sync_failure_monitoring_rule` - Sync failures are monitored
- `data_retention_compliance_rule` - Data retention meets GDPR/CCPA requirements
- `password_policy_configured_rule` - Password policies meet security standards
- `mfa_enabled_rule` - Multi-factor authentication is enabled
- `api_rate_limiting_rule` - API rate limits configured
- `audit_logging_enabled_rule` - Audit logs are captured

**Why These Matter:**
Security and compliance are non-negotiable. These rules ensure instances meet enterprise security standards and regulatory requirements (GDPR, CCPA, SOC2).

### Analytics Data Quality Rules (56 rules)
**Focus**: Reporting and analytics data quality

**Key Rules:**
- `employee_level_quality` - Employees have proper level/band data
- `employee_department_quality` - Employees assigned to departments
- `application_source_quality` - Application sources are tracked
- `application_funnel_completeness` - Application funnel stages captured
- `position_requisition_mapping` - Positions mapped to requisitions
- `interview_feedback_completeness` - Interview feedback captured
- `offer_acceptance_tracking` - Offer acceptance tracked
- `time_to_hire_data_quality` - Time-to-hire metrics calculable
- `diversity_data_quality` - Diversity data captured for reporting
- `stage_mapping_completeness` - All stages mapped correctly

**Why These Matter:**
Analytics and reporting depend on complete, accurate data. Missing or incorrect data leads to wrong business decisions and broken dashboards.

### TIP/Integrations Rules (38 rules)
**Focus**: Integration health and data synchronization

**Key Rules:**
- `ats_sync_lag_rule` - ATS sync is current (not lagging)
- `hris_sync_lag_rule` - HRIS sync is current
- `webhook_delivery_success_rule` - Webhooks delivering successfully
- `custom_field_mapping_rule` - Custom fields mapped correctly
- `eeoc_field_mapping_rule` - EEOC/diversity fields mapped
- `position_sync_completeness_rule` - All positions syncing
- `candidate_sync_completeness_rule` - All candidates syncing
- `employee_sync_completeness_rule` - All employees syncing
- `integration_error_monitoring_rule` - Integration errors monitored
- `api_connectivity_rule` - API connectivity is stable

**Why These Matter:**
Integrations are the data pipeline. If ATS/HRIS sync breaks or lags, the platform has stale data, leading to incorrect recommendations and broken workflows.

---

## 🔍 **Key Concepts**

### Delivery Excellence (DE) Models

| Model | ID | Description |
|-------|-----|-------------|
| **Partner Led - Guided Excellence** | 50388 | Implementation led by partner (Deloitte, Accenture, etc.) with Eightfold guided oversight |
| **Partner Led - Core Excellence** | 50387 | Partner-led with standard oversight |
| **EF Led - Core Excellence** | 50389 | Eightfold-led implementation with internal delivery team |

### Implementation Phases

1. **Not Started** - Project created but work hasn't begun
2. **Initiate and Preview** - Discovery, kickoff, requirements gathering
3. **Design and Build** - Configuration, customization, integration development
4. **Test** - User acceptance testing (UAT), integration testing
5. **Launch** - Go-live preparation, cutover, production deployment
6. **Hypercare** - Post-launch monitoring and support (2-4 weeks)

### Checkpoints

| Checkpoint | Phase | Rules | Purpose |
|------------|-------|-------|---------|
| Checkpoint 1 | Initiate and Preview | 1 | Pre-project readiness (Talent Lake provisioned) |
| Checkpoint 2 | Design and Build | 11 | Core configuration validation |
| Checkpoint 3 | Design and Build / Test | 15+ | Data quality before testing |
| Checkpoint 4 | Test | 10+ | UAT readiness |
| Checkpoint 5 | Launch | 20+ | Go-live readiness |
| Checkpoint 6 | Hypercare | 5+ | Post-launch stability |

---

## 🛠️ **Python Tools for Rule Processing**

### Tool Overview

| Tool | Purpose | Usage |
|------|---------|-------|
| `process_new_136_rules.py` | Process and enhance 136 new rules with Cursor descriptions | `python tools/process_new_136_rules.py` |
| `enhance_all_rule_descriptions.py` | Enhance all rule descriptions with Purpose/Impact/Fix format | `python tools/enhance_all_rule_descriptions.py` |
| `enhance_rule_descriptions.py` | Enhance specific rule descriptions | `python tools/enhance_rule_descriptions.py` |
| `generate_cursor_descriptions.py` | Generate AI descriptions for rules | `python tools/generate_cursor_descriptions.py` |
| `apply_rule_refinements.py` | Apply rule refinements and updates | `python tools/apply_rule_refinements.py` |

### What These Tools Do

**process_new_136_rules.py:**
- Reads `new_rules_136_input.tsv`
- Generates enhanced descriptions using AI/templates
- Adds Config Reference, Code Reference paths
- Outputs `new_rules_136_with_enhanced_descriptions.tsv`

**enhance_all_rule_descriptions.py:**
- Processes all existing rules
- Adds "Purpose", "Impact", "To Fix" sections
- Improves clarity and actionability
- Updates technical reference documentation

---

## 📊 **Documentation Statistics**

| File | Lines | Purpose |
|------|-------|---------|
| `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` | 3,971 | Complete technical reference for all rules |
| `RAG_KNOWLEDGE_BASE.md` | 415 | AI domain knowledge for analysis |
| `RULE_VERIFICATION_REPORT.md` | 183 | Rule verification documentation |
| `TA_TM_PCS_product_health_rules_v2.tsv` | 173 | Latest consolidated rule descriptions |
| `new_rules_136_with_enhanced_descriptions.tsv` | 819 | 136 new rules with descriptions |
| `PCS_TM_TA_rules_with_cursor_descriptions.tsv` | 166 | 165 original rules enhanced |
| **TOTAL** | **5,727** | **Complete rule documentation set** |

---

## 🎓 **New Agent Checklist**

When working on rules documentation:

- [ ] **FIRST: Verify correct repository!** Run `git remote -v` - must show `mharrison-eightfold/instance_health_rules`
- [ ] Read this file (`RULES_CONTEXT_LOADER.md`)
- [ ] **For ANY rule query**: Read `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md` first
- [ ] **When learning new info**: Update `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`
- [ ] Understand: This is **separate from app development** (app code goes to DE_heath_report_app repository)
- [ ] Understand: 165 original rules + 136 new rules = 301 total documented rules
- [ ] Know the rule categories: Config Health, Data Health, Operational Health
- [ ] Know the 6 checkpoints and their purposes
- [ ] Understand: AI rules focus on recommendation quality
- [ ] Understand: Security rules focus on compliance and data protection
- [ ] Understand: Analytics rules focus on reporting data quality
- [ ] Understand: Integration rules focus on sync health
- [ ] Know where to find technical details: `INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md`
- [ ] Know where to find remediation guidance: `RAG_KNOWLEDGE_BASE.md`
- [ ] Understand: Each rule has Purpose, Impact, To Fix sections
- [ ] Know: Rules map to actual Eightfold codebase (`www/data_audit/platform_health/...`)
- [ ] Know: Rules link to Confluence documentation

---

## 🔗 **Key Confluence References**

- [Instance Health Documentation](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2190936431/Instance+Health) - Main rule creation guide
- [Platform Health Check](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2063663155/Platform+Health+Check) - How-to guide for SEs and PDMs
- [Product Go Live and Implementation Phase Management](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2402025554) - Phase management and thresholds
- [Analytics Data Quality - Ongoing Assurance](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2528608431) - Analytics data quality monitoring
- [Instance Health Exemption Request Process](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2997944353) - Exemption approval process

---

## 💡 **Key Principles**

1. **Rule Criterion**: Only add rules that are **absolutely required** for functionality (not "nice to have")
2. **Ownership**: Product Delivery Team and Partners responsible for 100% config health pass rate
3. **Documentation First**: Every rule must have clear Purpose, Impact, and To Fix guidance
4. **Confluence Integration**: Link to official documentation whenever possible
5. **Code Traceability**: Every rule maps to implementation in Eightfold codebase
6. **AI-Friendly**: Documentation structured for AI analysis and recommendations
7. **Actionable**: Focus on "what to do" not just "what's wrong"
8. **Living Documentation**: Update Technical Reference when new information is learned

---

## 🚀 **What's Next?**

### Potential Future Work

1. **Rule Automation**: Automate rule evaluation and reporting
2. **Integration with App**: Display rule failures in Implementation Health App
3. **AI Recommendations**: Use RAG knowledge base to generate fix recommendations
4. **Rule Versioning**: Track rule changes over time
5. **Customer-Facing Docs**: Convert technical reference to customer documentation
6. **Rule Templates**: Create templates for adding new rules
7. **Exemption Tracking**: Track rule exemptions and their justifications

---

**You're ready to work on rules documentation! 🚀**

For app development work, see: **[DE_heath_report_app repository](https://github.com/mharrison-eightfold/DE_heath_report_app)**

For running the app, see: [LOCAL_SETUP_GUIDE.md](https://github.com/mharrison-eightfold/DE_heath_report_app/blob/main/documentation/LOCAL_SETUP_GUIDE.md) in app repo

For design rules, see: [EIGHTFOLD_BRANDING_GUIDELINES.md](https://github.com/mharrison-eightfold/DE_heath_report_app/blob/main/documentation/EIGHTFOLD_BRANDING_GUIDELINES.md) in app repo
