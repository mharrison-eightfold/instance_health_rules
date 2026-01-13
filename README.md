# Instance Health Rules Documentation

**Comprehensive technical reference and AI knowledge base for Eightfold's Instance Health rules**

[![Repository](https://img.shields.io/badge/repo-instance__health__rules-blue)](https://github.com/mharrison-eightfold/instance_health_rules)
[![Rules](https://img.shields.io/badge/rules-300%2B-green)](documentation/INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md)
[![Last Updated](https://img.shields.io/badge/updated-January%202026-orange)](.)

---

## 📋 What Is This?

This repository contains **comprehensive documentation for 300+ Instance Health rules** used in the Eightfold Talent Intelligence Platform. These rules evaluate the health of customer instances before UAT handover and production go-live.

**Related Project**: [Implementation Health App](https://github.com/mharrison-eightfold/DE_heath_report_app) - The web application that uses these rules

---

## 🎯 Repository Contents

### 📚 Core Documentation (5,554 lines total)

| Document | Lines | Purpose |
|----------|-------|---------|
| **[RULES_CONTEXT_LOADER.md](documentation/RULES_CONTEXT_LOADER.md)** | 430 | **Start here!** Quick context for AI agents and contributors |
| **[INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md](documentation/INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md)** | 3,971 | Complete technical reference for Solution Architects |
| **[RAG_KNOWLEDGE_BASE.md](documentation/RAG_KNOWLEDGE_BASE.md)** | 415 | AI domain knowledge for analysis and recommendations |
| **[RULE_VERIFICATION_REPORT.md](documentation/RULE_VERIFICATION_REPORT.md)** | 183 | Rule verification and validation documentation |

### 📊 Rule Data Files

| File | Rules | Description |
|------|-------|-------------|
| **[new_rules_136_with_enhanced_descriptions.tsv](documentation/new_rules_136_with_enhanced_descriptions.tsv)** | 136 | AI, Security, Analytics, and Integration rules (enhanced) |
| **[PCS_TM_TA_rules_with_cursor_descriptions.tsv](documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv)** | 165 | Original PCS, TM, and TA rules (enhanced) |
| **[new_rules_136_input.tsv](documentation/new_rules_136_input.tsv)** | 136 | Raw input data for 136 new rules |
| **[instance_health_rules_input.tsv](documentation/instance_health_rules_input.tsv)** | 167 | Original rule input data |

### 🛠️ Python Tools

| Tool | Purpose |
|------|---------|
| **[process_new_136_rules.py](tools/process_new_136_rules.py)** | Process and enhance 136 new rules with AI descriptions |
| **[enhance_all_rule_descriptions.py](tools/enhance_all_rule_descriptions.py)** | Enhance all rule descriptions with Purpose/Impact/Fix format |
| **[enhance_rule_descriptions.py](tools/enhance_rule_descriptions.py)** | Enhance specific rule descriptions |
| **[generate_cursor_descriptions.py](tools/generate_cursor_descriptions.py)** | Generate AI descriptions for rules |
| **[apply_rule_refinements.py](tools/apply_rule_refinements.py)** | Apply rule refinements and updates |

---

## 🎓 The Rules

### Rule Categories (300+ total)

#### **Original Rules (165)**
- **Talent Management - Core Rules** (20+ rules)
- **Talent Management - Leader Experience Rules**
- **Talent Acquisition - Core Rules** (30+ rules)
- **Talent Acquisition - PCS Rules**
- **Configuration Rules** (40+ rules)
- **Data Quality Rules** (40+ rules)

#### **New Rules Added (136)**
- **AI/ML Recommendation Rules** (22 rules) - Position calibration, employee profiles, skills
- **Security Rules** (20 rules) - SSL, data retention, compliance, audit logs
- **Analytics Data Quality Rules** (56 rules) - Reporting data completeness and accuracy
- **TIP/Integrations Rules** (38 rules) - ATS/HRIS sync, webhooks, field mappings

### Rule Types

**🛠️ Config Health Rules**
- Lightweight, real-time evaluation
- Based on current configuration state
- **Mandatory to pass** - absolutely required for functionality
- Examples: Calendar configured, PCS domain set, stage mapping defined

**📊 Data Health Rules**
- Ensure data quality of the instance
- Evaluated once daily (manual reload available)
- Examples: Employees have skills, positions have location, applications complete

**⚙️ Operational Health Rules**
- Runtime operational metrics
- System performance and reliability checks

---

## 🚀 Quick Start

### For AI Agents
1. **Read**: [RULES_CONTEXT_LOADER.md](documentation/RULES_CONTEXT_LOADER.md) - Complete context in 430 lines
2. **Reference**: [INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md](documentation/INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md) - Deep technical details
3. **Understand**: [RAG_KNOWLEDGE_BASE.md](documentation/RAG_KNOWLEDGE_BASE.md) - Domain knowledge for recommendations

### For Solution Architects
1. **Technical Reference**: Complete rule documentation with config schemas and resolution steps
2. **Confluence Integration**: Links to official Eightfold documentation
3. **Code References**: Maps to actual implementation in Eightfold codebase

### For Developers
1. **Python Tools**: Use tools in `tools/` directory to process and enhance rules
2. **TSV Files**: Rule data in tab-separated format for easy parsing
3. **Extensible**: Add new rules following the established format

---

## 📖 Documentation Structure

### RULES_CONTEXT_LOADER.md
**Quick context guide** covering:
- What Instance Health Rules are
- The 136 new rules breakdown (AI, Security, Analytics, Integrations)
- Rule categories and ownership
- Checkpoints and phases
- Python tools usage
- Key concepts and terminology

### INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md
**3,971-line comprehensive reference** including:
- Architecture overview
- Rule types and ownership (Config vs Data vs Operational)
- Implementation phase requirements
- Detailed documentation for 165+ rules
- Configuration guides for all product areas
- Debugging and troubleshooting guides
- Code reference mappings
- Confluence documentation links

### RAG_KNOWLEDGE_BASE.md
**AI domain knowledge** providing:
- Delivery Excellence methodology
- Checkpoint-based implementation approach
- Key metrics (Pass Rate, Checkpoint Completion, Health Score)
- Common issues and remediation guides
- Best practices and recommendations

---

## 🎯 Use Cases

### 1. Solution Architects
**Troubleshoot failed rules during implementation**
- Look up rule in technical reference
- Review "What It Checks" and "Why It Matters"
- Follow "Resolution Steps" to fix configuration
- Reference Confluence docs for detailed guides

### 2. AI Systems
**Generate analysis and recommendations**
- Use RAG_KNOWLEDGE_BASE.md for domain context
- Reference rule descriptions for accurate analysis
- Generate fix recommendations based on rule documentation
- Provide checkpoint-specific guidance

### 3. Product Delivery Teams
**Validate instance health before handover**
- Check rule pass rates across checkpoints
- Identify which rules are failing
- Follow remediation guidance
- Track progress towards 100% pass rate

### 4. Product Managers
**Understand rule coverage and gaps**
- Review rule categories and product area coverage
- Identify areas needing new rules
- Understand rule impact on implementations
- Plan rule enhancements

---

## 🔗 Key Concepts

### Delivery Excellence Models

| Model | ID | Description |
|-------|-----|-------------|
| Partner Led - Guided Excellence | 50388 | Partner-led with Eightfold guided oversight |
| Partner Led - Core Excellence | 50387 | Partner-led with standard oversight |
| EF Led - Core Excellence | 50389 | Eightfold-led implementation |

### Implementation Phases

1. **Not Started** - Project created but work hasn't begun
2. **Initiate and Preview** - Discovery, kickoff, requirements
3. **Design and Build** - Configuration, customization, integrations
4. **Test** - UAT, integration testing
5. **Launch** - Go-live preparation, cutover, deployment
6. **Hypercare** - Post-launch monitoring (2-4 weeks)

### Checkpoints

| Checkpoint | Phase | Focus |
|------------|-------|-------|
| Checkpoint 1 | Initiate and Preview | Pre-project readiness |
| Checkpoint 2 | Design and Build | Core configuration |
| Checkpoint 3 | Design and Build / Test | Data quality |
| Checkpoint 4 | Test | UAT readiness |
| Checkpoint 5 | Launch | Go-live readiness |
| Checkpoint 6 | Hypercare | Post-launch stability |

---

## 🛠️ Using the Python Tools

### Process New Rules
```bash
python tools/process_new_136_rules.py
```
Reads `new_rules_136_input.tsv`, generates enhanced descriptions, outputs enhanced TSV.

### Enhance Rule Descriptions
```bash
python tools/enhance_all_rule_descriptions.py
```
Processes all rules, adds Purpose/Impact/Fix sections, updates technical reference.

### Generate AI Descriptions
```bash
python tools/generate_cursor_descriptions.py
```
Generates AI-powered descriptions for rules using templates and context.

---

## 📊 Rule Format

Each rule includes:

**Basic Information**
- Rule ID (e.g., "2.01", "employee_level_quality")
- Rule Name (human-readable)
- Product Area (TM, TA, or TX)
- Feature Mapping

**Technical Details**
- Rule Logic (how pass/fail is evaluated)
- Configuration Schema (exact config structure)
- Code Reference (file path in Eightfold codebase)
- Confluence Reference (official documentation link)

**Practical Information**
- Description (what and why)
- Purpose (rule objective)
- Impact of Failure (what breaks)
- Resolution Steps (how to fix)

---

## 🔗 Related Projects

- **[Implementation Health App](https://github.com/mharrison-eightfold/DE_heath_report_app)** - Web app using these rules
- **[Eightfold Platform](https://eightfold.ai)** - The platform these rules validate

---

## 📋 Confluence References

- [Instance Health Documentation](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2190936431/Instance+Health)
- [Platform Health Check How-To](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2063663155/Platform+Health+Check)
- [Product Go Live Management](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2402025554)
- [Analytics Data Quality Assurance](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2528608431)
- [Exemption Request Process](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2997944353)

---

## 🤝 Contributing

This repository documents Instance Health rules for the Eightfold platform. 

**To add or update rules:**
1. Update the appropriate TSV file
2. Run enhancement tools to generate descriptions
3. Update technical reference documentation
4. Submit PR with clear description of changes

---

## 📞 Questions or Issues?

- **Documentation Questions**: Check [RULES_CONTEXT_LOADER.md](documentation/RULES_CONTEXT_LOADER.md)
- **Technical Details**: See [INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md](documentation/INSTANCE_HEALTH_RULES_TECHNICAL_REFERENCE.md)
- **App Issues**: File in [Implementation Health App repo](https://github.com/mharrison-eightfold/DE_heath_report_app)

---

**Last Updated**: January 13, 2026  
**Maintained By**: Michael Harrison (@mharrison-eightfold)  
**Total Rules Documented**: 301 (165 original + 136 new)  
**Total Documentation**: 5,554 lines
