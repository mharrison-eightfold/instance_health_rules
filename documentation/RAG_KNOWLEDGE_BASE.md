# RAG Knowledge Base for AI Analysis & Recommendations

**Purpose**: This document provides domain knowledge for AI systems to generate accurate, actionable analysis and recommendations for Eightfold Implementation Health Reports.

---

## 1. OVERVIEW: Delivery Excellence Program

### What is Delivery Excellence?

Delivery Excellence (DE) is Eightfold's structured implementation methodology that ensures customers successfully deploy the Eightfold Talent Intelligence Platform. The program uses a checkpoint-based approach to validate that implementations meet quality standards at each phase.

### Delivery Excellence Models

Projects are categorized by implementation type:

| Model | ID | Description |
|-------|-----|-------------|
| **Partner Led - Guided Excellence** | 50388 | Implementation led by a partner (e.g., Deloitte, Accenture, nFormal, BCC) with Eightfold providing guided oversight and quality checkpoints |
| **Partner Led - Core Excellence** | 50387 | Partner-led implementation with standard Eightfold oversight |
| **EF Led - Core Excellence** | 50389 | Eightfold-led implementation with internal delivery team |

### Implementation Phases

Projects progress through these phases:

1. **Not Started** - Project created but work hasn't begun
2. **Initiate and Preview** - Discovery, kickoff, requirements gathering
3. **Design and Build** - Configuration, customization, integration development
4. **Test** - User acceptance testing (UAT), integration testing
5. **Launch** - Go-live preparation, cutover, production deployment
6. **Hypercare** - Post-launch monitoring and support (typically 2-4 weeks)

### Key Metrics

- **Pass Rate**: Percentage of health rules passing (Target: ≥80%, Excellence: ≥90%)
- **Checkpoint Completion**: Number of checkpoints with all rules passing
- **Health Score**: Overall project health based on rule pass rate

---

## 2. CHECKPOINTS & HEALTH RULES

### Checkpoint 1: Pre-project Readiness
**Phase**: Initiate and Preview
**Purpose**: Validate infrastructure and environment readiness before implementation begins

| Rule ID | Rule Name | Description | What It Checks | Why It Matters |
|---------|-----------|-------------|----------------|----------------|
| 1.03 | Talent Lake Provisioned | Talent Lake has been provisioned and is ready for data ingestion | Verifies the Eightfold data lake infrastructure is set up for the customer instance | Without Talent Lake, no candidate/employee data can be ingested or processed. This is a blocking prerequisite for all downstream work. |

**When 1.03 Fails - Remediation**:
- Contact Eightfold Infrastructure team to provision Talent Lake
- Verify AWS/cloud resources are allocated for the customer
- Check that the instance (sandbox) has been properly created in Eightfold's systems
- Typical resolution time: 1-3 business days

---

### Checkpoint 2: Design Review
**Phase**: Design and Build
**Purpose**: Validate core configurations are properly set up before build phase

| Rule ID | Rule Name | Description | What It Checks | Why It Matters |
|---------|-----------|-------------|----------------|----------------|
| 2.01 | Default Calendar Configured | Default calendar provider has been configured for scheduling | Checks if calendar integration (Google, Outlook, etc.) is set up in `scheduling_config` | Required for interview scheduling functionality. Candidates and recruiters can't schedule interviews without this. |
| 2.02 | Job Req Templates Configured | All job requisition templates are properly mapped in stage transitions | Validates that requisition templates have proper stage transition mappings | Affects candidate pipeline visibility and workflow automation. Broken mappings cause candidates to get "stuck" in stages. |
| 2.03 | Hired Stage Defined | Hired stage has been defined in the candidate stage map | Checks that a "Hired" stage exists in the stage mapping configuration | Critical for reporting and analytics. Without a defined hired stage, conversion metrics and time-to-hire can't be calculated. |
| 2.04 | Referral Source Mapping | Referral sources are properly configured in application sources | Validates referral source IDs are set up in applicant source configuration | Enables tracking of referral program effectiveness. Without this, referral attribution is lost. |
| 2.05 | PCS Domain Configured | Personalized Career Site domain has been configured | Checks if the PCSX (Personalized Career Site) domain is registered | Required for the customer's external career site. Without this, candidates can't apply through the career site. |
| 2.06 | Employee Hiring Bands | Employee hiring bands have been configured for internal mobility | Validates hiring bands are set up for employees in the internal mobility configuration | Enables internal mobility matching. Without hiring bands, employees can't be matched to internal opportunities based on level. |
| 2.07 | Job Bands Configured | Job bands have been defined and configured in the system | Checks that job band classifications exist in the system | Required for job-to-candidate matching and skills-based recommendations. |
| 2.08 | Hiring Band Equivalence | Hiring band equivalence mappings have been established | Validates that hiring band equivalence relationships are defined | Enables cross-level matching (e.g., a Level 5 employee can be matched to Level 4-6 roles). |
| 2.09 | Data Retention Configured | Data retention policies have been configured per compliance requirements | Checks data retention settings meet compliance requirements | Legal/compliance requirement. GDPR, CCPA, and other regulations require proper data retention configuration. |
| 2.10 | Integration Systems Connected | ATS and other integration systems have been connected | Validates ATS configuration is present in `ats_config` namespace | Required for candidate data flow from external ATS systems (Workday, SAP, etc.). |
| 2.11 | Navbar Logo Configured | Navigation bar logo has been uploaded and configured | Checks if customer branding (navbar logo) is applied | Affects user experience and customer branding requirements. |

