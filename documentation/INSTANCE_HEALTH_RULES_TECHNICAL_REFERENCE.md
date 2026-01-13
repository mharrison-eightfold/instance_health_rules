# Instance Health Rules - Technical Reference Guide

**Version:** 2.1  
**Generated:** January 12, 2026  
**Purpose:** Comprehensive technical reference for Solution Architects and Functional Consultants to understand and resolve Instance Health rule failures.

### Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | January 12, 2026 | Added Confluence documentation integration; Enhanced rule details with official Confluence references; Added Config Health Recommendation Framework; Updated Implementation Phase Management with exemption process; Enhanced Stage Mapping Guide with debugging workflow; Added Career Navigator configuration; Expanded Analytics Data Quality documentation |
| 2.0 | January 8, 2026 | Initial comprehensive technical reference |

---

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Rule Types and Ownership](#rule-types-and-ownership)
4. [Implementation Phase Requirements](#implementation-phase-requirements)
5. [Talent Management - Core Rules](#talent-management---core-rules)
6. [Talent Management - Leader Experience Rules](#talent-management---leader-experience-rules)
7. [Talent Acquisition - Core Rules](#talent-acquisition---core-rules)
8. [Talent Acquisition - PCS Rules](#talent-acquisition---pcs-rules)
9. [PCS Configuration Guide](#pcs-configuration-guide)
10. [Configuration Schema Reference](#configuration-schema-reference)
11. [Career Hub Configuration Guide](#career-hub-configuration-guide)
12. [Pipeline & Workflow Configuration](#pipeline--workflow-configuration)
13. [Diversity Configuration Guide](#diversity-configuration-guide)
14. [Event Recruiting Configuration](#event-recruiting-configuration)
15. [Communities Configuration](#communities-configuration)
16. [Profile Masking Configuration](#profile-masking-configuration)
17. [Stage Mapping Guide](#stage-mapping-guide)
18. [Debugging Data Quality Issues](#debugging-data-quality-issues)
19. [Scheduling Configuration Guide](#scheduling-configuration-guide)
20. [Calibration Configuration Guide](#calibration-configuration-guide)
21. [Internal Mobility Configuration Guide](#internal-mobility-configuration-guide)
22. [Succession Planning Configuration Guide](#succession-planning-configuration-guide)
23. [Stage Transition Map Configuration](#stage-transition-map-configuration)
24. [Interview Feedback Configuration Guide](#interview-feedback-configuration-guide)
25. [Communication Configuration Guide](#communication-configuration-guide)
26. [Config Health Recommendation Framework](#config-health-recommendation-framework)
27. [AI/ML Recommendation Rules](#aiml-recommendation-rules)
28. [Security Rules](#security-rules)
29. [Analytics Data Quality Rules](#analytics-data-quality-rules)
30. [Integrations Rules](#integrations-rules)
31. [Talent Intelligence Platform Rules](#talent-intelligence-platform-rules)
32. [Code Reference Guide](#code-reference-guide)

---

## Introduction

Instance Health is accessed in Admin Console at `/integrations/implementation_health`. It is a tool to evaluate the health of any instance (group_id) before handover for UAT on sandbox or for Go-live and prod cutover.

This document provides a deep technical reference for each Instance Health rule. For each rule, you will find:

- **Rule ID**: The unique identifier used in the platform
- **Feature Mapping**: Which product feature this rule validates
- **Rule Logic**: How the rule evaluates pass/fail (from actual codebase)
- **Configuration Schema**: The exact config structure being checked
- **Technical Description**: What the rule does and why it matters
- **Resolution Steps**: Exactly what to configure to make the rule pass

**Confluence References**:
- [Instance Health Documentation](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2190936431/Instance+Health) - Main rule creation guide
- [Platform Health Check](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2063663155/Platform+Health+Check) - How-to guide for SEs and PDMs
- [Product Go Live and Implementation Phase Management](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2402025554) - Phase management and thresholds
- [Analytics Data Quality - Ongoing Assurance](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2528608431) - Analytics data quality monitoring
- [Instance Health Exemption Request Process](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2997944353) - Exemption approval process

---

## Architecture Overview

### Rule Evaluation Framework

Health rules are evaluated by the Platform Health system located in:
```
www/data_audit/platform_health/
├── data_health/               # Data quality rules (Solr/Analytics based)
├── config_health/             # Configuration validation rules
├── operational_health/        # Runtime operational metrics
└── platform_health_base.py    # Base classes and preconditions
```

### Rule Metadata Configuration

Rules are configured in `platform_health_base_config` with the following structure:

```python
# platform_health_base_config -> implementation_quality -> {feature_id}
{
    "feature_id": {
        "display_name": "Feature Name",
        "product_area": "Talent Management",  # or "Talent Acquisition", "Talent Experience"
        "linked_rules": [
            {
                "rule_id": "employee_level_quality",
                "rule_type": "data"  # or "config", "operational"
            }
        ]
    }
}
```

### Rule Handler Classes

| Handler Class | Purpose | Usage |
|---------------|---------|-------|
| `ProductConfigHealthFieldExistsRule` | Checks if a config field exists | Simple field presence checks |
| `ProductConfigHealthCompareValueRule` | Compares field to expected value | Boolean/value validation |
| `ProductConfigHealthTemplateRule` | Evaluates Jinja templates | Complex multi-field logic |
| `ProductConfigHealthListSizeRule` | Validates list/array size | Minimum items required |
| `GateEnabledRule` | Checks if a gate is enabled | Feature flag validation |
| `SolrBaseRule` | Queries Solr for data quality | Employee/Position data rules |
| `AnalyticsBaseRule` | Queries Redshift analytics | Historical data quality |

---

## Rule Types and Ownership

### Config Health Rules

Config rules are **lightweight rules** evaluated **real-time** based on the current state of config for any group_id.

#### Rule Criterion
All rules in config health are **mandatory to pass**. Only add rules which are **absolutely required** for functionality to work without business impact. **Not "nice to have"**.

#### Rule Ownership
**Product Delivery Team and Partners** are responsible to make sure all config health rules pass 100%.

Example config rule definition:
```json
{
    "employee_engagement_enabled": {
        "config": "career_hub_profile_config",
        "field_path": "product_configs.employee.employee_engagement_enabled",
        "display_name": "Employee Engagement Enabled",
        "description": "This determines if employee engagement in careerhub is enabled or not",
        "failure_text": "Employee engagement is not enabled"
    }
}
```

### Data Health Rules

Data rules ensure the **data quality** of the instance. These rules are **mandatory** for different product areas to function properly. They are **evaluated once daily** (use "Reload" button for manual re-evaluation).

#### Rule Criterion
All rules in data health are **mandatory to pass**. Only add rules which are **absolutely required** for functionality to work without business impact.

#### Rule Ownership
**Data Ingestion Team and SAs Implementation Team** are responsible to make sure all data health rules pass 100%.

#### Platform Health Metrics Display
Data Health Check Rules provide detailed insight into calculation methodology. For example:
- **Business Unit on Positions**: Shows positions with/without Business Unit values and calculates percentage against threshold
- **Hiring Band on Positions**: Shows positions with/without Hiring Band values
- Threshold is typically **95%** - rules fail below this threshold

#### How Data Rules Are Defined in Code
Data rules are defined in `www/data_audit/platform_health/data_health/data_health_evaluation_rules.py`:

```python
'employee_manager_email_quality': {
    'constructor_args': {
        'solr_fq_term': 'profile.data_json.employee.manager_email:[* TO *]',
        'metric_threshold': 95,
        'include_alumni': False,
    },
    'field_name': 'manager_email',
    'base_class': EmployeeDataSolrBaseRule,
    'metric_types': [AuditMetricType.PRODUCT_DATA_HEALTH, AuditMetricType.DATA_HEALTH]
}
```

Key parameters:
- **solr_fq_term**: Filter query for desired results (numerator)
- **metric_threshold**: Rule fails if threshold is below this number
- **base_class**: Either `SolrBaseRule` or `AnalyticsBaseRule`
- **metric_types**: `AuditMetricType.DATA_HEALTH` for Instance Health, `AuditMetricType.PRODUCT_DATA_HEALTH` for Platform Health

#### Data Rule Metrics Publication
Metrics are published daily by: `scripts/airflow/dags-common/dag_implementation_quality_audit.py`

View published rules: **DB Explorer > data_audit_log** table

Example data rule definition:
```python
'employee_manager_email_quality': {
    'constructor_args': {
        'solr_fq_term': 'profile.data_json.employee.manager_email:[* TO *]',
        'metric_threshold': 95,
        'include_alumni': False,
    },
    'field_name': 'manager_email',
    'base_class': EmployeeDataSolrBaseRule,
    'metric_types': [AuditMetricType.PRODUCT_DATA_HEALTH, AuditMetricType.DATA_HEALTH]
}
```

### Operational Health Rules

Operational health rules monitor **system health** across Core Platform, Talent Management, PCS, and Talent Acquisition for data integrations.

#### Rule Criterion
All rules in operational health are **mandatory to pass**. If a rule is only required in certain scenarios, use **preconditions** to ensure the rule doesn't show for instances where it's not mandatory.

#### Rule Ownership
**Eightfold Engineering Team** is responsible to make sure all operational health rules pass 100%.

---

## Implementation Phase Requirements

### Phase Transition Flow

**Sandbox Environment:**
```
Implementation → User Acceptance Testing → Prod Cutover
```

**Production Environment:**
```
Implementation → Prod Cutover → Go Live
```

### Implementation Banner
A newly provisioned customer at the beginning will initialize products in Implementation Phase. Until the module reaches its final phase, a banner displays at the top indicating the product is still under Implementation.

### Health Score Thresholds

| Phase Transition | Config Health Score | Overall Health Score |
|------------------|---------------------|---------------------|
| Sandbox → UAT | **100%** | **85%** |
| Sandbox → Prod Cutover | **100%** | **85%** |
| Production → Prod Cutover | **100%** | **85%** |
| Production → Go Live | **100%** | **100%** |

### Phase Management

**Gate Control:** `manage_implementation_phase_gate`
**Configs:** `product_setup_config` and `release_preferences_config`

The phase is managed in `release_preferences_config` under `implementation_phase_states`:
```json
{
    "implementation_phase_states": {
        "talent_acquisition": "implementation_phase",
        "talent_management": "uat_phase",
        "pcs": "go_live"
    }
}
```

### Key Handler Methods

The `ProductImplementationPhaseHandler` class exposes these important methods:

| Method | Description |
|--------|-------------|
| `is_phase_implementation_managed` | Indicates if phase implementation is managed |
| `show_implementation_phase_for_product_banner` | Whether to display the banner for a given product |
| `is_module_live` | Returns false if phase is not Go Live (prod) or Prod Cutover (sandbox) |

### Instance Health Exemption Process

All Instance Health exemption requests must be:
1. **Documented in Jira** (issue type = "action item")
2. **Reviewed by appropriate regional Solution Delivery team**

**For Americas (AMER):** Email to Kim Corley, Catie Ray, Sandeep Gogineni
**For EMEA/APAC:** Email to David Kennedy, Rob Ryan, Carolyn McLellan

**Confluence References**: 
- [Product Go Live and Implementation Phase Management](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2402025554)
- [Instance Health Exemption Request Process](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2997944353)

---

## Talent Management - Core Rules

### employee_level_quality

**Feature Mapping:** Core Talent Management (Employee Profiles)  
**Data Source:** Solr  
**Threshold:** 95%

#### Rule Logic (from codebase)
```python
# www/data_audit/platform_health/data_health/data_health_evaluation_rules.py
'employee_level_quality': {
    'constructor_args': {
        'solr_fq_term': 'profile.data_json.employee.level:[* TO *]',
        'metric_threshold': 95,
    },
    'field_name': 'level',
    'base_class': EmployeeDataSolrBaseRule,
}
```

#### Configuration Schema
The `level` field is populated from employee data ingestion:
```json
{
  "employee": {
    "level": "Senior",           // Job level/band
    "hiring_date": "2023-01-15",
    "business_unit": "Engineering",
    ...
  }
}
```

#### Technical Description
This rule queries the Solr employee index to determine what percentage of active employees have a `level` field populated in their profile. The level field is critical for:

1. **Career Navigator**: Determines which roles are appropriate targets based on seniority
2. **Internal Mobility**: Filters job recommendations by eligible hiring bands
3. **Succession Planning**: Identifies bench strength at each level
4. **Matching**: Calibrates employee-to-role matching by seniority

The rule passes if ≥95% of employees have a non-null level value.

#### Resolution Steps
1. **Navigate to**: Admin Console → Data Management → Employee Sync
2. **Verify mapping**: Ensure the source system's level/grade field is mapped to `employee.level`
3. **Run re-sync**: Trigger a full employee data sync to populate missing values
4. **Validate**: Check a sample of employee profiles to confirm level is displaying

---

### employee_location_quality

**Feature Mapping:** Core Talent Management (Employee Profiles)  
**Data Source:** Analytics/Redshift  
**Threshold:** 95%

#### Rule Logic
```python
'employee_location_quality': {
    'constructor_args': {
        'count_query_term': f'location is not null and lower(trim(location)) not in {NULL_VALUES}',
        'min_threshold': 95,
    },
    'base_class': EmployeeDataAnalyticsBaseRule,
}
# NULL_VALUES = ['undefined', 'unknown', 'none', 'null', '', '0', 'n/a']
```

#### Technical Description
Queries the analytics employee view to count employees with valid location data. Location is used for:

- Geo-based job recommendations
- Location filtering in search
- Workforce analytics by geography
- Determining remote/hybrid eligibility

#### Resolution Steps
1. **Check data mapping**: Verify location field mapping in employee sync configuration
2. **Review source data**: Ensure location values aren't null/empty in source system
3. **Standardize values**: Replace invalid values ('N/A', 'Unknown') with actual locations
4. **Re-sync employees**: Run full sync after mapping corrections

---

### employee_levels_in_internal_mobility_config_quality

**Feature Mapping:** Internal Mobility  
**Data Source:** Solr with config lookup  
**Threshold:** 95%

#### Rule Logic
```python
'employee_levels_in_internal_mobility_config_quality': {
    'constructor_args': {
        'solr_fq_term': '{{employee_level_in_ijp_levels_filter}}',
        'metric_threshold': 95
    },
    'base_class': EmployeeDataSolrBaseRule,
}

# The template resolves to:
def get_template_variables(self, group_id):
    return {
        'employee_level_in_ijp_levels_filter': search_utils.field_search(
            'profile.data_json.employee.level',
            user_login.get_import_user(group_id).get_ijp_config('job_bands', [])
        ) or '-*:*'
    }
```

#### Configuration Schema
```json
// ijp_config::{group_id}
{
  "job_bands": [
    "Entry Level",
    "Associate", 
    "Senior",
    "Lead",
    "Manager",
    "Director",
    "VP",
    "Executive"
  ],
  "hiring_band_equivalence": {
    "individual_contributor": ["Entry Level", "Associate", "Senior", "Lead"],
    "management": ["Manager", "Director", "VP", "Executive"]
  },
  "filter_by_hiring_band": true,
  "tenure_eligibility_years": 1
}
```

#### Technical Description
This rule validates that employee `level` values match the levels defined in the Internal Mobility (`ijp_config`) configuration. It ensures:

1. Employee levels align with the organization's defined job band hierarchy
2. Internal mobility eligibility can be properly calculated
3. Career pathing and job recommendations work correctly

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → Internal Mobility
2. **Review job_bands**: Ensure all employee levels exist in the `job_bands` array
3. **Export employee levels**: Run a report of distinct employee levels
4. **Add missing bands**: Add any employee levels not in the job_bands list
5. **Alternative**: Standardize employee level data to match existing bands

---

### employee_hiring_bands

**Feature Mapping:** Core Talent Management  
**Config Location:** `ijp_config`

#### Rule Logic
```python
# Checks if job_bands array is configured
def _get_job_bands(self, group_id):
    return user_login.get_import_user(group_id).get_ijp_config('job_bands', [])

def should_run(self, group_id, system_id):
    return super().should_run(group_id, system_id) and self._get_job_bands(group_id)
```

#### Configuration Schema
```json
// ijp_config::{group_id}
{
  "job_bands": ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"],
  ...
}
```

#### Technical Description
Validates that job bands (hiring bands) are configured for the organization. Job bands define the hierarchical levels used for:

- Internal mobility eligibility
- Job recommendation filtering
- Career pathing boundaries
- Succession planning level grouping

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → Internal Mobility
2. **Configure job_bands**: Add all organizational job levels in order from entry to executive
3. **Define equivalences**: Optionally configure `hiring_band_equivalence` for related levels
4. **Enable filtering**: Set `filter_by_hiring_band: true` if band-based filtering is desired

---

### hiring_band_equivalence

**Feature Mapping:** Internal Mobility  
**Config Location:** `ijp_config`

#### Rule Logic
```python
# Checks hiring_band_equivalence configuration
equivalent_bands = self.get_ijp_config('hiring_band_equivalence', {})
```

#### Configuration Schema
```json
{
  "hiring_band_equivalence": {
    "entry": ["L1", "L2"],
    "mid": ["L3", "L4"],
    "senior": ["L5", "L6"],
    "leadership": ["L7", "L8"]
  }
}
```

#### Technical Description
Hiring band equivalences group multiple job bands that should be treated as equivalent for mobility purposes. For example, an L3 employee might be eligible to apply for both L3 and L4 positions if they're in the same equivalence group.

Used by:
- Internal job eligibility calculations
- Mentor matching by level
- Succession planning pool sizing

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → Internal Mobility
2. **Define groups**: Create logical groupings of job bands
3. **Order matters**: Ensure bands within each group are listed in seniority order

---

### filter_by_hiring_band

**Feature Mapping:** Internal Mobility  
**Config Location:** `ijp_config`

#### Rule Logic
```python
def should_filter_by_job_bands(self):
    return bool(
        career_planner_config.get('career_planner_filter_by_job_band', False) or 
        (self.get_ijp_config('filter_by_hiring_band', default=False) and 
         self.get_ijp_config('job_bands'))
    )
```

#### Technical Description
Controls whether job recommendations are filtered by hiring band eligibility. When enabled, employees only see jobs within their eligible band range (typically current band ± configured offset).

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → Internal Mobility
2. **Enable filter**: Set `filter_by_hiring_band: true`
3. **Prerequisite**: Ensure `job_bands` and `hiring_band_equivalence` are configured

---

### upskilling_display_config

**Feature Mapping:** Skills Development / Upskilling  
**Config Location:** `career_hub_base_config`

#### Rule Logic
```python
# Checks if upskilling tab is configured in profile page
ProductConfigHealthFieldExistsRule:
    config: 'career_hub_base_config'
    field_path: 'product_configs.employee.profile_page.tabs.upskilling'
```

#### Configuration Schema
```json
// career_hub_base_config::{group_id}
{
  "product_configs": {
    "employee": {
      "profile_page": {
        "tabs": {
          "upskilling": {
            "enabled": true,
            "display_name": "Upskilling",
            "order": 3
          }
        }
      }
    }
  }
}
```

#### Technical Description
Validates that the Upskilling tab is configured to appear on employee profile pages. This tab allows employees to view and manage their upskilling plans, track skill development progress, and see recommended courses for gap closure.

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → Career Hub Configuration
2. **Enable Upskilling tab**: Add upskilling to the profile page tabs configuration
3. **Set display order**: Configure the tab's position relative to other profile tabs

---

### my_courses

**Feature Mapping:** Courses / Learning  
**Config Location:** `career_hub_base_config`

#### Rule Logic
```python
# Checks if My Courses is in the navigation
ProductConfigHealthFieldExistsRule:
    config: 'career_hub_base_config'
    field_path: 'product_configs.employee.navigation.my_courses'
```

#### Configuration Schema
```json
{
  "product_configs": {
    "employee": {
      "navigation": {
        "my_courses": {
          "enabled": true,
          "label": "My Courses",
          "url": "/courses/my-courses"
        }
      }
    }
  }
}
```

#### Technical Description
Ensures the "My Courses" navigation link is configured in Career Hub. This section provides employees access to:

- Assigned courses
- In-progress courses
- Completed courses
- Course recommendations

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → Career Hub Configuration → Navigation
2. **Add My Courses**: Enable the my_courses navigation item
3. **Prerequisite**: Courses feature must be enabled for the tenant

---

### course_skills_count_rule

**Feature Mapping:** Courses / Learning  
**Data Source:** Solr  
**Threshold:** 75%

#### Rule Logic
```python
'course_skills_count_rule': {
    'constructor_args': {
        'solr_fq_term': 'skills:[* TO *]',
        'metric_threshold': 75,
    },
    'base_class': CourseDataSolrBaseRule,
}
```

#### Technical Description
Measures the percentage of courses that have skills tagged. Skill tags are essential for:

- Upskilling plan recommendations
- Career Navigator course suggestions
- Skill gap closure recommendations

#### Resolution Steps
1. **Review course data**: Export courses without skills
2. **Enrich courses**: Add skill tags via course sync or manual entry
3. **Use AI enrichment**: Enable automatic skill extraction from course descriptions

---

## Talent Management - Leader Experience Rules

### employee_manager_email_quality

**Feature Mapping:** My Team / Org Chart  
**Data Source:** Analytics  
**Threshold:** 95%

#### Rule Logic
```python
'employee_manager_email_quality': {
    'constructor_args': {
        'count_query_term': f'manager_email is not null and lower(trim(manager_email)) not in {NULL_VALUES}',
        'min_threshold': 95,
    }
}
```

#### Technical Description
Validates that employees have manager email populated. Manager email is critical for:

- Org chart generation
- Manager-based permissions
- Skill assessment workflows (manager assessment)
- Team view functionality

#### Resolution Steps
1. **Verify sync mapping**: Ensure manager_email field is mapped
2. **Check source data**: Validate manager emails exist in HRIS
3. **Handle edge cases**: Define handling for top-level employees without managers

---

### talent_hub_config

**Feature Mapping:** Talent Hub View (for HRBP)  
**Config Location:** `career_hub_base_config`

#### Configuration Schema
```json
{
  "product_configs": {
    "hrbp": {
      "talent_hub": {
        "enabled": true,
        "tabs": ["team_planning", "succession", "insights"],
        "default_tab": "team_planning"
      }
    }
  }
}
```

#### Technical Description
Configures the Talent Hub view for HRBPs, enabling them to access team planning, succession management, and workforce insights.

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Management → HRBP Configuration
2. **Enable Talent Hub**: Set enabled: true
3. **Configure tabs**: Select which tabs should be visible
4. **Set permissions**: Ensure HRBP role has appropriate access

---

### hrbp_users_rule

**Feature Mapping:** Succession Planning  
**Data Source:** User database

#### Technical Description
Validates that users with HRBP (Human Resources Business Partner) permissions exist in the system to access HRBP-specific features.

#### Resolution Steps
1. **Create HRBP users**: Add users with HRBP role
2. **Assign permissions**: Grant necessary HRBP permissions
3. **Verify access**: Test HRBP login and feature access

---

### employee_engagement_enabled

**Feature Mapping:** Skill Assessments / Upskilling  
**Config Location:** `career_hub_profile_config`

#### Rule Logic
```python
# www/career_hub/career_hub_config.py
def is_employee_engagement_enabled(self, engagement_type=None):
    if not self.get_profile_field(CareerHubConfigConstants.EMPLOYEE_ENGAGEMENT_ENABLED, False):
        return False
    ...
```

#### Configuration Schema
```json
// career_hub_profile_config::{group_id}
{
  "product_configs": {
    "employee": {
      "employee_engagement_enabled": true,
      "engagement_types": ["skill_proficiencies", "endorsements", "assessments"]
    }
  }
}
```

#### Technical Description
Enables employee engagement tracking features including skill proficiency tracking, endorsements, and assessment participation metrics.

#### Resolution Steps
1. **Navigate to**: Career Hub Configuration → Profile Configuration
2. **Enable engagement**: Set employee_engagement_enabled: true
3. **Select types**: Enable specific engagement types needed

---

## Talent Acquisition - Core Rules

### recruiter_missing_communication_email

**Feature Mapping:** Candidate Engagement with Email  
**Data Source:** User database

#### Rule Logic
```python
# www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py
@product_data_health_rule_registry.register('recruiter_missing_communication_email')
class RecruiterMisssingCommunicationEmailRule(BaseRule):
    def evaluate(self, group_id: str, system_id: str, rule_name: str = 'recruiter_missing_communication_email'):
        # Get all roles with send message permission
        roles = user_login.get_roles_with_permission(group_id, permission=perms.PERM_SEND_MESSAGES)
        # Get user emails having those roles
        user_emails = user_login.get_user_emails_having_any_role_in(group_id, roles=roles, disabled=False)
        # Filter to users without valid communication email
        user_emails = self.filter_users_without_communication_email(group_id, emails=user_emails)
        if len(user_emails) > 0:
            return PlatformHealthRuleEvalStatus.FAILED
        return PlatformHealthRuleEvalStatus.SUCCESS
```

#### Technical Description
This rule identifies users who have the `PERM_SEND_MESSAGES` permission but lack a properly configured communication email. Users need an authorized communication email to send messages to candidates.

#### Resolution Steps
1. **Export affected users**: The rule failure message lists up to 5 affected users
2. **Configure communication emails**: Navigate to Admin Console → User Management
3. **Verify email authorization**: Ensure the email domain is authorized for sending
4. **Re-ingest if needed**: If communication email comes from HRIS, update sync mapping

---

### scheduling_config (Calendar Provider)

**Feature Mapping:** Smart Scheduling  
**Config Location:** `scheduling_config`

#### Configuration Schema
```json
// scheduling_config::{group_id}
{
  "calendarProvider": "google_calendar",  // or "microsoft_outlook_365", "no_calendar_provider"
  "preferences": {
    "isRoomsEnabled": true,
    "isOnlyCandidateRescheduleRequested": false
  },
  "templates": [...],
  "minSchedulingNoticeSeconds": 3600,
  "interviewDurationOptions": [30, 45, 60, 90, 120]
}
```

#### Technical Description
Configures the calendar integration for interview scheduling. The calendar provider determines:

- How availability is checked
- Where calendar events are created
- Video conferencing integration options

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Acquisition → Scheduling
2. **Select provider**: Choose Google Calendar, Microsoft Outlook 365, or No Calendar
3. **For Google/Microsoft**: Configure OAuth credentials, have users connect calendars
4. **Set preferences**: Configure scheduling options

---

### interview_feedback_config

**Feature Mapping:** Interview Feedback  
**Config Location:** `interview_feedback_config`

#### Configuration Schema
```json
// interview_feedback_config::{group_id}
{
  "enabled": true,
  "forms": [
    {
      "id": "general_feedback",
      "name": "General Interview Feedback",
      "questions": [
        {
          "id": "q1",
          "type": "rating",
          "question": "Overall candidate assessment",
          "scale": 5
        }
      ]
    }
  ],
  "dashboard_columns": ["interviewer", "date", "rating", "recommendation"]
}
```

#### Technical Description
Configures the interview feedback system, defining:

- Feedback form templates
- Question types and structure
- Dashboard display columns
- Consolidated feedback reports

#### Resolution Steps
1. **Navigate to**: Admin Console → Talent Acquisition → Interview Feedback
2. **Enable feedback**: Set enabled: true
3. **Create forms**: Design feedback form templates with appropriate questions

---

## Talent Acquisition - PCS Rules

### PCS Base Configuration

**Config Location:** `pcsx_base_config`

#### Configuration Schema (from codebase)
```python
# www/pcsx/services/config/models.py
class PCSXBaseConfig(BaseModel):
    enabled: bool = False
    search_config: SearchConfig = SearchConfig()
    position_details_config: PositionDetailsConfig = PositionDetailsConfig()
    branding: BrandingConfig = BrandingConfig()
    seo_config: SEOConfig = SEOConfig()
    source_tracking_config: SourceTrackingConfig = SourceTrackingConfig()
    apply_form_config: ApplyFormConfig = ApplyFormConfig()
    job_feed_config: JobFeedConfig = JobFeedConfig()
```

#### Resolution Steps
1. **Navigate to**: Admin Console → Career Site → Base Configuration
2. **Enable PCS**: Set enabled: true
3. **Configure basics**: Set up minimum required settings

---

### branding_config (Logo, Colors)

**Feature Mapping:** Career Site Branding  
**Config Location:** `pcsx_base_config.branding`

#### Configuration Schema
```python
class BrandingConfig(BaseModel):
    company_name: str | None = None
    company_logo: str | None = None
    privacy_html: str = "..."
    favicons: dict = {}
    hero_image_config: HeroImageConfig = HeroImageConfig()
```

#### Resolution Steps
1. **Navigate to**: Admin Console → Career Site → Branding
2. **Upload logo**: Add company logo (recommended: 200x50px PNG)
3. **Set colors**: Configure primary and secondary brand colors (hex format)
4. **Add favicons**: Upload favicon images for browser tabs

---

### apply_form_config

**Feature Mapping:** Application Workflows  
**Config Location:** `pcsx_base_config.apply_form_config`

#### Configuration Schema
```python
class ApplyFormConfig(ApplyConfigBaseModel):
    resume: ResumeConfig = ResumeConfig()
    questions_apply_v2: QuestionsApplyV2Config = QuestionsApplyV2Config()
    recaptcha_enabled: bool = True
    disallow_duplicate_active_applications: bool | None = False
    link_off_apply_config: LinkOffApplyConfig = LinkOffApplyConfig()
    email_apply_candidate_thanks: bool = True
```

#### Resolution Steps
1. **Navigate to**: Admin Console → Career Site → Apply Form
2. **Configure fields**: Set up required and optional application fields
3. **Set resume options**: Configure allowed file types and size limits

---

### smart_apply_config

**Feature Mapping:** Smart Apply  
**Config Location:** `smart_apply_config`

#### Configuration Schema
```python
smart_apply_cfg = {
    "enabled": True,
    "position_fq": "...",
    "recommended_star_threshold": 3,
    "push_application_to_ats": True,
    "company_name": "Acme",
    "branding": {...},
    "recaptcha_enabled": 1,
}
```

#### Resolution Steps
1. **Navigate to**: Admin Console → Career Site → Smart Apply
2. **Enable**: Set enabled: true
3. **Configure ATS sync**: Set push_application_to_ats based on integration

---

## PCS Configuration Guide

PCS (Personalized Career Site) is the primary job seeker portal for external candidates. The team develops and maintains the job seeker facing parts of the Eightfold product, controlling how candidates discover jobs and apply for roles.

**Confluence References**:
- [PCS/Talent Experience/Consumer Engineering](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/656834631/PCS+Talent+Experience+Consumer+Engineering)
- [Career Site and Referrals](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2012053627/Career+Site+and+Referrals)
- [SmartApply](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/629014541/SmartApply)
- [Personalized Career Site](https://eightfoldai.atlassian.net/wiki/spaces/PSEP/pages/2670886921/Personalised+Career+Site)

### PCS Admin Console Path

**Location:** Admin Console → Talent Experience → Career Site & Referrals

### Key PCS Features

| Feature | Description |
|---------|-------------|
| **AI-based Job Discovery** | Profile matching instead of search-based approach |
| **One-Click Apply** | Frictionless application in few clicks after resume upload |
| **Personalized Experience** | Match scores, candidate insights, "People You May Work With" |
| **Talent Network** | Candidates can join without applying to specific positions |
| **Job Distribution** | XML feeds for LinkedIn, Indeed, Glassdoor; SEO for Google |

### General Settings

| Configuration | Description | Value Example |
|---------------|-------------|---------------|
| `enabled` | Make Career Site live for candidates | TRUE |
| `company_name` | Company name displayed on site | "Acme Corporation" |
| `email_apply_candidate_thanks` | Send thank you email after application | TRUE/FALSE |
| `enableTalentNetwork` | Allow candidates to join Talent Pool | TRUE |

### Branding Configuration

**Config Path:** `smart_apply_config → branding`

| Element | Configuration | Description |
|---------|---------------|-------------|
| **Navigation Bar** | `image`, `link`, `background`, `opacity` | Logo, company link, nav bar color |
| **Hero Banner** | `hero_image_config` | Home page banner image (1400px wide minimum) |
| **Favicon** | `favicons` | Browser tab icon |
| **Custom CSS** | `custom_style.css` | Custom fonts, colors, styling |
| **Custom HTML** | `custom_html.header`, `custom_html.footer` | Custom header/footer HTML |

#### Hero Banner Best Practices
- Images should be landscape format (wider than tall)
- Minimum width: 1400px (1400 x 350px recommended)
- Do not rely on text within image (may be cropped)
- Use `device_configuration` for mobile-specific images

### Position Display Settings

| Configuration | Purpose | Default Value |
|---------------|---------|---------------|
| `position_fq` | Solr filter query for positions displayed | `position.type:ats AND is_externally_posted:1` |
| `recommended_star_threshold` | Min stars for "Strong Match" display | 3.0 |
| `hide_matched_section` | Disable Get Matched and Job Insights | false |

### Advanced Search Options

**Config Path:** `smart_apply_config → advanced_search_field_map`

```json
{
  "advanced_search_field_map": {
    "skills": "",
    "Company": "efcustom_text_company",
    "hiring_title": "position.profile.canonical_hiring_title",
    "departments": "position.ats_data.job_function"
  }
}
```

Available filters: Skills, Seniority, Remote Options, Function, Shift, Relocation Assistance

### Join Talent Network Configuration

**Config Path:** `smart_apply_config → join_talent_network_form_v2_config`

| Key | Purpose | Required Fields |
|-----|---------|-----------------|
| `questions` | List of form questions | `questionId`, `label`, `type`, `required` |
| `uploadResume` | Resume upload config | `enabled`, `required` |
| `emailSubscription` | Email subscription checkbox | `enabled`, `required`, `text` |
| `privacyPolicy` | Privacy policy checkbox | `enabled` |

#### Question Types
- `text-row`: Single-line text input
- `text-area`: Multi-line text input
- `select`: Dropdown selection
- `multiselect`: Multiple selection
- `radio`: Radio button options
- `checkbox`: Checkbox options

#### Sample Configuration
```json
{
  "questions": [
    {"questionId": "firstname", "label": "First Name", "required": true, "type": "text-row"},
    {"questionId": "lastname", "label": "Last Name", "required": true, "type": "text-row"},
    {"questionId": "email", "label": "Email", "required": true, "type": "text-row"}
  ],
  "uploadResume": {"enabled": true, "required": false},
  "emailSubscription": {"enabled": true, "required": true, "text": "Subscribe for updates?"},
  "privacyPolicy": {"enabled": true}
}
```

### Job Feed Configuration

**Config Path:** `job_feed_config` + `smart_apply_config → job_feed`

| Parameter | Description | Example |
|-----------|-------------|---------|
| `target` | Job board (linkedin, indeed, glassdoor) | "linkedin" |
| `max_jobs` | Maximum jobs in feed (max 1500) | 1000 |
| `utm_source` | Source tracking parameter | "linkedin" |
| `utm_medium` | Medium tracking parameter | "job_board" |

**Feed URL Format:**
```
https://{domain}.eightfold.ai/careers/feed?target=indeed&start=0&limit=10&utm_source=test123
```

### Source Tracking Configuration

**Config Path:** `source_tracking_config` + `source_map_config`

| Configuration | Purpose |
|---------------|---------|
| `referrer_src_map` | Maps referrer domains to source codes |
| `utm_source` | URL parameter for source tracking |
| `utm_medium` | URL parameter for medium tracking |
| `utm_campaign` | URL parameter for campaign tracking |

### Cookies Used by PCS

| Cookie | Purpose | Expiry |
|--------|---------|--------|
| `_vs` | Session management, new/old visitor tracking | 2 years |
| `_vscid` | Application cluster routing (prod0, prod1, prod2) | Session |

Third-party cookies may be added by: YouTube (videos), Medium (articles), Google Analytics, Sentry, FullStory.

### i18n (Internationalization)

**Config Path:** `smart_apply_config → branding → i18n_overrides`

```json
{
  "i18n_overrides": {
    "en": {
      "About_Us_Text": "About Us",
      "Join_TN_Text": "Join Talent Network"
    },
    "de": {
      "About_Us_Text": "Wir über uns",
      "Join_TN_Text": "Talentpool beitreten"
    }
  }
}
```

Use placeholders in custom HTML: `{{About_Us_Text}}`

### Branding by Department/Location

**Config Path:** `smart_apply_config → branding → branding_by_location_department`

Customize branding elements per department or location:
- Different hero banners for HR vs Engineering
- Location-specific content (Amsterdam vs Tokyo)
- Department-specific perks and benefits

### Smart Referrals Configuration

**Config Path:** `smart_apply_config → referrals`

| Configuration | Purpose |
|---------------|---------|
| `enabled` | Enable referral functionality |
| `referral_form_config` | Form fields for referral submission |
| `referral_workflow` | Referral tracking and approval workflow |

### Domain Whitelabeling

**Config Path:** `domain_whitelabeling_config`

| Requirement | Description |
|-------------|-------------|
| Custom Domain | e.g., `careers.company.com` |
| CNAME Record | Point to `company.eightfold.ai` |
| SSL Certificate | Must be valid and match domain |

### Key PCS Rules Summary

| Rule ID | What It Checks | Config Location |
|---------|----------------|-----------------|
| `pcsx_base_enabled_cs` | PCS base config enabled | `pcsx_base_config.enabled` |
| `pcs_logo_configured_cs` | Company logo uploaded | `branding_config.company_logo` |
| `pcs_colors_configured_cs` | Brand colors set (hex) | `branding_config.primary_color` |
| `smart_apply_enabled_cs` | Smart Apply enabled | `smart_apply_config.enabled` |
| `job_feed_enabled_cs` | Job feed enabled | `job_feed_config.enabled` |
| `seo_config_valid_cs` | SEO meta tags configured | `seo_config` |
| `source_tracking_enabled_cs` | Source tracking enabled | `source_tracking_config.enabled` |
| `talent_network_enabled_cs` | Talent network join enabled | `smart_apply_config.enableTalentNetwork` |
| `login_signup_configured_cs` | Login/signup configured | `login_signup_config` |
| `candidate_profile_enabled_cs` | Candidate profile enabled | `candidate_profile_config.enabled` |

### Troubleshooting PCS Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Jobs not appearing | `position_fq` filter too restrictive | Check Solr query in `position_fq` |
| Images cropped incorrectly | Wrong image dimensions | Use 1400px wide minimum, landscape |
| Fonts not loading | Font URL not configured | Add URL to `custom_style.font` |
| Custom header/footer not showing | Invalid HTML/CSS | Validate HTML, escape quotes |
| Source tracking not working | `publish_to_google` disabled | Enable in smart_apply_config |

---

## Configuration Schema Reference

### Key Config Locations

| Config Name | Purpose | Admin Console Location |
|-------------|---------|----------------------|
| `career_hub_base_config` | TM Core Settings | Talent Management → Career Hub |
| `career_hub_profile_config` | Employee Profile Config | Talent Management → Profile |
| `career_hub_explore_config` | Browse/Discovery | Talent Management → Explore |
| `ijp_config` | Internal Mobility | Talent Management → Internal Mobility |
| `scheduling_config` | Interview Scheduling | Talent Acquisition → Scheduling |
| `interview_feedback_config` | Feedback Forms | Talent Acquisition → Feedback |
| `smart_apply_config` | Career Site Applications | Career Site → Smart Apply |
| `pcsx_base_config` | Career Site Core | Career Site → Base Config |
| `branding_config` | Career Site Branding | Career Site → Branding |
| `email_config` | Email/SMS Integration | Admin → Communications |

---

## Career Hub Configuration Guide

Career Hub (CH) platform at Eightfold enables creating and supporting multiple product personas and high customization per customer while using the common underlying components with the use of CH configs.

**Confluence Reference**: [Career Hub Config Management](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/1698267139/Career+Hub+Config+Management)

### Types of Career Hub Configs

| Config | Purpose |
|--------|---------|
| `career_hub_base_config` | Entity types, navigation, branding, feeds, goals, navbar |
| `career_hub_explore_config` | Positions, Projects, Courses explore pages |
| `career_hub_profile_config` | Profile page layout, people search |
| `career_hub_entity_alerts_config` | Notification channels, templates |
| `career_hub_projectmarketplace_config` | My projects, create/edit project pages |
| `career_planner_config` | Career Planner page |

### Navigation Configuration

```json
// career_hub_base_config → top_nav
{
  "top_nav": {
    "logo": "https://company.com/logo.png",
    "links": [
      { "type": "route", "id": "jobs", "label": "Jobs" },
      { "type": "route", "id": "courses", "label": "Learning" },
      { "type": "dropdown", "label": "More", "items": [...] }
    ]
  }
}
```

### Homepage Feeds Configuration

```json
// career_hub_base_config → home_config
{
  "home_config": {
    "page_title": "Career Hub",
    "order_of_feeds": ["recommended_jobs", "recommended_courses", "similar_people"],
    "user_activity": {
      "greeting": "Welcome back",
      "tasks": {
        "profile_completeness": { "enabled": true }
      }
    }
  }
}
```

### Profile Page Configuration

```json
// career_hub_profile_config → display_config → profile → layout
{
  "ownProfile": {
    "rows": [
      {
        "columns": [
          {
            "sections": [
              "profile_about",
              "profile_skills",
              "profile_experience_work",
              "profile_experience_education"
            ]
          }
        ]
      }
    ]
  }
}
```

Available profile sections:
- `profile_about` / `ProfileAbout`
- `profile_org` / `ProfileOrgChart`
- `profile_skills` / `ProfileSkills`
- `skills_proficiency` / `SkillsProficiency`
- `profile_experience_work` / `WorkExperience`
- `profile_experience_education` / `EducationExperience`
- `profile_experience_projects` / `ProjectExperience`
- `profile_experience_courses` / `CoursesExperience`
- `profile_mentorship` / `ProfileMentorshipChart`

---

## Pipeline & Workflow Configuration

The pipeline & workflow config controls each tab on the position pipeline, from step and custom filters on the left, to action buttons available to users, to column display on the candidate table.

**Confluence Reference**: [Pipeline & Workflow](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2013200389/Pipeline+Workflow)

### Workflow Tabs

| Tab | Default | Purpose |
|-----|---------|---------|
| Lead Candidate | Yes | Sourced candidates matched via calibration |
| Contacted | Yes | Candidates who have been contacted |
| Applicant | Yes | Candidates who submitted applications |
| Recruiter Screen | Yes | Candidates in recruiter screening |
| HM Screen | Yes | Candidates in hiring manager review |
| Interview & Offer | Yes | Candidates in interview/offer stages |

Custom tabs can be configured to capture applicants in certain stages. For example, a Hiring Manager Screening workflow containing only Shortlist and Hiring Manager Review stages.

### Display Columns Configuration

Each workflow has default columns. Additional columns can display other candidate profile attributes (Location, Candidate ID from ATS, Citizenship status, etc.).

**Lead Candidate Tab Columns:**
- Candidate Name, Match Score, Last Contacted, Last Application, Feedback

**Applicant Tab Columns:**
- Candidate Name, Match Score, Hiring Stage, Application Time, Feedback

### Step Filters

Step filters are pre-defined filters on the top-left of the workflow page. The filter definition fetches results for individual step filters. Multiple filter definitions can be configured per step.

**Common Step Filters:**
- All Matched Lead: Matched candidates with calibration filter applied
- Past Referral: Previously referred candidates
- Current Employee: Internal mobility candidates
- Saved: Saved candidates
- EFS: Candidates from EF Sourcing
- Feedback Pending/Received
- Archived
- All Active Applicants
- New Applicant

### Available Filters

Standard out-of-box filters include:
- ATS Stage, Outreach Status, Match Score, Candidate Trait/Highlight
- Location, Skills/Keywords, Job Title, Seniority Level, Companies
- Experience, Education, Employee, ATS Details, Campaign, Others

Custom filters based on candidate profile attributes (language, citizenship, silver medalist) can be added.

### Action Buttons Configuration

Action buttons (advance stage, contact, request feedback, schedule) are configured per workflow/tab.

- Actions like contact/request feedback apply to all workflows
- Actions like reject should only appear on Applicant Workflow
- Actions can be hidden by role (e.g., hide Request Feedback from Hiring Manager)

**Note**: Some action permissions are tied to roles & permission config (e.g., only users with `perm_schedule_events` see the Schedule button).

### Related Rules

| Rule ID | Purpose |
|---------|---------|
| `leads_workflow` | Verifies Leads Workflow tab is configured |
| `applicants_workflow` | Verifies Applicant Workflow tab configuration |
| `all_job_req_templates_in_stage_transition_map` | Ensures templates are in stage transition map |

---

## Diversity Configuration Guide

Eightfold's Diversity solutions measurably reduce bias throughout the hiring process, leading to better outcomes and consistent success across organizations, positions, and talent pools.

**Confluence Reference**: [Diversity - Dashboard, traits, masking and blind review](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/1728741783/Diversity+-+Dashboard+traits+masking+and+blind+review)

### Key Components

| Component | Purpose |
|-----------|---------|
| Profile Masking | Anonymize candidate attributes to reduce bias |
| Candidate Traits (Highlights) | Surface insights on anonymous candidates |
| Diversity Dashboard | Analyze diversity outcomes across hiring process |

### Profile Masking Configuration

Masking can enable key roles (Sourcers, Hiring Managers) to review profiles without bias-introducing details (name, age, gender, geography, graduation year, etc.).

**Config Location**: `masking_config`, `workflow_config`

```json
// masking_config
{
  "enabled": true,
  "masked_stages": ["Apply", "Considered", "Reviewed"],
  "masked_users": ["recruiter", "followers"],
  "masked_schools": true,
  "masked_graduation_year": true,
  "masked_sharing": true
}
```

#### Masking Configuration Options

| Attribute | Description |
|-----------|-------------|
| `enabled` | Master toggle for masking (Boolean) |
| `masked_stages` | Array of application stages where masking applies |
| `masked_users` | Array of user types (hm, recruiter, followers) |
| `masked_schools` | Mask school name in education |
| `masked_graduation_year` | Mask graduation year |
| `masked_sharing` | Mask profiles in share emails |
| `masked_phone` | Mask phone number |

#### Pipeline-Level Masking

Add `"masked_profile": true` to workflow steps for pipeline-specific masking:

```json
{
  "steps": [{
    "display_name": "All Matched Leads",
    "short_name": "recommended",
    "masked_profile": true,
    "apply_calibration_filters": true
  }]
}
```

### Candidate Traits (Highlights)

Candidate Traits provide insights on anonymous candidates. Configure in `candidate_traits_config`:

| Trait | Description |
|-------|-------------|
| `is_diversity` | Candidate belongs to a diversity class |
| `school_categories` | Category of school (Top CS School, etc.) |
| `work_exp_years` | Total years of experience |
| `same_industry` | Experience in similar industry |
| `employee_trait` | Current/Past employee |
| `is_referral` | Candidate was referred |
| `movability` | Likelihood of relocating |
| `is_veteran` | Military background |

### Diversity Dashboard Configuration

**Config Location**: `diversity_dashboard_config`

```json
{
  "diversity_class_headers": {
    "hispanic": "hispanic or latino",
    "black": "black or african american"
  },
  "application_stage_map": {
    "new_applicant": {
      "index": 1,
      "stages": ["REVIEW"],
      "display_name": "New Applications"
    },
    "phonescreen": {
      "index": 2,
      "stages": ["SCREEN"],
      "display_name": "Phone Screen"
    },
    "hired": {
      "index": 6,
      "stages": ["HIRED"],
      "display_name": "Hired"
    }
  }
}
```

### Related Rules

| Rule ID | Purpose |
|---------|---------|
| `diversity_config_enabled_cs` | Diversity config exists |
| `masking_fields_configured_cs` | Masking fields are specified |

---

## Event Recruiting Configuration

TA Events allows customers to create and manage recruiting events (job fairs, virtual hiring events, networking events, open houses, conferences). The feature offers a complete digital experience with pre/post-event checklists, landing pages, and campaign options.

**Confluence Reference**: [Event Recruiting - Product Documentation](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/1800536409/Event+Recruiting+-+Product+Documentation)

### Event Types

Default event types (more can be created):

| Type | Purpose |
|------|---------|
| Open Event | Events where anyone can register and attend |
| Invite Only Event | Events for selected individuals only |
| Campus Event | Campus/university recruiting events |

### Event Tabs

Each TA Events page has these tabs per event:

| Tab | Purpose |
|-----|---------|
| Overview | Pre/post-event checklists, event details, statistics |
| Team | Add team members and event notes |
| Positions | Select positions to hire for |
| Candidates | Add specific candidates to reach out to |
| Assessment | Set up assessment templates for evaluation |
| Landing Page | Manage event details shown to candidates |
| Campaign | Engage with event candidates |

### Key Functionalities

1. **Custom Event Registration**: Create templates for collecting candidate information during registration
2. **Custom Assessment/Evaluation**: Create assessment templates for standardized candidate evaluation
3. **Branded Landing Pages**: Custom CSS and data privacy policy, "People you may work with" widget
4. **Virtual Events**: Enable virtual hiring process with scheduling products
5. **Add Candidates to Events**: Add walk-in or sourced candidates to events
6. **Filter on Registration/Assessment Data**: Filter candidates and create campaigns based on collected data

### Configuration

**Primary Config**: `planned_event_config`

```json
{
  "enabled": true,
  "event_types": ["open", "invite_only", "campus"],
  "registration_templates": [...],
  "assessment_templates": [...],
  "landing_page_config": {...}
}
```

### Related Rules

| Rule ID | Purpose |
|---------|---------|
| `event_config_enabled_cs` | Event recruiting feature is enabled |
| `event_stages_configured_cs` | Event pipeline stages are configured |
| `event_home_config_valid_cs` | Event home configuration is valid |

---

## Communities Configuration

Eightfold Community is a tool to manage profiles in the talent network and communicate to target groups with tailored messages for Talent Sourcers. Communities provide categorization/classification capability similar to positions but with different functional logic.

**Confluence Reference**: [Communities - Product Overview](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2389311543/Communities+-+Product+Overview)

### Use Cases for Sourcers

- Newsletters, Virtual career fairs, Hot jobs
- Sharing community configuration across regions/business units
- DEI events, Leadership pipelines
- Campus programs, Alumni pools
- Intern pipelines, Mentoring pools

### Default Workflows (Nurture Type)

| Workflow | Purpose |
|----------|---------|
| Matched | Calibration-based workflow showing profile match scores |
| Added | Profiles added to community (target group) |
| Contacted | Prospects contacted automatically move here |
| Interest | Interested candidates added via 'Advance Stage' |
| Screening | Screening stage |
| In Pipeline | Profiles moved to position pipeline from community |

### User Permissions

| Permission | Description |
|------------|-------------|
| `perm_view_my_community` | View own communities |
| `perm_manage_my_community` | Perform actions on prospects in own communities |
| `perm_create_community` | Create new communities |
| `perm_view_all_community` | View all communities in group_id |
| `perm_manage_all_community` | Manage prospects in all communities |
| `perm_calibrate_all_community` | Calibrate all communities |
| `perm_calibrate_my_community` | Calibrate own communities |
| `perm_manage_community_workflow` | Create/manage community workflows |

### Admin Console Configurations

| Config | Purpose |
|--------|---------|
| `community_home_config` | Community dashboard columns and filters |
| `community_pipeline_config` | Actions on community overview page |
| `community_workflow_config` | Workflow setup per community type |

### Workflow Automation

**Available Triggers:**
- When Prospects Replies
- When Prospect Is Contacted
- When Feedback Is Submitted
- When Prospect Is Marked For Followup Later
- When Prospect's Stage Changes

**Available Actions:**
- Stage Advance Action
- Send Email Action
- Save to Pipeline Action
- Add Tag Action
- Request Feedback Action
- Add to Community Action

### Related Rules

| Rule ID | Purpose |
|---------|---------|
| `community_home` | Community home page is correctly configured |
| `community_workflows` | Community workflow config is defined per type |

---

## Profile Masking Configuration

Candidate profile masking is determined by three toggles and two properties in `masking_config` or `workflow_config`. Additionally, `PERM_VIEW_MASKED_PROFILES_ONLY` permission overrides all other settings.

**Confluence Reference**: [Profile Masking - Product & Engineering overview](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/1519910913/Profile+Masking+-+Product+Engineering+overview)

### Masking Toggles

| Toggle | Config | Purpose |
|--------|--------|---------|
| `enabled` | `masking_config` | Master toggle - if false, no masking applies |
| `masked_sharing` | `masking_config` | Controls masking in interview/feedback requests |
| `masked_profile` | `workflow_config` | Pipeline step-specific masking |

### Masking Properties

Both properties must be used together:

| Property | Description |
|----------|-------------|
| `masked_stages` | Array of application stages to mask |
| `masked_users` | Array of user types (hm, recruiter, followers, all) |

### Masking Logic

**With Position Context (pid in URL):**
- If candidate is in a stage listed in `masked_stages` AND user's role is in `masked_users` → Profile is masked
- Otherwise → Profile is not masked

**Without Position Context:**
- If candidate is in a `masked_stages` stage in ANY position AND user role is in `masked_users` for ANY of those positions → Profile is masked

### Interview Feedback Request Masking

If `masked_sharing` is:
- **false**: Profiles shared are not masked for any recipient
- **true**: Profiles masked for all feedback request recipients
- **array**: Only recipients with roles in the array see masked profiles

### Additional Masking Properties

| Property | Purpose |
|----------|---------|
| `masked_schools` | Mask school name in education |
| `masked_graduation_year` | Mask graduation year |
| `masked_phone` | Mask phone number |
| `masked_address` | Mask email address |

### Implementation Steps

1. **Identify** pipeline stages with masking (e.g., Leads, Applicants)
2. **Determine** roles seeing masked profiles (e.g., Sourcers, Hiring Managers)
3. **Define** actions that remove masking (e.g., Contacted stage)
4. **Configure** `masking_config` with `enabled`, `masked_stages`, `masked_users`
5. **Add** `masked_profile: true` to workflow steps in `workflow_config`
6. **Configure** Screening Dashboard with `is_masked: true`
7. **Test** masking in Pipeline, Profile, Diversity Dashboard

---

## Stage Mapping Guide

Stage group mapping streamlines recruitment reporting by aligning pipeline stages with predefined groups. This ensures consistent analysis of KPIs such as new applicants, screens, interviews, and hires.

**Confluence Reference**: [Stage Mapping Guide](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2218755148/Stage+Mapping+Guide)

### Key Configurations

| Config | Purpose | Location |
|--------|---------|----------|
| `ats_config.stage_map` | Controls 'hired' stage and TA pipeline tabs | Aligned with Talent Acquisition > Positions > Pipelines |
| `diversity_dashboard_config.application_stage_map` | Manages stage groups for analytics | Only related to Eightfold analytics |

### Predefined Stage Groups

- `new_applicant`
- `phonescreen`
- `onsite`
- `offer`
- `hired`
- `hired_declined` (optional, EF-generated for candidates declining after being advanced to 'hired')
- `EF Missing XXX` (EF-generated for candidates advanced without going through expected stages)

### Implementation Steps

1. Gather all stages in the recruitment pipeline
2. Categorize them into predefined stage groups
3. Configure stage group mapping in `ats_config`
4. Optionally set up customized stage groups in ATS config for TA > Positions > Pipelines (must include pre-defined stage groups)
5. Optionally set up customized stage groups in `diversity_dashboard_config` for Analytics dashboards
6. Validate in Admin Console → Integration Health → Platform Health → Data Health (ensure all 'stage' or 'hire' rules pass)

### Config Override Priority

1. If `diversity_dashboard_config.application_stage_map` is set → it takes precedence for analytics
2. If not set → falls back to `ats_config.stage_map`
3. **Exception**: 'hired' stage is ALWAYS controlled by `ats_config.stage_map`

### Impact on Analytics Metrics

| Metric | Source | Description |
|--------|--------|-------------|
| **hires** | `ats_config.stage_map` | Candidate identified as hired based on 'hired' stage group |
| `hired_ts` | `ats_config` + heuristics | For integrations: checks application.status, hired stage group ts, keywords. For file ingest: pulled directly from file |
| `hired_advanced_ts` | `ats_config` | Based on ats_config 'hired' stage group |
| `new_applicant_ts` | `diversity_dashboard_config` | Earliest ts of stages in new_applicant group |
| `phonescreen_ts` | `diversity_dashboard_config` | Earliest ts of stages in phonescreen group |
| `onsite_interview_ts` | `diversity_dashboard_config` | Earliest ts of stages in onsite group |
| `offer_ts` | `diversity_dashboard_config` | Earliest ts of stages in offer group |

**Critical Warning**: `ats_config.stage_map` MUST include the 'hired' stage group. If `diversity_dashboard_config` includes 'hired' but `ats_config` doesn't, analytics will show 'hired' stage group but candidates won't have `application_status = 'hired'` or a `hired_ts`.

### Debugging Stage Mapping Issues

When candidates show wrong hire status, check these locations in order:

1. **Product profile page**: Verify 'hired' display for the application
2. **models page**: Check candidate details
3. **analytics.application_stage table**: Verify stage_group mappings
4. **analytics.application_v7 table**: Check `hired_ts`, `status`, `last_stage`, `last_stage_group`
5. **analytics.stage_mapping table**: Verify stage mappings for group_id
6. **diversity_dashboard_config** and **ats_config**: Check consistency

### Related Instance Health Rules

- `All stages in stage transition map should be present in stagemap`
- Rules related to 'stage' or 'hire' (searchable in Platform Health)

---

## Debugging Data Quality Issues

**Confluence Reference**: [Debugging Data Quality Basics](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2218360908)

### Platform Health Page - Where to Start

On the platform health page, look at failing data health rules:
- If **Metric Health is 0%**: Most likely due to a **missing cfv2 in ATS config**
- If **Metric Health is non-zero**: Mapping exists but many entities lack values for that field

### Debugging 0% Metric Health

1. **Confirm missing cfv2**: Check the ATS config for the field mapping
2. **Click "failing" entities link**: View specific failing entities
3. **Dry run sync**: Check example entities to see if fields are already being fetched
4. **Check Pass → Raw JSON**: Search for fields that could be mapped
5. **Follow up with customer**: Determine if they want that field mapped

### Debugging Non-Zero Metric Health

1. **Click "failing" entities link**: Get example entities without values
2. **Contact customer**: Share entities lacking values for that field
3. **Customer response options**:
   - Suggest a different mapping
   - Explain why entities don't have that value

### Using Data Audit Log

View published rule metrics in db_explorer:
```sql
SELECT * FROM data_audit_log 
WHERE group_id = '{group_id}' 
AND entity_type = 'implementation_quality' 
AND DATEDIFF(days, t_create, current_date) < 7
```

### Manual Rule Execution

Data rules are published daily by:
```
scripts/airflow/dags-common/dag_implementation_quality_audit.py
```

For local testing:
```bash
python www/data_audit/audit-local.py \
  --group_id <group_id> \
  --system_id <ats> \
  --entity_type platform_health \
  --metric_types data_health \
  --entity_id_list <ats> \
  --print_all_metrics
```
Add `--flush_to_redshift` to save results.

### Common Debugging Steps

1. **Check Profile Page**: Verify data displays correctly in product UI
2. **Check models page**: Review detailed candidate data
3. **Check application_stage table**: Validate stage mappings
4. **Check application_v7 table**: Verify timestamps and status
5. **Check stage_mapping table**: Confirm config is applied
6. **Check configs**: Verify `diversity_dashboard_config` and `ats_config`
7. **Run Instance Health report**: Use "Reload" for manual re-evaluation

### Sample Debug Queries

```sql
-- Check stage mapping effectiveness
SELECT 
  stage_group, 
  stage, 
  count(distinct application_id) as applications
FROM application_stage  
WHERE group_id = '{group_id}' 
AND stage_ts >= '2024-01-01'
GROUP BY 1, 2
ORDER BY 1, 2
```

```sql
-- Check hiring data consistency
SELECT 
  status,
  CASE WHEN hired_ts IS NULL THEN 'hired_ts null' ELSE 'has hired_ts' END as hired_ts,
  count(distinct application_id)
FROM application_v7  
WHERE group_id = '{group_id}' 
AND last_stage = 'HIRED - HIRE'
AND application_ts >= '2023-10-01'
GROUP BY 1, 2
```

### Data Audit Framework

The framework supports auditing entities:
- candidate, position, user_login
- ats_sync_activity, ats_candidate, ats_position
- hris_employee, stats, analytics, ats_config

See [Data Audit Framework](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/1709080791/Data+Audit+Framework) for complete documentation.

---

## Appendix: Rule ID to Config Mapping

| Rule ID | Config | Field Path |
|---------|--------|------------|
| `employee_level_quality` | Employee Sync | `employee.level` |
| `employee_location_quality` | Employee Sync | `employee.location` |
| `employee_manager_email_quality` | Employee Sync | `employee.manager_email` |
| `employee_hiring_bands` | `ijp_config` | `job_bands` |
| `hiring_band_equivalence` | `ijp_config` | `hiring_band_equivalence` |
| `filter_by_hiring_band` | `ijp_config` | `filter_by_hiring_band` |
| `upskilling_display_config` | `career_hub_base_config` | `product_configs.employee.profile_page.tabs.upskilling` |
| `my_courses` | `career_hub_base_config` | `product_configs.employee.navigation.my_courses` |
| `explore_course` | `career_hub_explore_config` | `product_configs.employee.course.enabled` |
| `recommended_jobs_filter_list` | `career_hub_base_config` | `product_configs.employee.feeds` |
| `talent_hub_config` | `career_hub_base_config` | `product_configs.hrbp.talent_hub` |
| `scheduling_config` | `scheduling_config` | `calendarProvider` |
| `interview_feedback_config` | `interview_feedback_config` | `enabled` |
| `smart_apply_config` | `smart_apply_config` | `enabled` |
| `pcsx_base_config` | `pcsx_base_config` | `enabled` |

---

## Scheduling Configuration Guide

Smart Scheduling enables automated interview scheduling with calendar integration.

**Confluence Reference**: [Scheduling](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2011463970/Scheduling)

### Calendar Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `calendarProvider` | Google Calendar | Calendar integration (Google, Microsoft 365, No Calendar) |
| `timezone` | - | Default interview timezone |
| `minSchedulingNoticeSeconds` | 0 Hours | Minimum notice before scheduling |
| `maxInterviewsDaily` | 100 | Maximum interviews per interviewer per day |
| `eventPrivacy` | None | Calendar event privacy setting |

### Branding Settings

| Setting | Purpose |
|---------|---------|
| `company_name` | Company name shown in scheduling communications |
| `contact_email` | Contact email for scheduling support |
| `css` | Custom CSS for scheduling pages |
| `navigation_bar` | Logo, colors, and link configuration |
| `privacy_policy_link` | Privacy policy URL |

### Preferences

| Setting | Default | Description |
|---------|---------|-------------|
| `enableCustomReasonsOption` | Yes | Allow custom cancellation reasons |
| `disableReminders` | No | Disable automatic reminders |
| `enableRooms` | No | Enable conference room booking |
| `hideConfidentialPositionDetails` | Yes | Hide confidential position info |
| `sendFeedbackFormOption` | Yes | Include feedback form with invite |
| `isOnlyCandidateRescheduleRequested` | No | Limit to candidate-led rescheduling |
| `enableSchedulingRequest` | Yes | Enable scheduling requests |
| `enableBulkScheduling` | Yes | Enable bulk interview scheduling |
| `enableLiveCodingTools` | No | Enable live coding integrations |
| `feedbackReminderEmailDays` | 2 | Days before feedback reminder |

### Video Conferencing Options

Configure available video conferencing tools:
- Zoom
- Webex
- MS Teams
- Google Meet

### Communication Channels

Enable candidate communication channels:
- SMS
- WhatsApp

---

## Calibration Configuration Guide

Calibration controls AI-driven candidate matching based on job requirements.

**Confluence Reference**: [Calibration](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2013134853/Calibration)

### Requirements Configuration

| Setting | Description |
|---------|-------------|
| `diversityChoices` | EEOC diversity categories (enabled/disabled) |
| `defaultCompaniesList` | Pre-populated list of target/competitor companies |
| `educationLevels` | Education level filters (Doctorate, Masters, Bachelors, Certificate) |
| `seniorityLevel` | Seniority filters (CXO, VP, Director, Manager, Senior, Mid-Level, Entry) |
| `certifications` | List of certifications for filtering |

### Veteran Section (US Only)

| Setting | Default |
|---------|---------|
| `showVeteranStatusSection` | No |
| `showMilitaryTitles` | No |
| `showSecurityClearance` | Yes |
| `showDisabledVeteran` | Yes |
| `showSkillbridge` | Yes |

### Calibration Action Settings

- `hideConfirmCalibrationActionButton`: Hide for specified roles
- `hideShareWithHiringManagerActionButton`: Hide for specified roles

### Other Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enableDiversityFilters` | No | Enable diversity filters in calibration |
| `showHiringCompany` | No | Show hiring company filter |
| `hideDefaultCalibrationFromAssistant` | No | Hide default calibration |
| `appliesAllCalibrationFiltersToComputeLeads` | No | Apply all filters to leads |
| `showExperienceSection` | Yes | Show experience section |
| `calibrationNotesTemplate` | - | Template for calibration notes |

---

## Internal Mobility Configuration Guide

Internal Mobility enables employee job applications within Career Hub.

**Confluence Reference**: [Internal Mobility](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2020180053/Internal+Mobility)

### Application Flow Settings

| Config | Description | Best Practice |
|--------|-------------|---------------|
| `applySuccessMessage` | Message shown after successful application | Customer configurable |
| `applyButtonText` | Override apply button text (e.g., "Apply in Workday") | Customer configurable |
| `enableApplyThroughEightfold` | Toggle for direct EF apply vs. redirect | Must be OFF for redirect |
| `applyUrlTemplate` | Redirect URL for external ATS application | ATS-specific configuration |
| `applyDisclaimer` | Terms shown before application | Default privacy text |
| `emailNotificationOnCandidateApply` | Roles receiving apply notifications | Inviter, HM, Recruiter, Followers |
| `tenureEligibilityYears` | Minimum tenure in current role | Default 0 (0.5 = 6 months) |

### Job Levels and Bands

| Config | Description |
|--------|-------------|
| `showEligibleLevel` | Display eligible level below apply button |
| `showPositionLevel` | Show position level |
| `jobLevels` | Available levels for jobs and employees |
| `jobBands` | Job bands in hierarchical order |
| `bandEligibility` | Number of levels up/down for eligibility |
| `hiringBandEquivalence` | Equivalent bands (e.g., IC6 = Manager2) |

**Critical Impact**: Job bands and hiring band equivalence are essential for job recommendations and Career Navigator functionality.

### Career Navigator Configuration

Career Navigator provides personalized career path recommendations based on roles, skills, and job levels.

**Confluence Reference**: [Career Navigator Oncall Handbook](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2124808281)

#### Enablement

- Enable from [Quick Setup TM](https://stage.eightfold.ai/integrations/quick_setup_tm)
- Data quality issues are emailed to the person performing enablement
- Auto-refreshes next roles as data quality for roles improves
- Generates next roles for all roles (takes ~1 hour to complete)

#### Critical Data Quality Requirements

Platform health rules: Admin Console → Integration Health → Platform Health → Entity type → Role & Employee

| Issue | Impact | Fix |
|-------|--------|-----|
| **Roles not present** | No career paths available | Enable role auto-initialization in `jie_role_init_system_defaults_config` |
| **Role levels not present** | Incorrect seniority progression | Add JobLevel tag in `role_library_config > integration_config > display_tags` |
| **Role levels not in IJP config** | Seniority validation fails | Add to `ijp_config > job_bands / hiring_band_equivalence / career_navigator_seniority_ordering` |
| **Employee levels not in IJP config** | Level-based eligibility broken | Same as above - add employee levels to `ijp_config` |

#### IJP Config for Career Navigator

```json
{
  "job_bands": ["L1", "L2", "L3", "L4", "L5", "M1", "M2", "M3"],
  "hiring_band_equivalence": {
    "Group_1": ["L1", "L2"],
    "Group_2": ["L3", "L4"],
    "Group_3": ["L5", "M1"]
  },
  "career_navigator_seniority_ordering": ["L1", "L2", "L3", "L4", "L5", "M1", "M2", "M3"]
}
```

**Important**: Ordering in `job_bands` and `career_navigator_seniority_ordering` must be **increasing** (lowest to highest seniority).

#### Current Role Determination

User's current role is determined in order of precedence:
1. **Explicit association** - Manually associated by HRBP from UI (`efcustom_text_primary_role_id`)
2. **Implicit association** - Based on job code matching (`role_library_config > integration_config > configuration_tags`)
3. **Title matching** - Best matching role based on current employee title

#### Troubleshooting Empty/Sparse Recommendations

1. Check Data Quality at `/integrations/data_quality > Role > number of roles with no next roles`
2. Verify "Roles With Job Level" percentage is high
3. Verify "Roles With Job Level not in IJP Config" is close to 0
4. Check IJP config ordering (must be increasing seniority)
5. Refresh next roles from Admin Console

---

## Succession Planning Configuration Guide

Succession Planning enables HRBPs and Managers to plan for role transitions.

**Confluence Reference**: [Succession Planning Configs](https://eightfoldai.atlassian.net/wiki/spaces/TM/pages/1706066309/Succession+Planning+Configs)

### HRBP Permissions

Configure in Admin Console: `Provisioning > Manage HRBP Users`

| Permission | Description |
|------------|-------------|
| Business Unit (BU) | Assign BUs to HRBP |
| Location | Countries within the BU |
| jobLevel Ceiling | Maximum job level for succession plans |
| jobLevel Floor | Minimum job level for succession plans |

**Note**: Managers have implicit permissions for their team members when the feature is enabled.

### Feature Configuration Areas

1. **Succession Plan Heat Map Page**
   - Filter employees by various criteria
   - View succession plan health
   - Gender and ethnicity diversity insights
   - Stats module (configurable display/hide)

2. **Manage Succession Plan Page**
   - Add/edit/delete successors
   - View recommended successors
   - Configurable columns per group_id

3. **Recommended Successors Calibration**
   - Link to Job Intelligence Engine
   - Requires `role_library_config`

4. **HRBP/Manager View**
   - Configured via `career_hub_profile_config`
   - Custom fields: Strengths, Career Aspirations, Development Goals

5. **Download Talent Card**
   - PDF summary of employee information
   - Configurable fields per group_id

### Configuration Location

All succession planning configs are in `career_hub_base_config` under `manager_hrbp_features`.

---

## Stage Transition Map Configuration

Stage Transition Map controls candidate pipeline stage movements.

**Confluence Reference**: [Understanding Stage Transition Map](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2076442645/Understanding+Stage+Transition+Map+TA)

### Key Configuration

Location: `ats_config > workflow_template_to_stage_transition_map`

### Advance Stage Modes

| Mode | Description |
|------|-------------|
| `only_stage_group` | Valid transitions based on current stage group (e.g., Taleo) |
| `include_all_stage_groups` | All transitions available regardless of current stage (e.g., SuccessFactors) |
| `include_all_stages_until_first_mandatory` | All transitions up to first mandatory stage |

### Key Fields

| Field | Description |
|-------|-------------|
| `template_to_stage_transition_map` | Maps template names to stage transitions |
| `default_workflow_template_id` | Default template for positions without workflow_template_id |
| `mandatory_stage_before_advance` | If true, stage must be completed before advancing |

### Stage Matching Logic (only_stage_group mode)

1. Exact match with STM keys
2. UPPER CASE match with STM keys
3. Prefix match (e.g., "New - initial screen" matches "New")
4. UPPER CASE prefix match

---

## Interview Feedback Configuration Guide

Interview Feedback enables structured feedback collection from interviewers.

**Confluence Reference**: [Interview Feedback](https://eightfoldai.atlassian.net/wiki/spaces/PSGLOBAL/pages/2012020820/Interview+Feedback)

### General Settings

- Control Request Feedback button visibility on:
  - Candidate search page
  - Communication center/inbox
  - Chrome extension
- Follow-up email settings:
  - Enable feedback follow-up
  - Number of days before follow-up

### Feedback Report

Configure consolidated feedback report columns:
- Display name
- Field mapping
- Formatting rules

### Feedback Dashboard

Default columns in Feedback Center:
- Candidate Name
- Position Name
- Feedback Form
- Date Requested
- Action Button (Give Feedback, Archive)

---

## Communication Configuration Guide

Eightfold supports Email, SMS, and WhatsApp communication channels.

**Admin Console Path**: Provisioning → Email & SMS Configuration

### Email Configuration

| Setting | Description |
|---------|-------------|
| `reply_to_domain` | Domain for email replies |
| `send_from_domain` | Domain for outgoing emails |
| `bcc_emails` | BCC recipients for all communications |

### SMS Configuration

| Setting | Description |
|---------|-------------|
| `sms_twilio_account_sid` | Twilio account SID |
| `sms_twilio_auth_token` | Twilio authentication token |
| `sms_restrictions` | Block SMS by template category |

### WhatsApp Configuration

| Setting | Description |
|---------|-------------|
| `whatsapp_twilio_account_sid` | WhatsApp Twilio account SID |
| `whatsapp_twilio_auth_token` | WhatsApp Twilio auth token |
| `whatsapp_twilio_messaging_service_id` | Messaging service ID |
| `whatsapp_twilio_number` | WhatsApp phone number |
| `whatsapp_restriction` | Block WhatsApp by template category |

### Communication Templates

Templates are managed in Admin Console: `Communication Templates`

Template types:
- Email templates
- SMS templates
- WhatsApp templates (require Meta approval)
- Scheduling templates

---

## Config Health Recommendation Framework

The Config Health Recommendation Framework provides smart suggestions to users on how to optimize their configurations for better outcomes.

**Confluence Reference**: [Config Health and Recommendation Notifications](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/1930592796)

### Rule Registry and Implementation

Rules are defined in `www/integrations_console/config_health/config_health_rule.py`:

```python
CONFIG_HEALTH_RULE_REGISTRY = {
    'notify_if_missing_or_falsy_value': NotifyIfMissingOrFalsyValueRule,
    'notify_if_sandbox_difference': NotifyIfSandboxDifferenceRule,
    'notify_if_falsy_expression': NotifyIfFalsyExpressionRule,
    'validate_config': ValidateConfigRule,
}
```

### Rule Class Attributes

| Attribute | Description |
|-----------|-------------|
| `identifier` | Admin Console page identifier (e.g., `smart_apply_config`) |
| `config_name` | Name of the config (may differ from identifier for partial configs) |
| `config_path` | Path of partial config shown on Admin Console |
| `current_user` | UserLogin object of logged-in user |
| `group_id` | Group ID of logged-in user |
| `notification_config` | Configuration for the rule notification |
| `config_dict` | JSON of config shown on Admin Console |

### Creating Custom Rules

1. **Define rule class** inheriting from `ConfigHealthRuleBase`
2. **Implement `evaluate()` method** - Returns True if notification should display
3. **Implement `get_payload()` method** - Returns `ConfigHealthRulePayload` with:
   - `Title`: Short summary of notification purpose
   - `Description`: Detailed action required
   - `Category`: One of 'issue', 'warning', 'recommendation'
   - `Deeplink`: Redirect link within Admin Console

4. **Register in CONFIG_HEALTH_RULE_REGISTRY**
5. **Add to config_health_config schema**

### Common Rule Types

#### NotifyIfMissingOrFalsyValueRule
Triggers notification if a specific field is missing or falsy:
```json
{
  "enabled": true,
  "field_path": "publish_to_google",
  "title": "Jobs are not being published to Google",
  "category": "warning",
  "description": "To publish jobs to Google, set publish_to_google to true",
  "rule_id": "notify_if_missing_or_falsy_value",
  "deeplink": "smart_apply_config?tab_id=configuration_form&field_path=Publish%20To%20Google"
}
```

#### NotifyIfFalsyExpressionRule
Evaluates Jinja expressions for complex validations:
```json
{
  "enabled": true,
  "rule_id": "notify_if_falsy_expression",
  "expression": "{{ config.company_name and config.company_name != 'Acme' }}",
  "description": "Company name cannot be empty",
  "title": "Invalid company name",
  "category": "issue"
}
```

### ATS-Specific Rules

For ATS page notifications, use `included_ats_list` to specify applicable ATS systems:
```json
{
  "enabled": true,
  "field_path": "career_site_source_id",
  "title": "PCS application source not being attached",
  "rule_id": "notify_if_missing_or_falsy_value",
  "included_ats_list": ["successfactors"],
  "deeplink": "ats?tab_id=configuration_form&field_path=Career%20Site%20Source%20Id"
}
```

### Finding Deeplinks

1. Go to Solr and select "config_description" index
2. Enter field/page name in Query term
3. Enter "deeplink" in Fields text box
4. Run Solr Query to get correct deeplink

---

## AI/ML Recommendation Rules

AI/ML recommendation rules validate that positions, employees, projects, and courses have sufficient data quality to power accurate AI-driven recommendations. These rules are critical for Internal Mobility, Career Navigator, Project Staffing, Course Recommendations, and Mentor Matching.

**Config References**: `ijp_config`, `career_hub_base_config`, `internal_mobility_config`

### Internal Mobility Recommendations

#### internal_positions_calibrated_rule

**Feature Mapping:** Internal Mobility Recommendations  
**Data Source:** Solr  
**Threshold:** Configurable via `metric_data_json.min_threshold`

**Purpose:** Ensures that all open internal positions are calibrated to allow candidates/employees to receive relevant job recommendations.

**Impact of Failure:** Missing calibration may lead to job recommendations that are not aligned with a candidate/employee's experience and background, reducing relevance and quality of matches.

**Resolution Steps:**
1. Navigate to each open internal position in Talent Acquisition
2. Open the Calibration tab
3. Add skills, ideal candidates, and requirements
4. Confirm calibration to save settings

---

#### internal_positions_with_location_rule

**Feature Mapping:** Internal Mobility Recommendations  
**Data Source:** Solr  
**Threshold:** Configurable

**Purpose:** Ensures that all open positions have a location assigned to allow employees to receive relevant job recommendations based on geographic preferences.

**Impact of Failure:** Missing location data may lead to job recommendations that are not aligned with an employee's preferred or eligible locations, reducing relevance and quality of matches.

**Resolution Steps:**
1. Verify position sync mapping includes location field
2. Check source system (ATS/HRIS) has location data populated
3. Run position re-sync to update missing locations
4. For remote positions, configure "Remote" location option

---

#### internal_positions_with_skills_rule

**Feature Mapping:** Internal Mobility Recommendations  
**Data Source:** Solr  
**Threshold:** Configurable

**Purpose:** Ensures that positions have at least one skill assigned to support relevant job recommendations based on employee skill sets.

**Impact of Failure:** Without any skills assigned, the system cannot accurately match employees to roles, resulting in low-quality or irrelevant recommendations.

**Resolution Steps:**
1. Enable automatic skill extraction from job descriptions
2. Manually add skills during calibration
3. Map skill fields from ATS if available
4. Verify skill taxonomy is configured for the tenant

---

#### internal_positions_with_multiple_skills_rule

**Feature Mapping:** Internal Mobility Recommendations  
**Data Source:** Solr  
**Threshold:** Positions must have at least 3 skills

**Purpose:** Ensures that all open positions have at least 3 skills assigned to enable more precise and high-quality job recommendations.

**Impact of Failure:** Inadequate skill tagging can reduce the accuracy of recommendations and hinder the system's ability to distinguish between relevant and irrelevant matches.

**Resolution Steps:**
1. Review positions with fewer than 3 skills
2. Use calibration to add additional relevant skills
3. Enable AI skill enrichment from job descriptions
4. Review role definitions in Job Intelligence Engine

---

#### internal_positions_with_job_band_rule

**Feature Mapping:** Internal Mobility Recommendations  
**Config Location:** `ijp_config`

**Purpose:** Ensures that positions have a job band assigned to enable relevant job recommendations based on seniority alignment.

**Impact of Failure:** Missing job band data can result in mismatches between job seniority and employee experience, reducing recommendation effectiveness.

**Resolution Steps:**
1. Navigate to Admin Console → Talent Management → Internal Mobility
2. Configure `job_bands` array with all organizational levels
3. Map position hiring_band field in `custom_fields_v2`
4. Verify job band values match `ijp_config.job_bands`

---

#### claimed_employee_profiles_with_levels

**Feature Mapping:** Internal Mobility Recommendations, Mentor Recommendations  
**Data Source:** Solr  
**Threshold:** Configurable

**Purpose:** Ensures that employee profiles have a job level assigned to enable job recommendations aligned with the employee's seniority.

**Impact of Failure:** Recommendations may be too junior or senior for the employee's current position, reducing their usefulness and relevance. Additionally, missing job level information prevents the system from aligning employees with mentors at the appropriate seniority level.

**Resolution Steps:**
1. Verify employee sync mapping includes level field
2. Map level field in HRIS integration configuration
3. Ensure level values match `ijp_config.job_bands`
4. Run employee re-sync to populate missing levels

---

#### claimed_employee_profiles_with_skills

**Feature Mapping:** Internal Mobility Recommendations, Mentor Recommendations  
**Data Source:** Solr  
**Threshold:** Configurable

**Purpose:** Ensures that employee profiles include skills to support relevant job/course recommendations based on capabilities and expertise.

**Impact of Failure:** Absence of skill data can lead to generic or irrelevant recommendations that don't reflect the employee's abilities. Without skills in employee profiles, the system cannot recommend mentors with the right expertise.

**Resolution Steps:**
1. Enable Profile Activation to prompt skill entry
2. Configure skills import from HRIS if available
3. Enable AI skill extraction from resumes
4. Promote profile completion campaigns

---

### Project Recommendations

#### projects_with_multiple_skills_rule

**Feature Mapping:** Project Lead Recommendations, Project Recommendations  
**Data Source:** Solr  
**Threshold:** Projects must have at least 3 skills

**Purpose:** Ensures that projects have at least 3 relevant skills assigned to enable accurate and high-quality employee matches.

**Impact of Failure:** Limited skill data on projects can reduce matching precision, leading to inefficient resource allocation. Projects with too few skills may lead to inaccurate or generic matches.

**Resolution Steps:**
1. Add skills when creating/editing projects
2. Use calibration to add ideal skills
3. Enable skill inference from project descriptions
4. Review project templates for skill requirements

---

#### projects_with_ideal_candidates_rule

**Feature Mapping:** Project Lead Recommendations, Project Recommendations  
**Data Source:** Solr  
**Threshold:** Projects must have at least 3 ideal candidates

**Purpose:** Ensures that projects have at least three ideal candidates assigned to improve the quality of employee matching.

**Impact of Failure:** Without an ideal candidate reference, matching may not reflect actual expectations for the role. The system lacks a benchmark for fit, resulting in mismatches and reduced match confidence.

**Resolution Steps:**
1. Navigate to project calibration page
2. Add at least 3 ideal candidates as benchmarks
3. Select employees who represent ideal project contributors
4. Confirm calibration settings

---

#### projects_with_location_rule

**Feature Mapping:** Project Lead Recommendations, Project Recommendations  
**Data Source:** Solr

**Purpose:** Ensures that projects have a location assigned to support relevant employee matches based on geography.

**Impact of Failure:** Employees may be recommended for projects in unsuitable locations, impacting assignment success. Employee-project matches may ignore geographic constraints.

**Resolution Steps:**
1. Add location when creating/editing projects
2. Specify "Remote" for location-agnostic projects
3. Configure multiple locations for distributed projects

---

### Course Recommendations

#### courses_with_skills_rule

**Feature Mapping:** Course Recommendations  
**Data Source:** Solr  
**Threshold:** Configurable

**Purpose:** Ensures courses have skills present to support accurate course-to-skill matching.

**Impact of Failure:** Courses without skill tags can't be effectively matched to employee development needs, reducing recommendation quality.

**Resolution Steps:**
1. Enable AI skill extraction for courses
2. Map skills from LMS/LXP integration
3. Manually tag courses with relevant skills
4. Review course metadata for skill keywords

---

#### courses_with_description_rule

**Feature Mapping:** Course Recommendations  
**Data Source:** Solr  
**Threshold:** Minimum 50 words

**Purpose:** Ensures courses have adequate descriptions (minimum 50 words) to make the recommendation appropriate.

**Impact of Failure:** Lack of context about the course due to incomplete descriptions or no descriptions decreases the quality of course recommendation.

**Resolution Steps:**
1. Review courses with short descriptions
2. Enrich course descriptions from LMS source
3. Use AI to expand course descriptions
4. Add learning objectives and outcomes

---

### Career Navigator Recommendations

#### role_levels_in_internal_mobility_config_quality

**Feature Mapping:** Career Navigator Recommendations  
**Config Location:** `internal_mobility_config`

**Purpose:** Define levels in internal mobility configuration to establish a clear role hierarchy across the organization.

**Impact of Failure:** Without defined levels, the system cannot accurately interpret progression paths or seniority alignment, leading to invalid career path recommendations.

**Resolution Steps:**
1. Navigate to Admin Console → Talent Management → Internal Mobility
2. Configure role levels in order of seniority
3. Map levels to employee and position data
4. Verify levels align with Job Intelligence Engine roles

---

#### role_job_code_quality

**Feature Mapping:** Career Navigator Recommendations  
**Data Source:** Analytics

**Purpose:** Job codes act as unique identifiers to determine distinct roles and associate employees accurately with them.

**Impact of Failure:** Missing or inconsistent job codes lead to incorrect role mappings and invalid career path recommendations.

**Resolution Steps:**
1. Verify job_code field mapping from HRIS
2. Ensure unique job codes for each distinct role
3. Standardize job code format across systems
4. Run employee re-sync after mapping updates

---

#### role_lob_quality

**Feature Mapping:** Career Navigator Recommendations  
**Data Source:** Analytics

**Purpose:** Assign business functions (Line of Business) to roles to infer domain and improve recommendation relevance in Career Navigator.

**Impact of Failure:** Without business function context, the system may misunderstand role intent, affecting domain-specific guidance.

**Resolution Steps:**
1. Map business_function field from HRIS
2. Standardize LOB values across organization
3. Configure LOB taxonomy in Job Intelligence Engine
4. Verify employee LOB assignments

---

#### role_skills_quality

**Feature Mapping:** Career Navigator Recommendations  
**Data Source:** Analytics  
**Threshold:** Roles must have at least 3 skills

**Purpose:** Skills and benchmarks help define role requirements and power recommendations in key TM modules like Career Navigator.

**Impact of Failure:** Poorly defined role requirements hinder accurate skill gap identification and reduce the value of personalized suggestions.

**Resolution Steps:**
1. Configure role library in Job Intelligence Engine
2. Add skills to each role definition
3. Set skill proficiency benchmarks
4. Enable role skill enrichment from job market data

---

### Mentor Recommendations

#### claimed_employee_profiles_open_to_mentor

**Feature Mapping:** Mentor Recommendations  
**Data Source:** Solr

**Purpose:** Ensures a sufficient number of mentors are available to support relevant mentor recommendations for employees.

**Impact of Failure:** Too few mentors can limit access and degrade the quality of mentorship matching.

**Resolution Steps:**
1. Enable mentorship feature in Career Hub
2. Promote mentorship opt-in campaigns
3. Configure mentorship eligibility criteria
4. Track mentor availability metrics

---

#### mentor_profiles_with_rich_data

**Feature Mapping:** Mentor Recommendations  
**Data Source:** Solr

**Purpose:** Ensures mentor profiles have rich data to allow the system to make high-quality mentor recommendations.

**Impact of Failure:** Incomplete mentor profiles reduce relevance and engagement in mentorship programs.

**Resolution Steps:**
1. Encourage profile completion for mentors
2. Enable Profile Activation for mentors
3. Add mentor-specific profile sections
4. Track mentor profile completeness scores

---

## Security Rules

Security rules validate that the instance is configured according to security best practices, protecting both data integrity and user privacy.

**Config References**: `seo_config`, `external_account_for_group_id`, `campaign_config`, `email_loopback_gate`, `custom_session_timeout_config`

### is_pcs_seo_optimization_for_sandbox_true

**Feature Mapping:** Security (New Rule)  
**Config Location:** `seo_config`

**Purpose:** Ensures that sandbox environments do not publish jobs to Google/Search Engines, preventing candidates from arriving at the sandbox site rather than the production site.

**Impact of Failure:** Sandbox job postings may appear in search results, confusing candidates and potentially exposing test data.

**Resolution Steps:**
1. Navigate to Admin Console → Career Site → SEO Configuration
2. For sandbox instances, set `noindex: true`
3. Configure robots.txt to disallow crawling
4. Verify meta tags exclude sandbox from search engines

---

### num_external_domains

**Feature Mapping:** Security  
**Config Location:** `external_account_for_group_id`  
**Threshold:** Maximum 20 domains

**Purpose:** This rule checks the `external_account_for_group_id` config to ensure that the number of external domains for this instance is no more than 20.

**Impact of Failure:** Excessive external domains may indicate configuration sprawl or potential security risk.

**Resolution Steps:**
1. Review external domains in configuration
2. Remove unused or unnecessary domains
3. Consolidate domains where possible
4. Document business justification for each domain

---

### max_campaign_limit

**Feature Mapping:** Security  
**Config Location:** `campaign_config`  
**Threshold:** Maximum 2000 per campaign

**Purpose:** This rule checks that the maximum campaign limit is set to under 2000. This is set in `campaign_config` under the key `max_per_campaign`.

**Impact of Failure:** Unlimited campaigns could enable spam or abuse of the messaging system.

**Resolution Steps:**
1. Navigate to Admin Console → Communications → Campaign Settings
2. Set `max_per_campaign` to 2000 or less
3. Configure rate limiting for outbound emails
4. Monitor campaign volume metrics

---

### email_loopback_prod / email_loopback_non_prod

**Feature Mapping:** Security  
**Config Location:** `email_loopback_gate`

**Purpose:**
- **Production (`email_loopback_prod`)**: Ensures email loopback is DISABLED for production instances so emails reach actual recipients.
- **Sandbox (`email_loopback_non_prod`)**: Ensures email loopback is ENABLED for sandbox instances so test emails are routed back to the logged-in user.

**Impact of Failure:**
- In production: Loopback enabled means candidates/interviewers won't receive emails
- In sandbox: Loopback disabled means test emails go to real recipients

**Resolution Steps:**
1. For production: Disable `email_loopback_gate`
2. For sandbox: Enable `email_loopback_gate`
3. Configure `loopback_whitelisted_recipient_emails` for testing in sandbox
4. Reference: [Enhanced Email Loopback Documentation](https://docs.eightfold.ai/integration/enhanced-email-loopback)

---

### provision_user_accounts_prod

**Feature Mapping:** Security (New Rule)

**Purpose:** This determines which accounts should have accounts provisioned. Only employees whose data has been synced to Eightfold will have accounts created.

**Impact of Failure:** Accounts may be created for non-employees or former employees, creating security and access control issues.

**Resolution Steps:**
1. Configure account provisioning based on employee sync
2. Enable SSO-based provisioning
3. Set up automatic account deprovisioning
4. Review provisioned accounts regularly

---

### custom_session_timeout_config

**Feature Mapping:** Security  
**Config Location:** `custom_session_timeout_config`  
**Threshold:** Less than 24 hours

**Purpose:** This determines if the session timeout is less than 24 hours.

**Impact of Failure:** Extended sessions increase security risk from unattended workstations.

**Resolution Steps:**
1. Navigate to Admin Console → Security → Session Settings
2. Set session timeout to 24 hours or less
3. Configure idle timeout settings
4. Enable forced logout after inactivity

---

### employee_profile_visibility

**Feature Mapping:** Security  
**Config Location:** `career_hub_profile_config`

**Purpose:** Check if unclaimed employee profiles can be viewed by other employees and recruiters.

**Impact of Failure:** Unclaimed profiles may expose sensitive employee information before the employee has reviewed and approved their profile.

**Resolution Steps:**
1. Configure profile visibility settings
2. Restrict unclaimed profile access
3. Enable Profile Activation workflow
4. Set visibility permissions by role

---

### Sync Failure Rules

#### candidate_sync_failure_rule

**Purpose:** This rule evaluates the health of candidate syncs by tracking the number of sync failures.

#### position_sync_failure_rule

**Purpose:** This rule evaluates the health of position syncs by tracking the number of sync failures.

#### employee_sync_failure_rule

**Purpose:** The rule "Too many Employee Sync Failures" activates when the total count of failed synchronizations in a single day exceeds the average failed synchronizations over the last seven days by more than one standard deviation. This method uses statistical analysis to pinpoint unusual activity.

**Resolution Steps (all sync failure rules):**
1. Check ATS/HRIS API connectivity
2. Review sync error logs in Integrations Console
3. Verify credentials and permissions
4. Check for data format issues in source system
5. Re-run failed syncs after fixing issues

---

### num_rejections_rule

**Feature Mapping:** Security

**Purpose:** This rule warns if the number of rejections in a single day is unusually high compared to the average over the last seven days, using statistical analysis to detect spikes. This helps identify anomalies that might need investigation.

**Resolution Steps:**
1. Review rejection patterns in analytics
2. Investigate bulk rejection actions
3. Check for automated rejection rules
4. Validate rejection reasons

---

### application_failures_rule

**Feature Mapping:** Security

**Purpose:** This rule fails if the total number of application failures in a single day is more than one standard deviation above the average number of failures from the past seven days.

**Resolution Steps:**
1. Review application submission logs
2. Check Smart Apply configuration
3. Verify questionnaire mapping
4. Test application flow end-to-end

---

### profile_data_retention_rule

**Feature Mapping:** Security  
**Threshold:** 10% maximum

**Purpose:** This rule identifies when the percentage of profiles flagged for data retention exceeds 10% of the total talent pool.

**Impact of Failure:** Once profiles are purged, proactive checks may not be accurate as any activity on those profiles will reset the counter and prevent their deletion.

**Resolution Steps:**
1. Review data retention rules configuration
2. Verify retention periods are appropriate
3. Check for profiles incorrectly flagged
4. Run data retention audit

---

### unsubscribe_requests_volume_rule

**Feature Mapping:** Security

**Purpose:** This rule checks for a high number of unsubscribe requests. High volumes may indicate email deliverability issues or content problems.

**Resolution Steps:**
1. Review email content for relevance
2. Check unsubscribe reasons if captured
3. Verify email frequency settings
4. Review email sender reputation

---

### num_admin_accounts_rule

**Feature Mapping:** Security

**Purpose:** Check if there are too many admin accounts set up in the instance.

**Impact of Failure:** Excessive admin accounts increase security risk and complicate audit trails.

**Resolution Steps:**
1. Review all admin accounts
2. Remove unnecessary admin access
3. Implement principle of least privilege
4. Document admin access justifications

---

### data_subject_requests

**Feature Mapping:** Security

**Purpose:** Check if there are too many data subject requests set up in the instance.

**Impact of Failure:** High DSR volume may indicate compliance issues or data handling problems.

**Resolution Steps:**
1. Review DSR trends and patterns
2. Automate DSR processing where possible
3. Verify GDPR/CCPA compliance
4. Implement data minimization practices

---

## Analytics Data Quality Rules

Analytics data quality rules ensure that employee, position, and application data meets the minimum quality standards required for accurate analytics dashboards and reporting.

**Confluence Reference**: [Analytics Data Quality - Ongoing Assurance](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2528608431)

**Config References**: `diversity_dashboard_config`, `ats_config.stage_map`, `custom_fields_v2`

### Analytics Data Quality Goals

Analytics data quality refers to **accuracy** and **consistency** across various analytics products:

| Goal | Definition | Example |
|------|------------|---------|
| **Accuracy** | Metrics correctly reflect customer's business reality | # of hires on EF dashboard = actual # of hires in customer's ATS |
| **Consistency** | Same metrics in different EF products show same numbers | # of hires shown consistently across all EF products |

### Operational Goals

1. **New customers go live** without accuracy or consistency issues
2. **New dashboards go live** without accuracy or consistency issues  
3. **Minimize reoccurring issues** in existing dashboards

### Key Data Quality Challenges

| Challenge Area | Description |
|----------------|-------------|
| **Product Feature Instrumentation** | New features must ensure accurate data instrumentation (event tracking, etc.) |
| **Configuration and Data Mapping** | Data mapping from ATS/HRIS must be accurate; stage mapping, source mapping must be correctly set |
| **Analytics Products Development** | MVs, customer views, dashboard calculated fields, Data Hub queries must be error-free |
| **Analytics Data Freshness** | Occasional refresh lag (e.g., latest stage not updated within 2-hour SLA) |

### Instance Health for Analytics

Instance Health runs **daily checks** on data quality rules covering:
- Stage group mapping
- Field mapping
- Data configuration

**For Implementing Customers:**
- Customer cannot go live without clearing all Instance Health rules
- If rules cannot pass, exempt them with proper documentation
- Owner: Implementation team

**For Live Customers:**
- Failed rules show as banner notifications in Admin Console
- Alerts sent to analytics team on-call person
- Team creates tickets to fix with XFN team

### TM Analytics - Employee Data Quality

#### employee_level_quality

**Feature Mapping:** TM Analytics  
**Data Source:** Analytics  
**Threshold:** Configurable

**Purpose:** Employee levels are essential for determining employee seniority and for automatically initializing role seniority. This rule ensures that employee level field is not blank.

**Resolution Steps:**
1. Map level field from HRIS
2. Verify level values in source system
3. Run employee re-sync
4. Check analytics ETL job status

---

#### employee_location_country_quality

**Feature Mapping:** TM Analytics  
**Data Source:** Analytics

**Purpose:** This rule ensures that country field is not blank since it is used in analytics dashboards for generating insights and for filtering.

**Resolution Steps:**
1. Map location_country field from HRIS
2. Standardize country values (ISO codes)
3. Handle multi-location employees
4. Verify geographic hierarchy

---

#### employee_email_quality

**Feature Mapping:** TM Analytics  
**Data Source:** Analytics

**Purpose:** This rule ensures that email field is not blank for the employees since this field is used as a primary key in some of our datasets.

**Resolution Steps:**
1. Email is typically a required field
2. Verify email format validation
3. Check for placeholder/test emails
4. Ensure unique emails per employee

---

#### employee_is_alumni_and_termination_date_discrepancy_quality

**Feature Mapping:** TM Analytics  
**Threshold:** Discrepancy less than configured threshold

**Purpose:** This rule ensures that all employees who have left the organisation have a termination date present.

**Resolution Steps:**
1. Review alumni employees without termination dates
2. Map termination_date field from HRIS
3. Backfill missing termination dates
4. Verify alumni flag logic

---

#### employee_first_name_quality / employee_last_name_quality

**Feature Mapping:** TM Analytics

**Purpose:** This rule ensures that first name and last name must be present for employees.

**Resolution Steps:**
1. Names are typically required fields
2. Check for anonymous/masked names
3. Handle international name formats
4. Verify name sync mapping

---

#### employee_hiring_date_quality

**Feature Mapping:** TM Analytics

**Purpose:** This rule ensures that hiring date field is not blank for employees since it is important for analytics dashboard data accuracy.

**Resolution Steps:**
1. Map hiring_date from HRIS
2. Handle legacy employees without dates
3. Verify date format standardization
4. Check date validation rules

---

#### employee_manager_id_quality

**Feature Mapping:** TM Analytics

**Purpose:** This rule ensures that manager's user id field is not blank. The manager_userid field is important for the org chart product to work, as the org chart can only be generated if manager ids are present.

**Resolution Steps:**
1. Map manager_id from HRIS
2. Handle top-level employees (no manager)
3. Verify manager ID matches employee IDs
4. Check org hierarchy consistency

---

#### employee_division_quality

**Feature Mapping:** TM Analytics

**Purpose:** This rule ensures that the division field is not blank. Division (line of business) is important to understand employee's role and for role auto initialization to infer role business function.

**Resolution Steps:**
1. Map division/LOB field from HRIS
2. Standardize division naming
3. Verify division hierarchy
4. Handle cross-divisional employees

---

### TA Analytics - Application Funnel Quality

#### application_funnel_more_new_applicants_than_phonescreen

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that the count of applications in 'new_applicant' stagegroup is more than application in 'phonescreen' stagegroup so that the funnel integrity is maintained.

---

#### application_funnel_more_phonescreen_than_onsite

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that the count of applications in 'phonescreen' stagegroup is more than application in 'onsite' stagegroup so that the funnel integrity is maintained.

---

#### application_funnel_more_onsite_than_offer

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that the count of applications in 'onsite' stagegroup is more than application in 'offer' stagegroup so that the funnel integrity is maintained.

---

#### application_funnel_more_offer_than_hired

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that the count of applications in 'offer' stagegroup is more than application in 'hired' stagegroup so that the funnel integrity is maintained.

**Resolution Steps (all funnel rules):**
1. Review stage mapping in `ats_config.stage_map`
2. Verify `diversity_dashboard_config.application_stage_map`
3. Check for missing stage mappings
4. Validate funnel progression logic

---

### TA Analytics - Application Quality

#### application_source_type_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that applications must have source_type. This is critical to identify where the application was created from.

**Resolution Steps:**
1. Map source_type from ATS
2. Configure default source for direct applications
3. Set up source tracking for PCS
4. Verify source taxonomy

---

#### application_stage_group_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that a percentage of applications must be in a stage group other than 'Others'.

**Resolution Steps:**
1. Review stages mapped to 'Others'
2. Add missing stage mappings
3. Standardize stage naming
4. Update `diversity_dashboard_config.application_stage_map`

---

#### application_rejection_reason_quality

**Feature Mapping:** TA Analytics

**Purpose:** This rule ensures that rejected applications must have a rejection reason.

**Resolution Steps:**
1. Map rejection_reason from ATS
2. Configure `custom_fields_v2.application.reason`
3. Enforce rejection reason in workflow
4. Train recruiters on rejection coding

---

#### application_hired_ts_quality

**Feature Mapping:** TA Analytics

**Purpose:** This rule ensures that applications with hires must have hired_ts populated.

**Resolution Steps:**
1. Verify 'hired' stage is mapped in `ats_config.stage_map`
2. Check hired_ts population logic
3. Backfill missing hired_ts values
4. Verify ATS hired stage sync

---

### TA Analytics - Position Quality

#### position_status_data_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that status must be present for positions. This is important for analytics and is also used in the positions page.

---

#### position_location_country_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that location_country must be present for positions. This is important for analytics and is generally used while evaluating important metrics like time to fill, time to hire etc.

---

#### position_hiring_manager_name_data_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that HM name must be present for positions. This is important for analytics since this field is used as a filter in some of our dashboards.

---

#### position_title_data_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that title must be present for positions. This is important for analytics dashboards and is also used in the positions page.

---

#### position_business_unit_data_quality

**Feature Mapping:** TA Analytics

**Purpose:** This metric ensures that business_unit must be present for positions. This is important for analytics and is generally used while evaluating customer usage and success metrics.

**Resolution Steps (all position rules):**
1. Map corresponding field from ATS
2. Verify field population in source system
3. Configure `custom_fields_v2.position` mappings
4. Run position re-sync

---

### Stage Mapping Consistency

#### stagemap_hired_equal_to_diversity_config_hired

**Feature Mapping:** TA Analytics

**Purpose:** This rule ensures that if hired stagegroup is set up in diversity dashboard config, then it matches the hired stage group mappings in ATS config stagemap.

**Resolution Steps:**
1. Compare `ats_config.stage_map.hired` with `diversity_dashboard_config.application_stage_map.hired`
2. Ensure stage names match exactly
3. Update configurations to align
4. Test with sample applications

---

#### all_stage_transition_map_stages_in_diversity_dashboard_config

**Feature Mapping:** TA Analytics

**Purpose:** Diversity dashboard tracks all application stages in the system. This rule ensures all stages in stage transition map are also mapped in diversity dashboard config.

**Resolution Steps:**
1. Export all stages from stage transition map
2. Add missing stages to `diversity_dashboard_config.application_stage_map`
3. Assign appropriate stage groups
4. Validate stage index ordering

---

#### application_stage_map_index_consistency

**Feature Mapping:** TA Analytics

**Purpose:** Checks the consistency of stage indexes in diversity dashboard config. Indexes should be unique and continuous.

**Resolution Steps:**
1. Review stage indexes in `diversity_dashboard_config`
2. Ensure indexes are sequential (1, 2, 3, ...)
3. Remove duplicate indexes
4. Maintain funnel order (new_applicant → hired)

---

## Integrations Rules

Integrations rules validate the health of ATS/HRIS synchronization, webhooks, and field mappings.

**Config References**: `ats_config`, `integration_systems`, `custom_fields_v2`

### Sync Lag Rules

#### position_sync_lag_rule

**Feature Mapping:** HR Systems Integrations  
**Threshold:** Less than 60 minutes median lag

**Purpose:** This rule evaluates the health of position sync for the group_id. Position sync lag must be lower than 60 minutes for the last 7 days for this rule to pass.

**Resolution Steps:**
1. Check ATS API connectivity and rate limits
2. Review sync schedules in Integrations Console
3. Verify webhook configuration if applicable
4. Investigate slow-running sync jobs
5. Check `ats_sync_log` for error patterns

---

#### candidate_sync_lag_rule

**Feature Mapping:** HR Systems Integrations  
**Threshold:** Less than 60 minutes median lag

**Purpose:** This rule evaluates the health of candidate sync for the group_id. Candidate sync lag must be lower than 60 minutes for the last 7 days for this rule to pass.

---

#### employee_sync_lag_rule

**Feature Mapping:** HR Systems Integrations  
**Threshold:** Less than 24 hours median lag

**Purpose:** This rule evaluates the health of employee sync for the group_id. Employee sync lag must be lower than 24 hours for the last 7 days for this rule to pass.

---

### Webhook Rules

#### candidate_webhook_sync_rule

**Feature Mapping:** HR Systems Integrations  
**Threshold:** 90% success rate  
**Supported Adapters:** SuccessFactors, Workday, Greenhouse, Lever

**Purpose:** This rule evaluates the health of candidate webhook syncs for the group_id. At least 90% of webhook candidate syncs from last 7 days should pass.

---

#### position_webhook_sync_rule

**Feature Mapping:** HR Systems Integrations  
**Threshold:** 90% success rate  
**Supported Adapters:** SuccessFactors, Workday, Greenhouse, Lever

**Purpose:** This rule evaluates the health of position webhook syncs for the group_id. At least 90% of webhook position syncs from last 7 days should pass.

---

#### webhook_event_failure_rule

**Feature Mapping:** HR Systems Integrations

**Purpose:** This rule evaluates the health of webhook events for the group_id.

---

#### webhook_enabled

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `ats_config.webhook_settings`

**Purpose:** webhook_settings.status should be enabled.

**Resolution Steps (all webhook rules):**
1. Verify webhook endpoint configuration in ATS
2. Check webhook secret/authentication
3. Review webhook event logs
4. Test webhook with sample events
5. Verify network connectivity

---

### Custom Field Mapping Rules

#### custom_fields_v2_application_reason

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `custom_fields_v2.application.reason`

**Purpose:** This health rule validates that the application.reason field is properly configured. The application.reason field captures rejection reasons when candidates are moved to rejection stages.

**Impact of Failure:**
- Rejection reason data will not flow from your ATS to Eightfold
- Analytics reports will show blank/null values for rejection reasons
- Outcome data classification accuracy may be reduced
- Workflow automation rules based on rejection reasons will not trigger

**Resolution Steps:**
1. Configure `custom_fields_v2 > application > reason` in Integration System
2. Map to appropriate ATS field (e.g., `rejectionReason`)
3. Test with rejected application
4. Verify data flows to analytics

---

#### custom_fields_v2_position_recruiter

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `custom_fields_v2.position.recruiter`

**Purpose:** General custom_fields_v2.position configurations that can include recruiter field mappings to be populated for position details. Also used in screening dashboard and analytics contexts.

---

#### custom_fields_v2_position_hiring_manager

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `custom_fields_v2.position.hiring_manager`

**Purpose:** General custom_fields_v2.position configurations that can include hiring manager field mappings to be populated for position details.

---

#### custom_fields_v2_position_hiring_band

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `custom_fields_v2.position.hiring_band`

**Purpose:** 
- Salary/compensation bands: Categorizes positions into compensation levels
- Job leveling: Helps determine seniority and responsibility levels
- Career progression: Used for internal mobility and promotion tracking

---

#### custom_fields_v2_position_job_function

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `custom_fields_v2.position.job_function`

**Purpose:** Used in analytics and job categorization/reporting.

---

#### custom_fields_v2_position_business_unit

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `custom_fields_v2.position.business_unit`

**Purpose:** Critical for organizational reporting and position categorization. Data health rule `position_business_unit_data_quality` checks that 95% of positions have non-null business_unit values.

---

### EEOC Field Mappings

#### custom_fields_v2_application_race / custom_fields_v2_application_gender

**Feature Mapping:** HR Systems Integrations

**Purpose:** EEOC compliance fields extracted from application questionnaires. Used for diversity dashboard and reporting.

#### custom_fields_v2_application_disability_status / custom_fields_v2_application_veteran_status

**Feature Mapping:** HR Systems Integrations

**Purpose:** EEOC compliance fields for disability and veteran status tracking.

#### custom_fields_v2_candidate_race / custom_fields_v2_candidate_gender / custom_fields_v2_candidate_disability_status / custom_fields_v2_candidate_veteran_status

**Feature Mapping:** HR Systems Integrations

**Purpose:** EEOC compliance fields at candidate level. Extracted from EEOC questionnaire data.

**Resolution Steps (all EEOC rules):**
1. Most EEOC fields are handled automatically by ATS adapters
2. Verify EEOC data is being collected in source ATS
3. Check field mappings in Integration System
4. Test with sample application containing EEOC data

---

### RAAS List Reports (Workday)

#### candidate_raas_list_report / position_raas_list_report / questionnaire_raas_list_report

**Feature Mapping:** HR Systems Integrations  
**Adapter:** Workday

**Purpose:** These must be configured to meet sync lag SLA requirements and enable questionnaire auto-generation for Smart Apply.

**Resolution Steps:**
1. Create RAAS reports in Workday
2. Configure report URLs in `ats_config`
3. Verify report access permissions
4. Test report data retrieval

---

### Source Tracking Configuration

#### internal_job_posting_sites / external_job_posting_sites

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `enterprise_config`

**Purpose:** Defines which job board/posting site IDs are classified as internal vs external job postings.

---

#### add_application_sources_referral / add_application_sources_employee / add_application_sources_applied

**Feature Mapping:** HR Systems Integrations  
**Adapters:** iCIMS, Jobvite

**Purpose:** Maps application source types to specific ATS values for referral, employee (internal), and applied (external) applications.

---

#### internal_app_regex_source_type

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `ats_config.internal_app_regex.source_type`

**Purpose:** Automatically classifies job applications as internal by matching the application's source_type field against a regex pattern.

---

#### career_site_source_id

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `ats_config.career_site_source_id`  
**Adapter:** SuccessFactors

**Purpose:** Tags applications from the company's career site by setting the source ID in ATS systems during application writeback.

---

### SuccessFactors-Specific Rules

#### list_terminated_employees

**Feature Mapping:** HR Systems Integrations  
**Adapter:** SuccessFactors

**Purpose:** Controls whether to include terminated/inactive employees when fetching employee data.

---

#### stage_advance_using_odata

**Feature Mapping:** HR Systems Integrations  
**Adapter:** SuccessFactors

**Purpose:** The stage_advance_using_odata flag modernizes your SuccessFactors integration by switching from legacy APIs to the more capable OData API for application stage management operations.

---

#### hide_skipped_statuses_in_application_trail

**Feature Mapping:** HR Systems Integrations  
**Adapter:** SuccessFactors

**Purpose:** Cleans up the application history by filtering out phantom stages that SuccessFactors automatically creates but that applications never actually visit.

---

#### internal_to_external_candidate_profile_conversion_rule

**Feature Mapping:** HR Systems Integrations  
**Adapter:** SuccessFactors

**Purpose:** This rule succeeds if internal to external candidate conversion is enabled in SuccessFactors. This is a setting in SF, not Eightfold, and requires manual exemption.

---

## Talent Intelligence Platform Rules

Platform-wide rules that validate core Talent Intelligence Platform configurations.

### talent_lake_provisioned

**Feature Mapping:** Data Warehouse  
**Config Location:** Platform provisioning

**Purpose:** Confirms whether Talent Lake, a key feature of the Talent Intelligence Platform, is provisioned.

**Impact of Failure:** Without Talent Lake, advanced analytics and talent insights are unavailable, reducing platform utility.

**Resolution Steps:**
1. Verify Talent Lake provisioning status
2. Contact Eightfold support if not provisioned
3. Check data pipeline connectivity
4. Validate ETL job status

---

### data_retention_config

**Feature Mapping:** Admin Console - Data Retention  
**Config Location:** `data_retention_config`

**Purpose:** Ensures data retention policies are configured to purge or anonymize historical candidate data as per compliance requirements (GDPR, CCPA). A minimum of one data retention rule must be defined for the talent pool.

**Impact of Failure:** Non-compliance with data privacy laws could result in legal risks, regulatory penalties, and data mismanagement.

**Resolution Steps:**
1. Navigate to Admin Console → Data Management → Data Retention
2. Create at least one retention rule
3. Configure retention periods per source type
4. Enable automated purge schedules

---

### email_loopback

**Feature Mapping:** Admin Console - Email Loopback

**Purpose:** Email loopback is activated for all sandbox instances to route emails back to the logged-in user. In production, loopback should be disabled. Use `loopback_whitelisted_recipient_emails` for testing.

**Resolution Steps:**
1. For sandbox: Enable email loopback
2. For production: Disable email loopback
3. Configure whitelisted recipients for testing
4. Reference: [Enhanced Email Loopback](https://docs.eightfold.ai/integration/enhanced-email-loopback)

---

### oauth_enabled

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `ats_config.oauth_settings`

**Purpose:** Ensures integrations utilize OAuth authentication when supported by the adapter to enhance security posture and reduce credential exposure risks.

**Impact of Failure:** Using OAuth provides enhanced security through token-based authentication, automatic token refresh capabilities, and reduced risk of credential compromise.

**Supported Adapters:** Workday, SuccessFactors, Greenhouse, Lever, ADP

**Resolution Steps:**
1. Check if ATS supports OAuth
2. Configure OAuth credentials in Integration System
3. Test OAuth token refresh
4. Remove legacy username/password credentials

---

### stagemap_hired

**Feature Mapping:** HR Systems Integrations  
**Config Location:** `ats_config.stage_map`

**Purpose:** This rule ensures that the hired stage group mapping is set up in ATS config stagemap. The hired stage group must be defined to evaluate the 'Average Days to Hire' metric and is crucial for identifying candidates as 'hired'.

**Resolution Steps:**
1. Navigate to Admin Console → Integrations → Stage Mapping
2. Add stages to 'hired' stage group
3. Verify stage names match ATS exactly
4. Test with hired application

---

### reply_to_eightfold_support_email_validation

**Feature Mapping:** Support Health Check  
**Config Location:** `email_config`

**Purpose:** This rule checks if the default reply-to is set to support@eightfold.ai. It should be modified to the customer's level 1 admin or support team.

**Impact of Failure:** Candidates may reply to Eightfold support instead of customer support.

**Resolution Steps:**
1. Navigate to Admin Console → Communications → Email Settings
2. Update reply-to email to customer support address
3. Consult account CSM if unsure of correct email
4. Verify authorized team members for support tickets

---

## Code Reference Guide

This section provides the exact code locations for each Instance Health rule implementation, enabling developers and technical consultants to trace rule logic directly to source code.

### Base Classes and Registries

| File Path | Description |
|-----------|-------------|
| `www/data_audit/platform_health/platform_health_base.py` | Base classes: `BaseRule`, `AtsConfigBaseRule`, `ProductConfigBaseRule`, `GateEnabledBaseRule`, `PlatformHealthRuleEvalStatus`, `Preconditions` |
| `www/data_audit/platform_health/data_health/data_health_evaluation_rules.py` | Data health rule registry and base classes: `AnalyticsBaseRule`, `SolrBaseRule`, `EmployeeDataSolrBaseRule`, `CandidateDataSolrBaseRule`, `PositionDataSolrBaseRule`, `RoleDataSolrBaseRule` |
| `www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py` | Product-specific data health rules: `product_data_health_rule_registry` |
| `www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py` | Operational health rules: `operational_health_rule_registry` |
| `www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py` | Product config health rules: `product_config_health_rules` |
| `www/data_audit/platform_health/config_health/ats_config_health_configurable_rules.py` | ATS config health rules: `CONFIGURABLE_RULE_HANDLERS` |
| `www/integrations_console/config_health/config_health_rule.py` | Config health rule handlers: `CONFIG_HEALTH_RULE_REGISTRY` |

---

### Data Health Rules - Code References

#### Candidate/Profile Data Quality Rules

| Rule ID | Class Name | File Path | Base Class |
|---------|------------|-----------|------------|
| `profile_race_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `CandidateDataSolrBaseRule` |
| `profile_skills_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `CandidateDataSolrBaseRule` |
| `profile_inferred_gender_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `ProfileDataAnalyticsBaseRule` |
| `profile_first_name_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `ProfileDataAnalyticsBaseRule` |
| `profile_veteran_status_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `CandidateDataSolrBaseRule` |
| `profile_disability_status_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `CandidateDataSolrBaseRule` |
| `profile_gender_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `CandidateDataSolrBaseRule` |
| `candidate_ingestion_quantity_quality` | `CandidateIngestionQuantityQuality` | `data_health_evaluation_rules.py` line 1923 | `BaseRule` |

#### Employee Data Quality Rules

| Rule ID | Class Name | File Path | Base Class |
|---------|------------|-----------|------------|
| `employee_level_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_levels_in_internal_mobility_config_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeLevelsInIJPLevelsSolrRule` |
| `employee_thin_profile_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_email_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_role_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_hiring_date_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_current_title_seniority_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_location_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeAnalyticsBaseRule` |
| `employee_title_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeAnalyticsBaseRule` |
| `employee_job_code_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeAnalyticsBaseRule` |
| `employee_manager_email_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_division_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_internal_candidate_id_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_business_unit_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeDataSolrBaseRule` |
| `employee_multiple_profile_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeAnalyticsBaseRule` |
| `employee_is_alumni_and_termination_date_discrepancy_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `DiscrepancyAnalyticsBaseRule` |
| `employee_role_linked` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `EmployeeAnalyticsBaseRule` |
| `valid_manager_email` | `ValidManagerEmailRule` | `product_data_health_evaluation_rules.py` line 55 | `EmployeeAnalyticsBaseRule` |

#### Application Data Quality Rules

| Rule ID | Class Name | File Path | Base Class |
|---------|------------|-----------|------------|
| `internal_applications` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `referral_applications` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_source_type_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_status_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_hired_ts_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_rejection_reason_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_ts_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_position_id_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_profile_id_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_is_career_site_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationsBaseRule` |
| `application_stage_group_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationStageBaseRule` |
| `application_hired_stage_group_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationStageBaseRule` |
| `application_offer_stage_group_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationStageBaseRule` |
| `application_stage_ts_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `AnalyticsApplicationStageBaseRule` |
| `application_funnel_more_new_applicants_than_phonescreen` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `DiscrepancyAnalyticsBaseRule` |
| `application_funnel_more_phonescreen_than_onsite` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `DiscrepancyAnalyticsBaseRule` |
| `application_funnel_more_onsite_than_offer` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `DiscrepancyAnalyticsBaseRule` |
| `application_funnel_more_offer_than_hired` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `DiscrepancyAnalyticsBaseRule` |
| `duplicate_application_source_types` | `DuplicateApplicationSourceTypesRule` | `product_data_health_evaluation_rules.py` line 536 | `AnalyticsBaseRule` |
| `application_stage_group_funnel_shape_consistency` | `ApplicationStageGroupFunnelShapeConsistencyRule` | `data_health_evaluation_rules.py` line 988 | `AnalyticsBaseRule` |
| `incorrect_reject_applications_status` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `IncorrectApplicationStatusRule` |
| `incorrect_hired_applications_status` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `IncorrectApplicationStatusRule` |

#### Position Data Quality Rules

| Rule ID | Class Name | File Path | Base Class |
|---------|------------|-----------|------------|
| `position_hiring_band_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataSolrBaseRule` |
| `position_creation_ts_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `open_position_recruiter_email_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_hiring_manager_email_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_title_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_job_function_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_status_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_business_unit_data_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_location_country_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |
| `position_supervisory_org_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `PositionDataAnalyticsBaseRule` |

#### Role Data Quality Rules

| Rule ID | Class Name | File Path | Base Class |
|---------|------------|-----------|------------|
| `role_job_code_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_title_tag_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_employee_title_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_level_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_skills_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_title_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_bu_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_lob_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleDataSolrBaseRule` |
| `role_domain_matching_field_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `DomainMatchingFieldSolrRule` |
| `role_levels_in_internal_mobility_config_quality` | Dictionary-based | `data_health_evaluation_rules.py` → `data_health_rule_registry_dict` | `RoleLevelsInIJPLevelsSolrRule` |
| `total_role_profile_skills` | `TotalRoleProfileSkillsRule` | `product_data_health_evaluation_rules.py` line 404 | `RoleDataSolrBaseRule` |

---

### Product Data Health Rules - Code References

| Rule ID | Class Name | File Path | Line | Base Class |
|---------|------------|-----------|------|------------|
| `courses_with_skills_rule` | `CoursesWithSkillsRule` | `product_data_health_evaluation_rules.py` | 276 | `CourseSolrBaseRule` |
| `courses_with_title_rule` | `CoursesWithTitleRule` | `product_data_health_evaluation_rules.py` | 283 | `CourseSolrBaseRule` |
| `courses_with_description_rule` | `CoursesWithDescriptionRule` | `product_data_health_evaluation_rules.py` | 290 | `CourseSolrBaseRule` |
| `courses_with_difficulty_rule` | `CoursesWithDifficultyRule` | `product_data_health_evaluation_rules.py` | 344 | `CourseSolrBaseRule` |
| `course_skills_count_rule` | `CourseSkillsRule` | `product_data_health_evaluation_rules.py` | 247 | `CourseSolrBaseRule` |
| `projects_with_description_rule` | `ProjectsWithDescriptionRule` | `product_data_health_evaluation_rules.py` | 297 | `ProjectDataSolrBaseRule` |
| `projects_with_title_rule` | `ProjectsWithTitleRule` | `product_data_health_evaluation_rules.py` | 304 | `ProjectDataSolrBaseRule` |
| `projects_with_skills_rule` | `ProjectsWithSkillsRule` | `product_data_health_evaluation_rules.py` | 311 | `ProjectDataSolrBaseRule` |
| `projects_with_multiple_skills_rule` | `ProjectsWithMultipleSkillsRule` | `product_data_health_evaluation_rules.py` | 317 | `ProjectDataSolrBaseRule` |
| `projects_with_ideal_candidates_rule` | `ProjectsWithIdealCandidatesRule` | `product_data_health_evaluation_rules.py` | 326 | `ProjectDataSolrBaseRule` |
| `projects_with_location_rule` | `ProjectsWithLocationRule` | `product_data_health_evaluation_rules.py` | 335 | `ProjectDataSolrBaseRule` |
| `pcs_position_fq_count_rule` | `PCSPositionsQuality` | `product_data_health_evaluation_rules.py` | 350 | `BaseRule` |
| `pcsx_position_fq_count_rule` | `PCSXPositionsQuality` | `product_data_health_evaluation_rules.py` | 373 | `BaseRule` |
| `hrbp_users_rule` | `UserLoginHRBPAnalyticsRule` | `product_data_health_evaluation_rules.py` | 431 | `AnalyticsBaseRule` |
| `valid_applicant_source_id` | `ApplicantSourceIDValidationRule` | `product_data_health_evaluation_rules.py` | 484 | `BaseRule` |
| `recruiter_missing_communication_email` | `RecruiterMisssingCommunicationEmailRule` | `product_data_health_evaluation_rules.py` | 690 | `BaseRule` |
| `internal_positions_calibrated_rule` | `InternalPositionsCalibratedRule` | `product_data_health_evaluation_rules.py` | 742 | `InternalPositionDataSolrBaseRule` |
| `internal_positions_with_location_rule` | `InternalPositionsWithLocationRule` | `product_data_health_evaluation_rules.py` | 751 | `InternalPositionDataSolrBaseRule` |
| `internal_positions_with_skills_rule` | `InternalPositionsWithSkillsRule` | `product_data_health_evaluation_rules.py` | 760 | `InternalPositionDataSolrBaseRule` |
| `internal_positions_with_multiple_skills_rule` | `InternalPositionsWithMultipleSkillsRule` | `product_data_health_evaluation_rules.py` | 769 | `InternalPositionDataSolrBaseRule` |
| `internal_positions_with_ideal_candidates_rule` | `InternalPositionsWithIdealCandidatesRule` | `product_data_health_evaluation_rules.py` | 779 | `InternalPositionDataSolrBaseRule` |
| `internal_positions_with_job_band_rule` | `InternalPositionsWithJobBandRule` | `product_data_health_evaluation_rules.py` | 788 | `InternalPositionDataSolrBaseRule` |
| `claimed_employee_profiles_with_rich_data` | `ClaimedEmployeeProfilesWithRichData` | `product_data_health_evaluation_rules.py` | 835 | `ClaimedEmployeeProfileDataSolrBaseRule` |
| `claimed_employee_profiles_with_levels` | `ClaimedEmployeeProfilesWithLevels` | `product_data_health_evaluation_rules.py` | 844 | `ClaimedEmployeeProfileDataSolrBaseRule` |
| `claimed_employee_profiles_with_skills` | `ClaimedEmployeeProfilesWithSkills` | `product_data_health_evaluation_rules.py` | 859 | `ClaimedEmployeeProfileDataSolrBaseRule` |
| `claimed_employee_profiles_open_to_mentor` | `ClaimedEmployeeProfilesOpenToMentor` | `product_data_health_evaluation_rules.py` | 868 | `ClaimedEmployeeProfileDataSolrBaseRule` |
| `mentor_profiles_with_rich_data` | `MentorProfilesWithRichData` | `product_data_health_evaluation_rules.py` | 885 | `MentorProfileDataSolrRule` |
| `employee_profiles_with_rich_data` | `EmployeeProfilesWithRichData` | `product_data_health_evaluation_rules.py` | 894 | `EmployeeDataSolrBaseRule` |
| `employee_profiles_with_skills` | `EmployeeProfilesWithSkills` | `product_data_health_evaluation_rules.py` | 906 | `EmployeeDataSolrBaseRule` |
| `num_admin_accounts_rule` | `NumAdminAccountsRule` | `product_data_health_evaluation_rules.py` | 181 | `UserSolrBaseRule` |
| `unsubscribe_requests_volume_rule` | `UnsubscribeRequestsVolumeRule` | `product_data_health_evaluation_rules.py` | 918 | `GeneralDataHealthRule` |
| `emails_by_country` | `EmailsByCountryRule` | `product_data_health_evaluation_rules.py` | 995 | `GeneralDataHealthRule` |
| `data_subject_requests` | `DataSubjectRequestsRule` | `product_data_health_evaluation_rules.py` | 1082 | `GeneralDataHealthRule` |
| `role_changes` | `RoleChangesRule` | `product_data_health_evaluation_rules.py` | 1151 | `GeneralDataHealthRule` |
| `profile_data_retention_rule` | `ProfileDataRetentionRule` | `product_data_health_evaluation_rules.py` | 1215 | `GeneralDataHealthRule` |
| `emails_sent_to_employees` | `EmployeeEmailsAnalyticsRule` | `product_data_health_evaluation_rules.py` | 1314 | `EmailAnalyticsBaseRule` |
| `num_emails_rule` | `EmailsCountAnalyticsRule` | `product_data_health_evaluation_rules.py` | 1365 | `EmailAnalyticsBaseRule` |
| `reply_to_eightfold_support_email_validation` | `ReplyToEightfoldSupportEmailValidationRule` | `default_reply_to_email_validation_rules.py` | Registered at line 665 | `BaseRule` |

---

### Operational Health Rules - Code References

| Rule ID | Class Name | File Path | Line | Base Class |
|---------|------------|-----------|------|------------|
| `position_sync_lag_rule` | `PositionSyncLagRule` | `operational_health_evaluation_rules.py` | 1082 | `BaseSyncLagRule` |
| `candidate_sync_lag_rule` | `CandidateSyncLagRule` | `operational_health_evaluation_rules.py` | 1074 | `BaseSyncLagRule` |
| `employee_sync_lag_rule` | `EmployeeSyncLagRule` | `operational_health_evaluation_rules.py` | 1090 | `BaseSyncLagRule` |
| `position_sync_failure_rule` | `PositionSyncFailureRule` | `operational_health_evaluation_rules.py` | 1173 | `BaseSyncFailureRule` |
| `candidate_sync_failure_rule` | `CandidateSyncFailureRule` | `operational_health_evaluation_rules.py` | 1167 | `BaseSyncFailureRule` |
| `employee_sync_failure_rule` | `EmployeeSyncFailureRule` | `operational_health_evaluation_rules.py` | 1179 | `BaseSyncFailureRule` |
| `application_submissions_per_job_req_template_week_rule` | `ApplicationSubmissionsPerJobReqTemplateWeekRule` | `operational_health_evaluation_rules.py` | 1097 | `BaseApplicationSubmissionRule` |
| `application_submissions_per_job_req_template_month_rule` | `ApplicationSubmissionsPerJobReqTemplateMonthRule` | `operational_health_evaluation_rules.py` | 1104 | `BaseApplicationSubmissionRule` |
| `application_stage_advances_per_job_req_template_rule` | `ApplicationStageAdvancesPerJobReqTemplateRule` | `operational_health_evaluation_rules.py` | 1111 | `BaseApplicationStageAdvanceRule` |
| `candidate_webhook_sync_rule` | `CandidateWebhookSyncRule` | `operational_health_evaluation_rules.py` | 1118 | `BaseWebhookSyncRule` |
| `position_webhook_sync_rule` | `PositionWebhookSyncRule` | `operational_health_evaluation_rules.py` | 1127 | `BaseWebhookSyncRule` |
| `employee_webhook_sync_rule` | `EmployeeWebhookSyncRule` | `operational_health_evaluation_rules.py` | 1136 | `BaseWebhookSyncRule` |
| `webhook_event_failure_rule` | `WebhookEventFailureRule` | `operational_health_evaluation_rules.py` | 455 | `BaseRule` |
| `num_rejections_rule` | `NumRejectionsRule` | `operational_health_evaluation_rules.py` | 564 | `BaseRule` |
| `application_failures_rule` | `ApplicationFailuresRule` | `operational_health_evaluation_rules.py` | 636 | `BaseRule` |
| `application_failures_sla_rule` | `ApplicationFailuresSLARule` | `operational_health_evaluation_rules.py` | 719 | `ApplicationFailuresRule` |
| `stage_advance_failures_sla_rule` | `StageAdvanceFailuresSLARule` | `operational_health_evaluation_rules.py` | 796 | `ApplicationFailuresRule` |
| `api_server_error_rate` | `APIServerErrorRateRule` | `operational_health_evaluation_rules.py` | 875 | `BaseRule` |
| `app_platform_error_rate` | `AppPlatformErrorRateRule` | `operational_health_evaluation_rules.py` | 941 | `BaseRule` |
| `file_ingest_error_rate` | `FileIngestErrorRateRule` | `operational_health_evaluation_rules.py` | 1014 | `BaseRule` |
| `internal_to_external_candidate_profile_conversion_rule` | `InternalToExternalCandidateProfileConversionRule` | `operational_health_evaluation_rules.py` | 1144 | `BaseRule` |

---

### Config Health Rules - Code References

#### Product Config Rules

| Rule ID | Handler Class | File Path | Description |
|---------|---------------|-----------|-------------|
| Field existence rules | `ProductConfigHealthFieldExistsRule` | `product_config_health_configurable_rules.py` line 19 | Checks if config field exists |
| Gate enabled rules | `GateEnabledRule` | `product_config_health_configurable_rules.py` line 32 | Checks if feature gate is enabled |
| List size rules | `ProductConfigHealthListSizeRule` | `product_config_health_configurable_rules.py` line 45 | Validates list field sizes |
| Template rules | `ProductConfigHealthTemplateRule` | `product_config_health_configurable_rules.py` line 86 | Evaluates Jinja templates |
| Compare value rules | `ProductConfigHealthCompareValueRule` | `product_config_health_configurable_rules.py` line 127 | Compares config values |
| Dynamic threshold rules | `ProductConfigHealthDynamicCompareValueThresholdRule` | `product_config_health_configurable_rules.py` line 152 | Threshold comparison |
| Diversity stage map index | `DiversityDashboardConfigHealthApplicationStageMapIndexRule` | `product_config_health_configurable_rules.py` line 216 | Stage index validation |
| Planned event config | `PlannedEventConfigDiscrepenacyRule` | `product_config_health_configurable_rules.py` line 276 | Event config validation |
| Recommended feed threshold | `RecommendedFeedThresholdRule` | `product_config_health_configurable_rules.py` line 372 | Career Hub threshold check |

#### ATS Config Rules

| Handler Class | File Path | Description |
|---------------|-----------|-------------|
| `AtsConfigHealthFieldExistsRule` | `ats_config_health_configurable_rules.py` line 17 | ATS config field existence |
| `AtsConfigHealthCompareWithExternalSourceRule` | `ats_config_health_configurable_rules.py` line 30 | External source comparison |
| `AtsConfigHealthCompareValueWithOtherConfigRule` | `ats_config_health_configurable_rules.py` line 102 | Cross-config comparison |
| `AtsConfigHealthCompareValueRule` | `ats_config_health_configurable_rules.py` line 134 | ATS config value comparison |
| `AtsConfigHealthCheckDuplicatesRule` | `ats_config_health_configurable_rules.py` line 163 | Duplicate detection |
| `AtsConfigHealthCompareMapValuesRule` | `ats_config_health_configurable_rules.py` line 208 | Stage map value comparison |
| `AtsConfigHealthConfiguredJobReqTemplatesRule` | `ats_config_health_configurable_rules.py` line 298 | Job req template validation |
| `AtsConfigHealthCountryNameFormatRule` | `ats_config_health_configurable_rules.py` line 365 | Country name format check |

#### Integrations Console Config Rules

| Rule Type | Handler Class | File Path | Description |
|-----------|---------------|-----------|-------------|
| Missing/Falsy Value | `NotifyIfMissingOrFalsyValueRule` | `config_health_rule.py` line 73 | Checks for missing config |
| Falsy Expression | `NotifyIfFalsyExpression` | `config_health_rule.py` line 84 | Evaluates expressions |
| Validate Config | `ValidateConfigRule` | `config_health_rule.py` line 102 | Schema validation |
| Sandbox Difference | `NotifyIfSandboxDifferenceRule` | `config_health_rule.py` line 125 | Sandbox sync check |

---

### Key Base Class Hierarchy

```
BaseRule (platform_health_base.py)
├── AtsConfigBaseRule
│   └── [ATS Config Health Rules]
├── ProductConfigBaseRule
│   └── [Product Config Health Rules]
├── GateEnabledBaseRule
│   └── [Gate Enabled Rules]
├── AnalyticsBaseRule
│   ├── AnalyticsApplicationsBaseRule
│   ├── AnalyticsApplicationStageBaseRule
│   ├── EmployeeAnalyticsBaseRule
│   ├── ProfileDataAnalyticsBaseRule
│   ├── PositionDataAnalyticsBaseRule
│   ├── DiscrepancyAnalyticsBaseRule
│   └── EmailAnalyticsBaseRule
├── SolrBaseRule
│   ├── EmployeeDataSolrBaseRule
│   │   └── EmployeeLevelsInIJPLevelsSolrRule
│   ├── CandidateDataSolrBaseRule
│   ├── PositionDataSolrBaseRule
│   │   └── InternalPositionDataSolrBaseRule
│   ├── RoleDataSolrBaseRule
│   │   ├── DomainMatchingFieldSolrRule
│   │   └── RoleLevelsInIJPLevelsSolrRule
│   ├── CourseSolrBaseRule
│   ├── ProjectDataSolrBaseRule
│   ├── UserSolrBaseRule
│   └── ClaimedEmployeeProfileDataSolrBaseRule
│       └── MentorProfileDataSolrRule
├── GeneralDataHealthRule
├── BaseSyncLagRule
├── BaseSyncFailureRule
├── BaseApplicationSubmissionRule
├── BaseApplicationStageAdvanceRule
└── BaseWebhookSyncRule
```

---

### Data Sources

| Data Source Constant | Description | File |
|---------------------|-------------|------|
| `AuditDataSource.SEARCH_POSITIONS` | Solr positions index | `audit_base.py` |
| `AuditDataSource.SEARCH_EMPLOYEE_PROFILES` | Solr employee profiles | `audit_base.py` |
| `AuditDataSource.SEARCH_CANDIDATE_PROFILES` | Solr candidate profiles | `audit_base.py` |
| `AuditDataSource.SEARCH_COURSE` | Solr courses index | `audit_base.py` |
| `AuditDataSource.ANALYTICS_DB` | Redshift analytics database | `audit_base.py` |
| `AuditDataSource.ANALYTICS_DB_APPLICATIONS` | Redshift applications table | `audit_base.py` |
| `AuditDataSource.ANALYTICS_DB_EMPLOYEE` | Redshift employee table | `audit_base.py` |
| `AuditDataSource.ANALYTICS_DB_PROFILE` | Redshift profile table | `audit_base.py` |
| `AuditDataSource.ANALYTICS_DB_POSITION` | Redshift position table | `audit_base.py` |
| `AuditDataSource.DB_ATS_SYNC_LOG` | Redshift ATS sync log | `audit_base.py` |
| `AuditDataSource.DB_ATS_WRITE_LOG` | Redshift ATS write log | `audit_base.py` |
| `AuditDataSource.DB_WWW_SERVER_LOG` | Redshift www server log | `audit_base.py` |
| `AuditDataSource.DB_WEBHOOKS_LOG` | Redshift webhooks log | `audit_base.py` |

---

### Rule Configuration Location

All rule definitions and configurations are maintained in `platform_health_base_config`:

```python
# Path: config/platform_health_base_config.json
{
    "implementation_quality": {
        "<feature_id>": {
            "display_name": "Feature Display Name",
            "product_area": "Talent Management|Talent Acquisition|Talent Experience",
            "linked_rules": [...]
        }
    },
    "data_health_rules": {...},
    "product_data_health_rules": {...},
    "product_operational_health_rules": {...},
    "ats_config_health_rules": {...},
    "product_config_health_rules": {...}
}
```

---

*This document incorporates information from the Eightfold codebase and Confluence documentation. For the latest updates, refer to the [Instance Health](https://eightfoldai.atlassian.net/wiki/spaces/EP/pages/2190936431/Instance+Health) Confluence page.*