**Common Checkpoint 2 Issues**:

1. **Calendar Not Configured (2.01)**:
   - Work with customer IT to obtain calendar API credentials
   - Configure OAuth for Google Workspace or Microsoft 365
   - Test calendar connectivity in sandbox before production

2. **Stage Mapping Issues (2.02, 2.03)**:
   - Review customer's hiring workflow to understand stages
   - Map customer stages to Eightfold standard stages
   - Ensure "Hired" stage is explicitly defined (not assumed)

3. **PCS Domain Issues (2.05)**:
   - Customer must provide domain (e.g., careers.customer.com)
   - DNS configuration required (CNAME record)
   - SSL certificate provisioning may take 24-48 hours

---

### Checkpoint 3: Build Review
**Phase**: Design and Build / Test
**Purpose**: Validate data quality and core functionality before testing

| Rule ID | Rule Name | Description | What It Checks | Why It Matters |
|---------|-----------|-------------|----------------|----------------|
| 3.01 | Employee Location Data Quality | 95%+ of employees have location information populated | Checks percentage of employee records with location data | Location is critical for job matching (remote vs. on-site) and compliance (work authorization by location). |
| 3.02 | Employee Mobility Levels | 95%+ of employees have mobility levels configured | Validates employee level assignments in internal mobility config | Required for internal mobility matching based on career level progression. |
| 3.03 | PCS Enabled | Personalized Career Site is enabled and functional | Verifies PCS is actively enabled and operational | Career site must be live for external candidates to apply. |
| 3.04 | SSO Configured | Single Sign-On has been configured with entity ID and ACS URL | Checks SSO configuration in `sso_config` namespace | Required for secure employee/recruiter access. Most enterprises require SSO for compliance. |
| 3.05 | Position Hiring Band Data Quality | 95%+ of positions have hiring_band information populated | Validates position records have hiring band assignments | Affects job-to-candidate matching accuracy. Positions without bands can't be matched properly. |
| 3.06 | Role Levels in Mobility Config | Role levels are properly configured in internal mobility settings | Checks role level configuration completeness | Enables career pathing and internal mobility recommendations. |

**Data Quality Standards**:
- **95% threshold**: Industry standard for data quality in HR systems
- Records below threshold should be flagged for data remediation
- Common causes: Legacy data migration issues, incomplete integrations

**SSO Configuration (3.04) Details**:
- Requires: Entity ID, ACS URL, IdP Certificate
- Common providers: Okta, Azure AD, Ping Identity, OneLogin
- Test thoroughly in sandbox before production cutover

---

### Checkpoint 4: Pre-cutover Review
**Phase**: Test / Launch
**Purpose**: Final validation before production go-live

| Rule ID | Rule Name | Description | What It Checks | Why It Matters |
|---------|-----------|-------------|----------------|----------------|
| 4.01 | Notification Rules Configured | Email notification rules and domains have been configured | Validates email configuration in `email_config` namespace | Ensures candidates and employees receive system notifications (application confirmations, interview invites, etc.) |

**Email Configuration Checklist**:
- Reply-to domain configured
- Send-from domain configured
- SPF/DKIM records set up for email deliverability
- Email templates customized with customer branding
- Test emails sent and verified

---

## 3. EIGHTFOLD PLATFORM TERMINOLOGY

### Core Products

| Term | Full Name | Description |
|------|-----------|-------------|
| **TA** | Talent Acquisition | External hiring and recruitment module |
| **TM** | Talent Management | Internal employee development and performance module |
| **TD** | Talent Design | Workforce planning and org design module |
| **RM** | Resource Management | Contingent workforce and project staffing module |
| **PCS** | Personalized Career Site | External-facing career site for candidates |
| **PCSX** | Personalized Career Site Extended | Enhanced career site with AI-powered recommendations |
| **TT** | Talent Transformation | Large-scale workforce transformation programs |

### Technical Terms

| Term | Description |
|------|-------------|
| **Talent Lake** | Eightfold's unified data lake for candidate and employee data |
| **Group ID** | Unique identifier for a customer instance (sandbox or production) |
| **Sandbox Group ID** | The development/test environment identifier |
| **Stage Map** | Configuration mapping customer hiring stages to Eightfold stages |
| **Hiring Bands** | Job level classifications (e.g., IC1-IC5, M1-M3) |
| **Internal Mobility** | Features enabling employees to find internal opportunities |
| **ATS** | Applicant Tracking System (external systems like Workday, SAP) |

### Implementation Terms

| Term | Description |
|------|-------------|
| **SOW** | Statement of Work - Contract defining implementation scope |
| **Go-Live Date** | Target date for production deployment |
| **Hypercare** | Post-launch support period (typically 2-4 weeks) |
| **Cutover** | The transition from sandbox to production |
| **UAT** | User Acceptance Testing |
| **Checkpoint** | Quality gate validating implementation readiness |

---

## 4. ANALYSIS GUIDELINES

### Health Status Thresholds

| Pass Rate | Status | Color | Interpretation |
|-----------|--------|-------|----------------|
| ≥90% | Excellent | Green | Exceeds delivery standards, on track for successful go-live |
| 75-89% | Good | Yellow | Meets basic standards but needs attention on specific items |
| 60-74% | Fair | Orange | Moderate risk, several areas need remediation |
| <60% | At Risk | Red | Critical attention needed, escalation recommended |

### Severity Classification

**Critical Issues** (Address Immediately):
- Blocking go-live (e.g., no Talent Lake, no SSO)
- Compliance risk (e.g., data retention not configured)
- Customer-facing functionality broken (e.g., career site down)

**High Priority** (Address This Week):
- Data quality below 95% threshold
- Missing integrations
- Incomplete stage mappings

**Medium Priority** (Address Before Go-Live):
- Branding/customization items
- Non-blocking configuration gaps
- Documentation incomplete

**Low Priority** (Address During Hypercare):
- Nice-to-have enhancements
- Optimization opportunities
- Training follow-ups

---

## 5. RECOMMENDATION TEMPLATES

### For Failed Health Rules

**Template: Rule Failure Recommendation**
```
Title: [Action] - [Rule Name]
Priority: [high/medium/low]
Category: [Remediation/Configuration/Data Quality/Process]
Description: [What failed and why it matters]
Actions:
1. [Specific first step]
2. [Second step]
3. [Verification step]
4. [Documentation step]
```

### Example Recommendations by Rule Type

**Talent Lake Not Provisioned (1.03)**:
```
Title: Provision Talent Lake Infrastructure
Priority: high
Category: Infrastructure
Description: Talent Lake has not been provisioned for this instance. 
             This is a blocking issue - no data processing can occur without it.
Actions:
1. Open infrastructure ticket with Eightfold Platform team
2. Provide customer instance details and go-live timeline
3. Verify provisioning complete via health check
4. Test data ingestion with sample records
```

**SSO Not Configured (3.04)**:
```
Title: Complete SSO Configuration
Priority: high
Category: Security
Description: Single Sign-On is not configured. Users cannot securely 
             access the platform. This is typically a launch blocker.
Actions:
1. Obtain SAML metadata from customer IdP (Okta, Azure AD, etc.)
2. Configure Entity ID and ACS URL in Eightfold admin
3. Test SSO login flow with customer IT team
4. Document SSO configuration for support handoff
```

**Data Quality Below 95% (3.01, 3.05)**:
```
Title: Remediate [Field] Data Quality
Priority: medium
Category: Data Quality
Description: [Field] data is below 95% population threshold. 
             This affects [matching/reporting/compliance].
Actions:
1. Generate report of records missing [field] data
2. Identify source of missing data (integration vs. legacy)
3. Work with customer to provide missing data via bulk update
4. Re-run health check to verify improvement
```

---

## 6. CONTEXTUAL ANALYSIS FACTORS

### Consider These When Analyzing Projects

1. **Phase Context**:
   - Early phase (Initiate): Focus on infrastructure and planning
   - Mid phase (Design/Build): Focus on configuration and data quality
   - Late phase (Test/Launch): Focus on completeness and go-live readiness

2. **Go-Live Proximity**:
   - >30 days out: Standard priority on all items
   - 15-30 days out: Escalate any medium+ items
   - <15 days out: Critical attention on any open items

3. **Partner vs. EF-Led**:
   - Partner-led: More guidance and oversight recommended
   - EF-led: Assume internal expertise, focus on blockers

4. **Project Complexity**:
   - Single module (TA only): Faster resolution expected
   - Multi-module (TA+TM+TD): More dependencies, longer remediation

5. **Customer Type**:
   - Enterprise: Higher compliance requirements, more stakeholders
   - Mid-market: Faster decisions, simpler configurations

### Comment Analysis Keywords

Look for these indicators in JIRA comments:

**Positive Signals**:
- "completed", "tested", "verified", "approved"
- "on track", "ahead of schedule"
- "customer sign-off", "UAT passed"

**Warning Signals**:
- "blocked", "waiting on", "dependency"
- "delayed", "pushed", "rescheduled"
- "issue", "problem", "concern"

**Risk Signals**:
- "escalation", "critical", "urgent"
- "scope change", "CR" (change request)
- "resource constraint", "bandwidth"

---

## 7. COMMON FAILURE PATTERNS

### Pattern 1: Data Quality Issues
**Symptoms**: Rules 3.01, 3.02, 3.05, 3.06 failing
**Root Cause**: Incomplete data migration from legacy systems
**Recommendation**: 
- Generate missing data report
- Work with customer HRIS team on data enrichment
- Consider phased approach with data quality improvements post-go-live

### Pattern 2: Integration Gaps
**Symptoms**: Rules 2.01, 2.10, 4.01 failing
**Root Cause**: Pending IT approvals or credentials
**Recommendation**:
- Escalate to customer project sponsor
- Identify backup/manual workarounds for go-live
- Document integration as post-go-live enhancement

### Pattern 3: Configuration Incomplete
**Symptoms**: Multiple Checkpoint 2 rules failing
**Root Cause**: Requirements not finalized or miscommunication
**Recommendation**:
- Schedule configuration workshop with customer
- Review requirements documentation
- Assign dedicated SA for configuration completion

### Pattern 4: SSO/Security Blockers
**Symptoms**: Rule 3.04 failing close to go-live
**Root Cause**: Customer IT processes slow
**Recommendation**:
- Escalate to customer CIO/CISO level
- Propose temporary bypass (if acceptable to customer)
- Set hard deadline for SSO completion

---

## 8. SUCCESS CRITERIA

### Go-Live Readiness Checklist

A project is ready for go-live when:

1. **All Checkpoint rules pass** (100% pass rate ideal, ≥90% acceptable)
2. **SSO tested and verified** (no password-based access in production)
3. **Career site live and accessible** (if TA module deployed)
4. **Email notifications working** (test emails received)
5. **Data quality ≥95%** for key fields
6. **UAT sign-off obtained** from customer
7. **Hypercare plan documented** and resources assigned
8. **Runbook created** for common support scenarios

### Excellence Indicators

Projects demonstrating excellence show:
- 95%+ pass rate throughout implementation
- Proactive identification of issues (not reactive)
- Strong customer engagement and communication
- Documentation complete and thorough
- Lessons learned captured for future projects

---

## 9. APPENDIX: JIRA Field Mappings

### Key Custom Fields

| Field ID | Field Name | Description |
|----------|------------|-------------|
| customfield_10142 | Customer | Customer account name |
| customfield_10366 | SOW/Template Type | Statement of Work identifier |
| customfield_10613 | Phase | Current implementation phase |
| customfield_10617 | Go-Live Date | Target production deployment date |
| customfield_10646 | Sandbox Group ID | Development instance identifier |
| customfield_10666 | Delivery Excellence Model | Project type (Partner Led, EF Led, etc.) |
| customfield_10791 | Project EM | Engagement Manager assigned |
| customfield_10436 | Project SA | Solution Architect assigned |
| customfield_10227 | CSM Owner | Customer Success Manager |
| customfield_10487 | DE Functional Reviewer | Delivery Excellence functional reviewer |
| customfield_11024 | DE Technical Reviewer | Delivery Excellence technical reviewer |
| customfield_13787 | DE Program Manager | Delivery Excellence program manager |

---

## 10. VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial RAG knowledge base created |

---

**End of RAG Knowledge Base**

