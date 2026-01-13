#!/usr/bin/env python3
"""
Enhance all rule descriptions to be clearer, more accurate, and more helpful.
Based on comprehensive Confluence documentation and codebase review.
"""

import csv
import os

# Enhanced rule descriptions mapping - Rule ID to enhanced description
ENHANCED_DESCRIPTIONS = {
    # TM - Skill Assessments
    "skill_proficiences": """**Purpose:** Ensures skill proficiency levels are configured for Skill Assessments in Career Hub. Proficiency levels (e.g., Beginner, Intermediate, Advanced, Expert) allow employees and managers to track competency progression over time.

**Impact:** Without proficiency configuration, skill assessments cannot measure or track competency levels, making it impossible to identify skill gaps or measure upskilling progress.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Skill Assessments. Enable proficiency tracking and configure the proficiency scale (typically 4-5 levels). Ensure proficiency levels are mapped to your organization's competency framework.""",

    "profile_page_skill_assessments": """**Purpose:** Validates that the Skill Assessments tab is configured on the employee profile page, providing a dedicated location for employees to view and complete their skill assessments.

**Impact:** If not configured, employees must navigate elsewhere to access assessments, reducing visibility and participation rates. This can significantly impact upskilling program adoption.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Profile Page Configuration. Add 'skill_assessments' to the profile page tabs. Verify the tab appears in the employee's profile navigation.""",

    "skill_assessment_default_access": """**Purpose:** Ensures access control is properly configured for Skill Assessments, determining who can view, request, and complete assessments based on organizational hierarchy and role.

**Impact:** Without proper access configuration, assessments may not respect organizational boundaries, or employees may be unable to access assessments assigned to them.

**To Fix:** Configure access rules in Admin Console → Talent Management → Skill Assessments → Access Control. Set permissions for employee self-assessment, manager-initiated assessments, and HRBP oversight.""",

    # TM - Employee Engagement
    "employee_engagement_enabled": """**Purpose:** Validates that employee engagement tracking is enabled in Career Hub, allowing the platform to measure and report on employee participation in development activities like upskilling, career planning, and skill assessments.

**Impact:** Without engagement tracking, organizations cannot measure adoption of TM features, identify disengaged employees, or demonstrate ROI of talent management initiatives.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub Base Config. Set 'employee_engagement_enabled' to true. Configure engagement metrics to track (logins, course completions, skill updates, etc.).""",

    # TM - Upskilling
    "upskilling_display_config": """**Purpose:** Ensures the Upskilling tab is visible on the employee profile page, providing access to upskilling plans, recommended courses, and skill development activities.

**Impact:** If missing, employees cannot view or manage their upskilling plans from their profile, reducing engagement with learning and development initiatives.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Profile Page. Add 'upskilling' to the tabs configuration. For org-led upskilling, also verify template management is accessible to HRBPs/Talent Admins.""",

    "upskilling_top_nav": """**Purpose:** Validates that the Upskilling link appears in Career Hub's top navigation bar, enabling quick access to upskilling features.

**Impact:** Without navigation visibility, employees may not discover upskilling features, reducing adoption and participation in development programs.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Navigation. Add 'upskilling' to the top navigation items. Configure display order and label.""",

    # TM - Profile Quality Rules
    "profile_skills_quality": """**Purpose:** Measures the percentage of employee profiles with at least one skill added. Target threshold: 75% of profiles should have skills.

**Impact:** Low skill coverage reduces the effectiveness of AI-powered matching, job recommendations, and skill-based analytics. Career Navigator and succession planning depend on skill data.

**To Fix:** Encourage employees to add skills via Profile Assistant. Use bulk skill import from HRIS. Enable skill inference from job titles and experience. Run engagement campaigns to improve profile completeness.""",

    "employee_level_quality": """**Purpose:** Validates that employee profiles have a defined level/grade. Levels are used for seniority inference, role matching, and Career Navigator path recommendations.

**Impact:** Missing levels affect job eligibility calculations, succession planning accuracy, and internal mobility recommendations. Career Navigator cannot properly initialize roles without level data.

**To Fix:** Ensure levels are ingested from HRIS. Map HRIS levels to Eightfold's level schema. Verify levels appear in employee profiles. Check level mapping in Admin Console → Internal Mobility.""",

    "employee_job_code_quality": """**Purpose:** Measures the percentage of employees with job codes defined. Job codes uniquely identify roles and are critical for role-based workflows.

**Impact:** Without job codes, employees cannot be properly mapped to roles in Talent Design. This breaks succession planning, internal mobility matching, and role-based analytics.

**To Fix:** Ensure job codes are ingested from HRIS during employee data sync. Verify job code field mapping. Check that job codes match role definitions in Talent Design.""",

    "employee_business_unit_quality": """**Purpose:** Validates that employees have Business Unit (BU) assignments, which are essential for organizational grouping, permissioning, and analytics segmentation.

**Impact:** Missing BU data affects HRBP permissions (which are often BU-scoped), organizational reporting, and workforce planning by business area.

**To Fix:** Verify BU field is mapped from HRIS. Ensure all employees have BU assignments. Check BU values match expected organizational structure in Admin Console → Provisioning.""",

    "employee_location_quality": """**Purpose:** Measures the percentage of employees with location data, which is essential for geo-based job recommendations and location-specific reporting.

**Impact:** Missing location data limits personalization of job recommendations and affects location-based workforce analytics and planning.

**To Fix:** Map location fields from HRIS. Verify location data includes sufficient granularity (country, state/region, city). Check location normalization in employee profiles.""",

    "employee_hiring_date_quality": """**Purpose:** Validates that employees have hiring dates defined, which are essential for tenure calculations and workforce analytics.

**Impact:** Missing hiring dates affect tenure-based eligibility rules, retention analytics, and workforce experience reporting.

**To Fix:** Map hire_date field from HRIS. Verify date format is correctly parsed. Check that hiring dates appear correctly in employee profiles.""",

    "employee_current_title_seniority_quality": """**Purpose:** Measures the percentage of employees with seniority level derived from their current title. Seniority is inferred by AI from job titles.

**Impact:** Missing seniority affects job matching accuracy, internal mobility recommendations, and succession planning eligibility.

**To Fix:** Ensure current titles are populated in employee profiles. AI will infer seniority automatically. For custom seniority mappings, configure in Admin Console → Calibration Settings.""",

    "employee_division_quality": """**Purpose:** Validates that employees have division/Line of Business (LOB) data, which helps with role initialization and business function inference.

**Impact:** Missing division data affects role grouping, workforce planning by business area, and analytics segmentation.

**To Fix:** Map division field from HRIS. Verify LOB values are consistent and match organizational structure. Check division appears in employee profiles.""",

    "employee_manager_email_quality": """**Purpose:** Measures the percentage of employees with manager email defined. Manager relationships are required for org charts, manager-based permissions, and skill assessments (which often require manager input).

**Impact:** Missing manager emails break org chart visualization, affect manager-based permissions, and prevent manager-initiated assessments.

**To Fix:** Ensure manager_email is mapped from HRIS. Verify manager emails match valid user_login records. Check org hierarchy displays correctly in Career Hub.""",

    "employee_manager_id_quality": """**Purpose:** Validates that employees have manager_userid defined, which is the unique identifier linking employees to their managers in the org hierarchy.

**Impact:** Missing manager IDs prevent accurate org chart construction and break manager-based workflows like succession planning access.

**To Fix:** Map manager_userid from HRIS (often the manager's employee ID). Verify IDs match existing employee records. Test org chart navigation.""",

    "valid_manager_email": """**Purpose:** Validates that manager emails assigned to employees correspond to actual employee records in the system (not just that the field exists, but that it's valid).

**Impact:** Invalid manager emails break org chart chains and may cause permission issues for manager-based features.

**To Fix:** Run data quality report to identify invalid manager emails. Update manager references to valid employee emails. Ensure terminated managers are properly reassigned.""",

    "employee_thin_profile_quality": """**Purpose:** Measures the percentage of employees who do NOT have thin (minimal) profiles. A thin profile lacks essential data like skills, experience details, or education.

**Impact:** High percentage of thin profiles reduces AI matching effectiveness, limits recommendations quality, and affects analytics accuracy.

**To Fix:** Enable Profile Assistant to help employees enrich profiles. Use resume parsing to auto-populate profile data. Run profile completeness campaigns. Set minimum profile requirements.""",

    # TM - Role Quality Rules
    "role_job_code_quality": """**Purpose:** Validates that roles in Talent Design have job codes defined, enabling mapping between employees and roles.

**Impact:** Roles without job codes cannot be matched to employees, breaking succession planning and internal mobility workflows.

**To Fix:** Navigate to Admin Console → Talent Design → Roles. Add job codes to role definitions. Ensure job codes match those in employee profiles.""",

    "role_title_quality": """**Purpose:** Validates that roles have titles defined. Titles are used for matching, display, and Career Navigator recommendations.

**Impact:** Roles without titles cannot be properly displayed or matched, affecting all TM features that depend on role data.

**To Fix:** Navigate to Admin Console → Talent Design → Roles. Ensure all roles have meaningful titles. Use consistent naming conventions.""",

    "role_level_quality": """**Purpose:** Validates that roles have associated levels/grades defined, which determine seniority and hierarchy.

**Impact:** Roles without levels cannot be properly ordered in Career Navigator paths and affect succession planning eligibility.

**To Fix:** Navigate to Admin Console → Talent Design → Roles. Assign levels to all roles. Ensure levels match the organization's job architecture.""",

    "role_levels_in_internal_mobility_config_quality": """**Purpose:** Validates that role levels are defined in the Internal Mobility configuration, which is critical for eligibility calculations.

**Impact:** Missing level configurations in Internal Mobility can break job band filtering and eligibility rules.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Verify all levels are configured in the job bands section.""",

    "role_lob_quality": """**Purpose:** Validates that roles have business function/Line of Business defined, which helps with domain-based matching and role grouping.

**Impact:** Roles without business function cannot be properly categorized, affecting Career Navigator and succession planning.

**To Fix:** Navigate to Admin Console → Talent Design → Roles. Assign business functions to roles based on organizational structure.""",

    "role_skills_quality": """**Purpose:** Measures the percentage of roles with at least 3 skills defined. Skills on roles enable accurate matching for succession planning.

**Impact:** Roles with fewer than 3 skills reduce matching accuracy and limit the effectiveness of succession recommendations.

**To Fix:** Navigate to Admin Console → Talent Design → Roles. Add relevant skills to each role (recommend 5-10 skills per role).""",

    "employee_role_quality": """**Purpose:** Validates that employees are assigned to roles in Talent Design, which is necessary for identifying required skills and succession planning.

**Impact:** Employees without role assignments cannot have their skill gaps identified or be considered for succession plans.

**To Fix:** Ensure employee-to-role mapping via job codes. Verify roles exist in Talent Design for all job codes. Check mapping in employee profiles.""",

    # TM - Courses
    "course_skills_count_rule": """**Purpose:** Measures the percentage of courses with skills tagged. Skills on courses enable accurate recommendations for upskilling plans.

**Impact:** Courses without skills cannot be recommended accurately for skill development, reducing effectiveness of learning recommendations.

**To Fix:** Tag courses with relevant skills via LMS integration or manual assignment. Use AI to infer skills from course titles and descriptions.""",

    "courses_with_skills_rule": """**Purpose:** Similar to course_skills_count_rule - validates that courses have associated skills for filtering and recommendations.

**Impact:** Courses without skills reduce recommendation quality and cannot be used effectively in upskilling workflows.

**To Fix:** Navigate to Admin Console → Learning. Tag courses with skills. Enable skill inference if available from your LMS integration.""",

    "courses_with_title_rule": """**Purpose:** Validates that courses have titles defined. Titles are essential for identification and skill inference.

**Impact:** Courses without titles are difficult to identify and cannot have skills inferred from them.

**To Fix:** Ensure LMS integration provides course titles. Verify titles appear in course listings. Add missing titles manually if needed.""",

    "courses_with_description_rule": """**Purpose:** Validates that courses have descriptions of at least 50 words. Rich descriptions help employees understand content and enable skill inference.

**Impact:** Courses without sufficient descriptions reduce engagement and limit AI skill inference capabilities.

**To Fix:** Add meaningful descriptions to courses via LMS. Include learning objectives, target audience, and key topics covered.""",

    "my_courses": """**Purpose:** Validates that the "My Courses" section is available in Career Hub navigation, providing a central location for employees to track their learning.

**Impact:** Without My Courses, employees cannot easily track assigned, in-progress, and completed courses in one place.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Navigation. Add 'my_courses' to navigation items.""",

    "explore_course": """**Purpose:** Validates that Course exploration is enabled, allowing employees to browse and discover learning opportunities.

**Impact:** Without course exploration, employees cannot discover new learning opportunities aligned with their career goals.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Explore. Enable course exploration feature.""",

    "global_search_course": """**Purpose:** Validates that courses are included in Global Search, allowing employees to find courses alongside other content.

**Impact:** Without global search integration, employees must navigate separately to find courses, reducing discoverability.

**To Fix:** Navigate to Admin Console → Talent Management → Global Search. Enable courses in searchable entity types.""",

    # TM - Projects
    "projects_with_skills_rule": """**Purpose:** Validates that projects have skills tagged, which helps showcase employee capabilities and enables skill-based project matching.

**Impact:** Projects without skills cannot be used for skill inference or accurate project recommendations.

**To Fix:** Enable skill tagging for projects. Encourage project owners to add relevant skills when creating projects.""",

    "projects_with_title_rule": """**Purpose:** Validates that projects have titles defined for identification and discoverability.

**Impact:** Projects without titles are difficult to find and cannot be properly displayed in search results.

**To Fix:** Require titles when creating projects. Add titles to existing projects that lack them.""",

    "projects_with_description_rule": """**Purpose:** Validates that projects have descriptions providing context about the work and skills developed.

**Impact:** Projects without descriptions provide limited value for showcasing employee work and capabilities.

**To Fix:** Add meaningful descriptions to projects describing objectives, responsibilities, and outcomes.""",

    "explore_project": """**Purpose:** Validates that Project exploration is enabled in Career Hub, allowing employees to discover project opportunities.

**Impact:** Without project exploration, employees cannot find relevant project opportunities for development.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Explore. Enable project exploration.""",

    "global_search_project": """**Purpose:** Validates that projects are included in Global Search for discoverability.

**Impact:** Without global search integration, projects are harder to discover across the platform.

**To Fix:** Navigate to Admin Console → Talent Management → Global Search. Enable projects in searchable entity types.""",

    "project_order_of_feeds": """**Purpose:** Validates that Recommended Projects feed is configured in the Career Hub home page order, ensuring project recommendations are visible.

**Impact:** Without this configuration, employees may miss project opportunities on their home page.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Home Page. Add 'recommended_projects' to the feed order.""",

    # TM - Internal Mobility
    "ijp_apply_redirect_url": """**Purpose:** Validates that the job application redirect URL is configured for Internal Mobility. This is required when apply_through_api is not supported and employees must be redirected to an external ATS.

**Impact:** Without proper redirect configuration, employees may encounter errors when applying to internal positions.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility → Application Flow. Configure apply_url_template with the correct ATS redirect URL pattern.""",

    "careerhub_employee_max_resume_size_bytes": """**Purpose:** Validates that maximum resume upload size is configured for job applications, preventing upload errors for large files.

**Impact:** Without size configuration, employees may encounter errors uploading resumes, causing frustration and application dropoff.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Set max_resume_size_bytes (recommended: 10MB = 10485760 bytes).""",

    "careerhub_employee_allowed_file_types": """**Purpose:** Validates that allowed file types for resume uploads are configured (e.g., PDF, DOC, DOCX).

**Impact:** Without file type configuration, employees may be unable to upload resumes in common formats.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Configure allowed_file_extensions to include PDF, DOC, DOCX, RTF, TXT.""",

    "employee_hiring_bands": """**Purpose:** Validates that hiring bands are configured to define role hierarchy. Bands determine job eligibility based on employee level.

**Impact:** Without hiring bands, job recommendations cannot be filtered by eligibility, and Career Navigator paths may not function correctly.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Configure job_bands with your organization's level structure. Map each band to seniority levels.""",

    "hiring_band_equivalence": """**Purpose:** Validates that band equivalencies are defined to group job bands across career tracks (e.g., Individual Contributor 6 = Manager 2).

**Impact:** Without equivalencies, employees may not see eligible positions across different career tracks.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Configure hiring_band_equivalence to map equivalent levels across tracks.""",

    "filter_by_hiring_band": """**Purpose:** Validates that hiring band filtering is enabled on the employee home page, showing only jobs the employee is eligible for based on their band.

**Impact:** Without this filter, employees may see jobs they're not eligible for, leading to confusion and poor experience.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Set filter_by_hiring_band to enabled (1 or true).""",

    "job_bands": """**Purpose:** Validates that job bands are configured to define role hierarchy for internal mobility workflows.

**Impact:** Without job bands, eligibility rules cannot be applied and Career Navigator cannot determine appropriate career paths.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Configure job_bands matching your organization's job architecture.""",

    # TM - Recommendations
    "recommended_jobs_filter_list": """**Purpose:** Validates that the filter list for recommended jobs is configured, ensuring personalized job recommendations on the Career Hub home page.

**Impact:** Without filter configuration, job recommendations may be irrelevant or missing entirely.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Feeds. Configure recommended_jobs with appropriate filters.""",

    "similar_people_filter_list": """**Purpose:** Validates that the Similar People recommendation filter is configured, showing employees with similar roles/skills for networking.

**Impact:** Without configuration, employees cannot discover peers for collaboration and networking.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Feeds. Configure similar_people with appropriate filters.""",

    # TM - Referrals
    "smart_apply_position_fq": """**Purpose:** Validates that the position filter query (fq) is configured for Smart Apply and Referrals, ensuring only appropriate positions appear.

**Impact:** Without this configuration, referrals may surface irrelevant or closed positions.

**To Fix:** Navigate to Admin Console → Talent Management → Referrals. Configure position_fq to filter for open, referral-eligible positions.""",

    "navbar_my_referrals": """**Purpose:** Validates that "My Referrals" appears in Career Hub navigation, allowing employees to track their referrals.

**Impact:** Without navigation visibility, employees cannot easily track referral activities and rewards.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub → Navigation. Add 'my_referrals' to navigation items.""",

    "myreferrals_config": """**Purpose:** Validates that My Referrals configuration is present, enabling referral tracking and management.

**Impact:** Without configuration, employees cannot view or manage their referral submissions.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure my_referrals section with appropriate settings.""",

    # TM - Succession Planning / Manager View
    "talent_hub_config": """**Purpose:** Validates that Talent Hub configuration is present, enabling HRBPs to access team planning and succession workflows.

**Impact:** Without configuration, HRBPs cannot access Talent Hub features for talent management.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure talent_hub section for HRBP access.""",

    "talent_hub_tab_order": """**Purpose:** Validates that Talent Hub tab order is configured correctly for intuitive HRBP navigation.

**Impact:** Incorrect tab order may confuse HRBPs and reduce efficiency.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure tab order in talent_hub settings.""",

    "team_table_order": """**Purpose:** Validates that team table column order is configured for the Talent Hub view.

**Impact:** Without proper column order, the team planning table may be confusing for HRBPs.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure team_table column order.""",

    "team_table_column_config": """**Purpose:** Validates that team table columns are properly configured and aligned with the defined order.

**Impact:** Misaligned columns can cause confusion in the team planning interface.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Verify column configuration matches column order.""",

    "profile_search_data_fields": """**Purpose:** Validates that profile search fields are configured for Talent Hub, enabling effective employee search.

**Impact:** Without proper field configuration, HRBPs may not be able to search effectively in Talent Hub.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure search fields in talent_hub settings.""",

    "talent_hub_filter_order": """**Purpose:** Validates that filter order is configured in Talent Hub for logical HRBP workflow.

**Impact:** Illogical filter order reduces usability and efficiency for HRBPs.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure filter order in talent_hub settings.""",

    "talent_hub_search_filters": """**Purpose:** Validates that search filters are configured in Talent Hub for effective talent analysis.

**Impact:** Missing or incorrect filters limit HRBPs' ability to analyze employee data.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure search_filters in talent_hub settings.""",

    "position_only_plan": """**Purpose:** Validates that position-only succession planning is configured when the organization uses position-based (not role-based) succession.

**Impact:** Without this configuration, succession planning may not align with organizational planning approach.

**To Fix:** Navigate to Admin Console → Talent Management → Succession Planning. Enable position_only_plan if using position-based succession.""",

    "hrbp_users_rule": """**Purpose:** Validates that users with HRBP permissions are created and configured to access HRBP features.

**Impact:** Without HRBP user assignments, succession planning and talent management features are inaccessible to HR teams.

**To Fix:** Navigate to Admin Console → Provisioning → Manage HRBP Users. Assign HRBP permissions with appropriate BU/Location scope.""",

    # TM - Mobile
    "mobile_app_top_nav": """**Purpose:** Validates that navigation links are configured for the Career Hub mobile app.

**Impact:** Without navigation configuration, mobile app users cannot navigate effectively.

**To Fix:** Navigate to Admin Console → Talent Management → Career Hub. Configure mobile_app_top_nav settings.""",

    # TA - Communication
    "email_config_enabled_cs": """**Purpose:** Validates that email configuration is present with valid 'reply_to_domain' and 'send_from_domain' settings, enabling recruiter-candidate email communication.

**Impact:** Without email configuration, recruiters cannot send emails to candidates from the platform.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Configuration. Configure reply_to_domain and send_from_domain with verified domains.""",

    "recruiter_missing_communication_email": """**Purpose:** Identifies users with send_messages permission who do not have a communication email configured, preventing them from sending candidate communications.

**Impact:** Users without communication email cannot send messages, blocking candidate engagement workflows.

**To Fix:** Navigate to Admin Console → Provisioning → Manage Users. Add communication_email for all users with PERM_SEND_MESSAGES permission.""",

    "sms_integration_enabled_cs": """**Purpose:** Validates that SMS integration is configured with Twilio credentials and phone number for candidate SMS communication.

**Impact:** Without SMS configuration, recruiters cannot send text messages to candidates.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Configuration. Configure sms_twilio_account_sid, sms_twilio_auth_token, and sms_twilio_number.""",

    "communication_channels": """**Purpose:** Validates that communication channels (SMS, WhatsApp) are configured for interview scheduling notifications.

**Impact:** Missing channel configuration can disrupt scheduling communications if candidates prefer non-email channels.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Enable desired communication channels (SMS, WhatsApp) in preferences.""",

    "whatsapp_integration_enabled_cs": """**Purpose:** Validates that WhatsApp Business API integration is configured for candidate WhatsApp messaging.

**Impact:** Without WhatsApp configuration, recruiters cannot communicate via WhatsApp, which is preferred in many regions.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Configuration. Configure whatsapp_twilio_account_sid, whatsapp_twilio_auth_token, whatsapp_twilio_messaging_service_id.""",

    # TA - Pipeline & Workflow
    "all_job_req_templates_in_stage_transition_map": """**Purpose:** Validates that all job requisition template IDs are present in the stage transition map, ensuring stage advances work for all position types.

**Impact:** Missing templates in stage transition map will cause stage advance failures for those position types.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Workflows. Ensure all job_req_template_ids are included in template_to_stage_transition_map.""",

    "leads_workflow": """**Purpose:** Validates that the Leads Workflow tab is configured on the pipeline page, which is the starting point for recruiters sourcing candidates.

**Impact:** Missing Leads tab prevents recruiters from accessing matched/sourced candidates.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Pipeline & Workflows. Verify leads tab is enabled in workflow_config.""",

    "applicants_workflow": """**Purpose:** Validates that the Applicants Workflow tab is configured on the pipeline page, showing candidates who have applied to positions.

**Impact:** Missing Applicants tab prevents recruiters from viewing and managing applicants.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Pipeline & Workflows. Verify applicants tab is enabled in workflow_config.""",

    "application_stage_advances_per_job_req_template_rule": """**Purpose:** Measures the success rate of stage advances per job requisition template. Target: 90% success rate.

**Impact:** Low success rate indicates stage transition map misconfiguration causing sync failures to the ATS.

**To Fix:** Review stage transition map for the failing template. Verify all stages are correctly mapped to ATS stages. Check ATS API connectivity.""",

    # TA - Candidate Profile
    "profile_sections_defined_cs": """**Purpose:** Validates that key profile sections (Overview, Experience, Education, Skills) are enabled for displaying candidate information to recruiters.

**Impact:** Missing profile sections prevent recruiters from viewing important candidate information.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Profile Display Config. Enable required sections.""",

    # TA - Copilot
    "copilot_feature_enabled_cs": """**Purpose:** Validates that Copilot AI features are enabled in configuration.

**Impact:** Without enablement, Copilot features like job description generation and scheduling assistance are unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Copilot Config. Set enabled: true.""",

    "copilot_capabilities_configured_cs": """**Purpose:** Validates that specific Copilot capabilities (job description generation, scheduling assistant, etc.) are enabled.

**Impact:** Without capability configuration, Copilot is enabled but has no usable features.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Copilot Capability Config. Enable desired capabilities.""",

    # TA - Diversity
    "diversity_config_enabled_cs": """**Purpose:** Validates that diversity configuration exists, enabling bias reduction features like profile masking.

**Impact:** Without configuration, diversity and bias reduction features cannot function.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Diversity Config. Initialize configuration.""",

    "masking_fields_configured_cs": """**Purpose:** Validates that specific fields are configured for masking (age, gender, ethnicity, etc.) when profile masking is enabled.

**Impact:** Masking enabled without field configuration means no fields are actually masked, defeating the purpose.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Diversity Config → Masking. Specify fields to mask.""",

    # TA - Events
    "event_config_enabled_cs": """**Purpose:** Validates that event recruiting is enabled, allowing creation and management of recruiting events.

**Impact:** Without enablement, recruiting events cannot be created or managed.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Event Config. Set enabled: true.""",

    "event_stages_configured_cs": """**Purpose:** Validates that event-specific pipeline stages (Registered, Attended, Interviewed, etc.) are configured.

**Impact:** Without event stages, candidates in events cannot be moved through the pipeline.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Event Workflow Config. Define event stages.""",

    "event_home_config_valid_cs": """**Purpose:** Validates that event home configuration is set up for displaying events list.

**Impact:** Without configuration, events list may not display correctly to recruiters.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Event Home Config. Configure display settings.""",

    # TA - Global Search
    "global_search_enabled_cs": """**Purpose:** Validates that global search is enabled, allowing recruiters to search across the talent network.

**Impact:** Without global search, recruiters cannot search for candidates effectively.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Global Search Config. Set enabled: true.""",

    "search_filters_configured_cs": """**Purpose:** Validates that search filters (location, skills, experience, etc.) are configured for refining search results.

**Impact:** Without filters, recruiters cannot effectively narrow down candidate search results.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Global Search Config. Configure filters for location, skills, experience, contact_consent, etc.""",

    # TA - Interview Feedback
    "feedback_config_enabled_cs": """**Purpose:** Validates that interview feedback feature is enabled for structured interviewer feedback collection.

**Impact:** Without enablement, interview feedback cannot be collected through the platform.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback Config. Set enabled: true.""",

    "feedback_forms_configured_cs": """**Purpose:** Validates that at least one feedback form template exists with questions for interviewers.

**Impact:** Without form templates, interviewers cannot submit structured feedback.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback. Create at least one feedback form template.""",

    "feedback_report": """**Purpose:** Validates that feedback report columns are configured for consolidated feedback viewing.

**Impact:** Misconfigured report affects how recruiters and hiring managers view interview feedback.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback. Configure report columns, display names, and formatting.""",

    "dashboard_columns_list": """**Purpose:** Validates that feedback dashboard columns are configured for the Interview Feedback Center.

**Impact:** Missing or incorrect columns reduce dashboard usefulness for managing feedback.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback. Configure dashboard_columns_list.""",

    # TA - Scheduling
    "scheduling_config": """**Purpose:** Validates that smart scheduling is enabled with calendar integration configured.

**Impact:** Without scheduling configuration, interview scheduling features cannot be used.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Set enabled: true and configure calendar provider.""",

    "scheduling_timezone": """**Purpose:** Validates that a default timezone is configured for interview scheduling.

**Impact:** Missing timezone can cause scheduling confusion and incorrect time display.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Set default timezone.""",

    "standard_schedule_action": """**Purpose:** Validates that the scheduling action is enabled on pipeline/profile pages.

**Impact:** Without the action, recruiters cannot initiate interview scheduling from the pipeline.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Enable schedule action in pipeline configuration.""",

    "scheduling_integration_configured_cs": """**Purpose:** Validates that calendar integration (Google/Outlook/Exchange) is configured for checking availability and creating events.

**Impact:** Without calendar integration, the system cannot check interviewer availability or create calendar events.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Configure calendar provider and OAuth credentials.""",

    "scheduling_templates_exist_cs": """**Purpose:** Validates that at least one scheduling template exists defining interview structure (type, duration, participants).

**Impact:** Without templates, interviews cannot be scheduled as there's no defined structure.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling Templates. Create at least one template with duration, interview type, and participant roles.""",

    "enabled_for_scheduling": """**Purpose:** Validates that a calendar provider is configured for interview scheduling.

**Impact:** Without calendar provider, interviews cannot be synchronized with calendars.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Configure calendarProvider (Google Calendar, Microsoft 365, or No Calendar).""",

    # TA - Smart Campaigns
    "campaign_config_enabled_cs": """**Purpose:** Validates that smart campaigns feature is enabled for candidate nurture workflows.

**Impact:** Without enablement, campaign features for candidate engagement are unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Campaign Config. Set enabled: true.""",

    "campaign_email_templates_exist_cs": """**Purpose:** Validates that email templates exist for campaign use, tagged appropriately for campaign workflows.

**Impact:** Without campaign templates, campaigns cannot send emails.

**To Fix:** Navigate to Admin Console → Email Templates. Create at least one template tagged for campaign use.""",

    # TA - Communities
    "community_config_enabled_cs": """**Purpose:** Validates that talent communities feature is enabled for talent pool management.

**Impact:** Without enablement, talent community features are unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Community Home Config. Set enabled: true.""",

    "community_stages_configured_cs": """**Purpose:** Validates that community pipeline stages are configured for managing prospect progression.

**Impact:** Without stages, community members cannot be managed through a pipeline workflow.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Community Workflow Config. Define community stages.""",

    "community_home": """**Purpose:** Validates that Community Home configuration includes available_filters, filter_to_fq_data_map, and columns for the community dashboard.

**Impact:** Missing configuration can render the Community Home page non-functional or impaired.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Communities. Configure available_filters, filter_to_fq_data_map, and columns.""",

    "community_workflows": """**Purpose:** Validates that community_workflow_config is defined per community type with valid display_name and workflow steps.

**Impact:** Without workflow configuration, communities cannot progress prospects or reflect status.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Community Workflow Config. Define workflows per community type.""",

    # TA - Workflow Automation
    "workflow_automation_enabled_cs": """**Purpose:** Validates that workflow automation feature is enabled for automated candidate workflows.

**Impact:** Without enablement, automated workflows cannot be created or executed.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Workflow Automation Config. Set enabled: true.""",

    "workflow_triggers_valid_cs": """**Purpose:** Validates that at least one workflow trigger is configured with valid events and conditions.

**Impact:** Without triggers, workflows cannot execute as there's no defined trigger condition.

**To Fix:** Navigate to Admin Console → Workflows. Configure at least one trigger with event type and conditions.""",

    # TA - Chrome Extension
    "extension_communities_disabled_text": """**Purpose:** Validates that a clear message is configured when Communities feature is disabled in the Chrome Extension.

**Impact:** Without clear messaging, users may be confused about feature unavailability.

**To Fix:** Configure descriptive disabled text in extension configuration.""",

    "extension_reminder_action": """**Purpose:** Validates that reminder functionality is configured in the extension, allowing team-wide visibility of candidate reminders.

**Impact:** Without reminders visible in extension, team members may duplicate outreach efforts.

**To Fix:** Configure reminder_action in extension configuration.""",

    "app_configs": """**Purpose:** Validates that hostname configurations are set for LinkedIn, Naukri, and GitHub in the Chrome Extension.

**Impact:** Missing hostname configuration prevents proper profile parsing from these sites.

**To Fix:** Configure app_configs with correct hostnames for each supported site.""",

    "extension_actions": """**Purpose:** Validates that all extension actions (save candidate, mark status, set reminder) are properly configured.

**Impact:** Missing or misconfigured actions prevent recruiters from managing candidates efficiently.

**To Fix:** Configure all actions and sub-actions in extension configuration for candidate management workflows.""",

    # PCS - Base Configuration
    "pcsx_base_enabled_cs": """**Purpose:** Validates that PCS (Personalized Career Site) base configuration is enabled. This is the foundation for all career site functionality.

**Impact:** Without base configuration, the career site will not be accessible to candidates.

**To Fix:** Navigate to Admin Console → Talent Experience → Career Site & Referrals. Set enabled: true in pcsx_base_config.""",

    "apply_form_configured_cs": """**Purpose:** Validates that the application form configuration exists, defining required fields and workflow for candidate applications.

**Impact:** Without form configuration, candidates cannot apply to positions.

**To Fix:** Navigate to Admin Console → Talent Experience → Career Site & Referrals → Apply Form. Configure required and optional fields.""",

    # PCS - Branding
    "pcs_logo_configured_cs": """**Purpose:** Validates that company logo is uploaded and configured for the career site.

**Impact:** Without logo, career site displays without company branding, reducing brand recognition.

**To Fix:** Navigate to Admin Console → Talent Experience → Branding Config. Upload company logo and verify URL is valid.""",

    "pcs_colors_configured_cs": """**Purpose:** Validates that brand colors are configured with valid hex codes (e.g., #146da6).

**Impact:** Without color configuration, career site uses default colors instead of brand colors.

**To Fix:** Navigate to Admin Console → Talent Experience → Branding Config. Set primary and secondary colors in hex format.""",

    # PCS - Login/Signup
    "login_signup_configured_cs": """**Purpose:** Validates that login and signup configuration is valid, defining authentication methods and required fields.

**Impact:** Without configuration, candidates cannot create accounts or log in to the career site.

**To Fix:** Navigate to Admin Console → Talent Experience → Login Signup Config. Configure authentication method and required fields.""",

    "candidate_profile_enabled_cs": """**Purpose:** Validates that candidate profile configuration is enabled, allowing candidates to create and manage their profiles.

**Impact:** Without enablement, candidates cannot maintain living profiles with updated information.

**To Fix:** Navigate to Admin Console → Talent Experience → Candidate Profile Config. Set enabled: true.""",

    "profile_fields_configured_cs": """**Purpose:** Validates that profile fields are defined for candidate profiles (name, email, phone, experience, education, skills).

**Impact:** Without field configuration, candidates cannot maintain complete profiles, affecting match quality.

**To Fix:** Navigate to Admin Console → Talent Experience → Candidate Profile Config. Define profile fields and mark required/optional.""",

    # PCS - Job Search
    "search_config_enabled_cs": """**Purpose:** Validates that job search is enabled on the career site.

**Impact:** Without search, candidates cannot find jobs effectively.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Search. Set enabled: true.""",

    "search_filters_available_cs": """**Purpose:** Validates that search filters (location, department, job type, etc.) are configured.

**Impact:** Without filters, candidates can search but cannot refine results, leading to poor experience.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Search. Configure filters for location, department, job type, etc.""",

    # PCS - Smart Apply
    "smart_apply_enabled_cs": """**Purpose:** Validates that Smart Apply is enabled with proper ATS integration for application sync.

**Impact:** Without Smart Apply, applications will not sync to the ATS, breaking the recruiting workflow.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Set enabled: true and configure ATS integration.""",

    "field_mapping_complete_cs": """**Purpose:** Validates that all required fields are mapped between Eightfold and the ATS.

**Impact:** Incomplete mapping causes application data to be incomplete in the ATS.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Field Mapping. Map all required fields.""",

    "linkoff_enabled_cs": """**Purpose:** Validates that Link-off (redirect to external ATS) is enabled when not using Smart Apply.

**Impact:** Without link-off configuration, applications cannot be properly routed to external ATS.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Apply Form → Link Off. Set enabled: true.""",

    "linkoff_redirection_cs": """**Purpose:** Validates that link-off redirect URL is configured when link-off is enabled.

**Impact:** Without redirect URL, candidates cannot be sent to the external application system.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Apply Form → Link Off. Configure apply_redirect_url.""",

    # PCS - Talent Network
    "talent_network_enabled_cs": """**Purpose:** Validates that Talent Network join feature is enabled, allowing candidates to join without applying to specific positions.

**Impact:** Without enablement, talent pool growth is limited to only active applicants.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Enable talent network join option.""",

    "talent_network_form_configured_cs": """**Purpose:** Validates that the Talent Network join form is configured with required fields.

**Impact:** Without form configuration, candidates cannot join the talent network.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Configure talent network form fields.""",

    # PCS - Job Distribution
    "job_feed_enabled_cs": """**Purpose:** Validates that job feed (XML) is enabled for distribution to job boards and search engines.

**Impact:** Without job feed, jobs will not be distributed to external job boards or indexed by search engines.

**To Fix:** Navigate to Admin Console → Talent Experience → Job Feed Config. Set enabled: true.""",

    "seo_config_valid_cs": """**Purpose:** Validates that SEO configuration is valid with proper meta tags, structured data, and sitemap settings.

**Impact:** Poor SEO configuration reduces career site visibility in search engine results.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → SEO. Configure meta tags, structured data, and enable sitemap.""",

    # PCS - Job Alerts
    "job_alerts_enabled_cs": """**Purpose:** Validates that job alerts are enabled for sending personalized job notifications to candidates.

**Impact:** Without job alerts, candidates do not receive notifications about new matching jobs.

**To Fix:** Navigate to Admin Console → Talent Experience → Notification Config. Enable job alerts.""",

    "job_alert_frequency_configured_cs": """**Purpose:** Validates that job alert frequency options are configured (daily, weekly, etc.).

**Impact:** Without frequency options, job alerts may send too frequently or not at all.

**To Fix:** Navigate to Admin Console → Talent Experience → Candidate Notifications Config. Configure frequency options.""",

    # PCS - Source Tracking
    "source_tracking_enabled_cs": """**Purpose:** Validates that source tracking is enabled for capturing where candidates come from.

**Impact:** Without source tracking, recruitment marketing effectiveness cannot be measured.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Source Tracking. Set enabled: true.""",

    "source_parameters_configured_cs": """**Purpose:** Validates that source parameters (UTM, referral codes) are configured for attribution.

**Impact:** Without parameter configuration, sources are not captured correctly.

**To Fix:** Navigate to Admin Console → Talent Experience → Source Map Config. Configure UTM parameter mapping.""",

    "source_ats_sync_configured_cs": """**Purpose:** Validates that source tracking data is mapped to sync with applications to the ATS.

**Impact:** Without source sync, source attribution is lost when applications sync to ATS.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Source Mapping. Map source field to ATS.""",

    # PCS - Referrals
    "referrals_enabled_cs": """**Purpose:** Validates that smart referral feature is enabled for employee referrals with AI matching.

**Impact:** Without enablement, employee referral functionality is unavailable.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Enable referrals.""",

    "referral_workflow_configured_cs": """**Purpose:** Validates that referral workflow is configured with submission form, tracking, and notifications.

**Impact:** Without workflow configuration, the referral process is incomplete.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Referrals. Configure submission form and tracking.""",

    # PCS - Domain
    "custom_domain_configured_cs": """**Purpose:** Validates that custom domain (e.g., careers.company.com) is configured for branded career site URL.

**Impact:** Without custom domain, career site uses default Eightfold domain.

**To Fix:** Navigate to Admin Console → Talent Experience → Domain Config. Configure custom domain and verify DNS CNAME record.""",

    "ssl_certificate_valid_cs": """**Purpose:** Validates that SSL certificate is present and valid for secure HTTPS access.

**Impact:** Invalid SSL causes security warnings or blocks access to career site.

**To Fix:** Navigate to Admin Console → Talent Experience → Domain Config. Verify SSL certificate is uploaded and not expired.""",

    # PCS - Landing Pages
    "landing_config_enabled_cs": """**Purpose:** Validates that landing page configuration is enabled for custom landing pages.

**Impact:** Without enablement, custom landing pages cannot be created.

**To Fix:** Navigate to Admin Console → Talent Experience → Landing Config. Initialize configuration.""",

    "landing_pages_valid_cs": """**Purpose:** Validates that landing pages have valid URLs and are accessible.

**Impact:** Invalid URLs cause landing pages to be inaccessible.

**To Fix:** Navigate to Admin Console → Talent Experience → Landing Config. Verify URL paths are valid and accessible.""",

    # PCS - Microsites
    "microsite_configs_valid_cs": """**Purpose:** Validates that each microsite has complete configuration including branding, domain mapping, and job filters.

**Impact:** Incomplete microsite configuration causes display issues or wrong job listings.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Microsites. Complete configuration for each microsite.""",

    # PCS - Tracking
    "tracking_scripts_valid_cs": """**Purpose:** Validates that tracking scripts (Google Analytics, etc.) have valid JavaScript and are assigned to correct events.

**Impact:** Invalid scripts cause tracking failures and analytics data gaps.

**To Fix:** Navigate to Admin Console → Talent Experience → Tracking Pixel Config. Verify JavaScript syntax and event assignments.""",

    # PCS - Withdraw
    "withdraw_enabled_cs": """**Purpose:** Validates that application withdrawal is enabled for candidates.

**Impact:** Without withdrawal capability, candidates cannot remove applications, affecting experience.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Applications. Enable withdraw option.""",

    "withdraw_workflow_valid_cs": """**Purpose:** Validates that withdrawal workflow includes confirmation, ATS sync, and candidate notification.

**Impact:** Incomplete workflow may cause withdrawals not to sync to ATS or candidates not to receive confirmation.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Applications → Withdraw. Configure confirmation dialog and ATS sync.""",

    # PCS - PYMWW
    "pymww_enabled_cs": """**Purpose:** Validates that "People You May Work With" feature is enabled on job detail pages.

**Impact:** Without enablement, candidates don't see potential colleagues, reducing engagement.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Position Details. Enable pymww_config.""",

    "pymww_criteria_configured_cs": """**Purpose:** Validates that PYMWW selection criteria (department, location matching) are configured.

**Impact:** Without criteria, PYMWW may show irrelevant employees.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Position Details → PYMWW. Configure selection criteria and fq.""",

    # PCS - Chatbot
    "chatbot_config_enabled_cs": """**Purpose:** Validates that candidate-facing Copilot/chatbot is enabled.

**Impact:** Without enablement, AI assistance is unavailable to candidates on career site.

**To Fix:** Navigate to Admin Console → Talent Experience → Chatbot Config. Set enabled: true.""",

    # PCS - Match Score
    "star_threshold": """**Purpose:** Validates that strong_match_threshold is configured for job matching display. This prevents poorly matched candidates from being shown.

**Impact:** Without threshold, irrelevant matches may be displayed, reducing quality of candidate and recruiter experience.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Search. Configure strong_match_threshold.""",

    # Sentence-based rule IDs that need enhancement
    "Alert frequency not configured. Go to integrations/candidate_notifications_config and configure frequency options.": """**Purpose:** Validates that job alert frequency options are configured for candidates, allowing them to choose how often they receive job recommendations.

**Impact:** Without frequency configuration, candidates may receive too many or too few notifications, impacting engagement.

**To Fix:** Navigate to Admin Console → Talent Experience → Candidate Notifications Config. Configure frequency options (daily, weekly, biweekly) with appropriate default.""",

    "Anonymization rules should be configured based on defined criteria.": """**Purpose:** Validates that anonymization rules are defined with specific criteria for removing identifying information from candidate profiles during bias-conscious workflows.

**Impact:** Without clear anonymization rules, profile masking may not adequately remove identifying information, defeating the purpose.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Diversity Config → Anonymization. Configure rules for each masked field with clear criteria.""",

    "Application form not configured. Go to integrations/pcsx_base_config Apply Form and configure fields.": """**Purpose:** Validates that the job application form is configured with the required and optional fields for candidates to submit applications.

**Impact:** Without application form configuration, candidates cannot apply to positions on the career site.

**To Fix:** Navigate to Admin Console → Talent Experience → Career Site & Referrals → Apply Form. Configure required fields (name, email, resume) and optional fields (phone, cover letter).""",

    "Assessment error messages should be captured properly.": """**Purpose:** Validates that assessment integration error messages are properly configured to provide clear feedback when assessment triggers fail.

**Impact:** Without proper error messaging, troubleshooting assessment failures becomes difficult.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Assessment Config. Configure error_messages for common failure scenarios.""",

    "Assessment triggers should be configured with all required fields.": """**Purpose:** Validates that assessment triggers are fully configured with all required fields including trigger event, assessment type, and conditions.

**Impact:** Incomplete trigger configuration prevents assessments from being sent to candidates automatically.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Assessment Config → Triggers. Ensure each trigger has event type, assessment provider, conditions defined.""",

    "Brand colors not configured. Go to integrations/branding_config and configure primary and secondary colors.": """**Purpose:** Validates that brand colors are configured with valid hex codes for the career site, ensuring consistent brand representation.

**Impact:** Without brand colors, the career site uses default colors instead of company branding, reducing brand recognition.

**To Fix:** Navigate to Admin Console → Talent Experience → Branding Config. Set primary_color and secondary_color in hex format (e.g., #146da6).""",

    "Calendar integration not configured. Go to integrations/scheduling_config and configure calendar provider.": """**Purpose:** Validates that calendar integration is configured for interview scheduling, enabling automatic availability checking and calendar event creation.

**Impact:** Without calendar integration, interviewers cannot have their availability checked automatically.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling Config. Select calendar provider (Google/Microsoft) and complete OAuth configuration.""",

    "Campaign templates not found. Go to integrations/email_templates and create templates for campaign use.": """**Purpose:** Validates that email templates exist for use in smart campaigns, enabling automated candidate nurture sequences.

**Impact:** Without campaign templates, smart campaigns cannot send automated emails to candidates.

**To Fix:** Navigate to Admin Console → Email Templates. Create templates and tag them for campaign use. Include merge fields for personalization.""",

    "Candidate copilot not enabled. Go to integrations/chatbotx_config and set enabled: true for candidate copilot.": """**Purpose:** Validates that the candidate-facing Copilot (AI assistant) is enabled to help candidates with job search and application questions.

**Impact:** Without Copilot, candidates don't have AI-powered assistance on the career site, reducing self-service capabilities.

**To Fix:** Navigate to Admin Console → Talent Experience → Chatbot Config. Set enabled: true and configure greeting message.""",

    "Candidate profile not enabled. Go to integrations/candidate_profile_config and set enabled: true.": """**Purpose:** Validates that candidate profile feature is enabled, allowing candidates to create and manage their profiles on the career site.

**Impact:** Without profile enablement, candidates cannot maintain living profiles with updated information.

**To Fix:** Navigate to Admin Console → Talent Experience → Candidate Profile Config. Set enabled: true.""",

    "Community stages not configured. Go to integrations/community_workflow_config and define stages.": """**Purpose:** Validates that pipeline stages are configured for talent communities, enabling progression tracking for community members.

**Impact:** Without stages, community members cannot be tracked through engagement workflows.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Community Workflow Config. Define stages (e.g., New, Engaged, Nurtured, Applied).""",

    "Company logo missing. Go to integrations/branding_config and upload company logo.": """**Purpose:** Validates that the company logo is uploaded for the career site, ensuring proper brand representation.

**Impact:** Without a logo, the career site displays without company branding, reducing recognition and trust.

**To Fix:** Navigate to Admin Console → Talent Experience → Branding Config. Upload logo image (recommended: PNG with transparent background, minimum 200x50 pixels).""",

    "Copilot capabilities not configured. Go to integrations/copilot_capability_config and enable at least one capability.": """**Purpose:** Validates that specific Copilot capabilities are enabled (e.g., job description generation, scheduling assistant).

**Impact:** Without capability configuration, Copilot is enabled but has no functional features.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Copilot Capability Config. Enable desired capabilities.""",

    "Copilot not enabled. Go to integrations/copilot_config and set enabled: true.": """**Purpose:** Validates that Copilot AI features are enabled for recruiters and hiring managers.

**Impact:** Without Copilot, AI-powered features like job description generation are unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Copilot Config. Set enabled: true.""",

    "Custom domain not configured. Go to integrations/domain_whitelabeling_config and configure custom domain.": """**Purpose:** Validates that a custom domain (e.g., careers.company.com) is configured for the career site instead of the default Eightfold subdomain.

**Impact:** Without custom domain, the career site URL includes the Eightfold domain, which may not align with company branding.

**To Fix:** Navigate to Admin Console → Talent Experience → Domain Config. Configure custom domain and add the required DNS CNAME record.""",

    "Diversity configuration missing. Go to integrations/diversity_config and initialize the configuration.": """**Purpose:** Validates that diversity configuration exists, which is required for enabling profile masking and bias reduction features.

**Impact:** Without configuration, diversity and bias reduction features cannot be activated.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Diversity Config. Initialize configuration and enable desired features.""",

    "email_config is missing or null. Go to  integrations/email_config and verify the configuration exists and is saved.": """**Purpose:** Validates that email configuration exists with valid send_from_domain and reply_to_domain settings for candidate communications.

**Impact:** Without email configuration, recruiters cannot send emails to candidates from the platform.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Configuration. Configure send_from_domain and reply_to_domain with verified domains.""",

    "Event home configuration invalid. Go to integrations/planned_event_home_config and configure display settings.": """**Purpose:** Validates that the Event Home page is properly configured with display settings for the events list.

**Impact:** Invalid configuration may cause the events list to display incorrectly or not at all.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Event Home Config. Configure columns, filters, and display settings.""",

    "Event recruiting not enabled. Go to integrations/planned_event_config and set enabled: true.": """**Purpose:** Validates that event recruiting is enabled, allowing creation and management of recruiting events (career fairs, info sessions, etc.).

**Impact:** Without enablement, event recruiting features are completely unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Event Config. Set enabled: true.""",

    "Event stages not configured. Go to integrations/planned_event_workflow_config and define event stages.": """**Purpose:** Validates that event-specific pipeline stages (Registered, Attended, Interviewed, etc.) are configured for candidate tracking.

**Impact:** Without stages, candidates in events cannot be progressed through event workflows.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Event Workflow Config. Define event stages with appropriate actions.""",

    "Feedback forms not configured. Go to integrations/interview_feedback_config and create at least one feedback form template.": """**Purpose:** Validates that at least one interview feedback form template exists with questions for interviewers to provide structured feedback.

**Impact:** Without form templates, interviewers cannot submit structured feedback through the platform.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback. Create at least one feedback form template with rating scales and open-ended questions.""",

    "Field mapping incomplete. Go to integrations/smart_apply_config Field Mapping and map all required fields.": """**Purpose:** Validates that all required application fields are mapped between Eightfold and the ATS for successful application sync.

**Impact:** Incomplete field mapping causes application data to be incomplete or missing in the ATS.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Field Mapping. Map all required fields (name, email, resume, phone, etc.).""",

    "Global search not enabled. Go to integrations/global_search_config and set enabled: true.": """**Purpose:** Validates that global search is enabled for recruiters to search across the entire talent network.

**Impact:** Without global search, recruiters cannot effectively find candidates across all sources.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Global Search Config. Set enabled: true.""",

    "Interview feedback not configured. Go to integrations/interview_feedback_config and set enabled: true.": """**Purpose:** Validates that interview feedback feature is enabled for collecting structured interviewer feedback.

**Impact:** Without enablement, interview feedback cannot be collected through the platform.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback Config. Set enabled: true.""",

    "Job alerts not enabled. Go to integrations/notification_config and enable job alerts.": """**Purpose:** Validates that job alerts are enabled, allowing candidates to receive personalized job recommendations via email.

**Impact:** Without job alerts, candidates don't receive notifications about new matching jobs, reducing engagement.

**To Fix:** Navigate to Admin Console → Talent Experience → Notification Config. Enable job alerts and configure frequency options.""",

    "Job feed not enabled. Go to integrations/job_feed_config and set enabled: true.": """**Purpose:** Validates that job feed generation is enabled for distributing jobs to external job boards and search engines.

**Impact:** Without job feed, jobs are not distributed to Indeed, LinkedIn, Glassdoor, or indexed by Google for Jobs.

**To Fix:** Navigate to Admin Console → Talent Experience → Job Feed Config. Set enabled: true.""",

    "Join form not configured. Go to integrations/smart_apply_config and configure talent network form.": """**Purpose:** Validates that the Talent Network join form is configured with appropriate fields for candidates joining without applying to specific positions.

**Impact:** Without form configuration, candidates cannot join the talent network, limiting talent pool growth.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Talent Network. Configure form fields (name, email, phone, interests).""",

    "Landing pages not configured. Go to integrations/landing_config and initialize configuration.": """**Purpose:** Validates that landing page configuration is initialized, enabling creation of custom landing pages for campaigns.

**Impact:** Without configuration, custom landing pages cannot be created for targeted recruitment campaigns.

**To Fix:** Navigate to Admin Console → Talent Experience → Landing Config. Initialize configuration.""",

    "Landing page URLs invalid. Go to integrations/landing_config and verify URL paths.": """**Purpose:** Validates that landing page URLs are valid and accessible, ensuring candidates can reach campaign-specific pages.

**Impact:** Invalid URLs cause landing pages to be inaccessible, breaking campaign links.

**To Fix:** Navigate to Admin Console → Talent Experience → Landing Config. Verify all URL paths are valid and test accessibility.""",

    "Linkoff config is enabled but redirect url is not added. Go to Integrations pcsx_base_config apply_form_config link_off_apply_config and add apply_redirect_url": """**Purpose:** Validates that when link-off (redirect to external ATS) is enabled, the redirect URL is configured.

**Impact:** Missing redirect URL causes candidates to be unable to complete applications.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Apply Form → Link Off. Add apply_redirect_url with the correct ATS application URL pattern.""",

    "Linkoff config is not enabled. Go to Integrations pcsx_base_config apply_form_config link_off_apply_config and set enabled to true": """**Purpose:** Validates that link-off configuration is enabled when redirecting candidates to an external ATS for application completion.

**Impact:** Without link-off enabled, candidates cannot be redirected to external application systems.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Apply Form → Link Off. Set enabled: true.""",

    "Login/signup not configured. Go to integrations/login_signup_config and configure authentication method.": """**Purpose:** Validates that login and signup configuration is defined, specifying authentication methods and required fields for candidate accounts.

**Impact:** Without configuration, candidates cannot create accounts or log in to the career site.

**To Fix:** Navigate to Admin Console → Talent Experience → Login Signup Config. Configure authentication method (email/social) and required fields.""",

    "Masking fields not configured. Go to integrations/diversity_config and specify which fields to mask.": """**Purpose:** Validates that when profile masking is enabled, specific fields are configured for masking (e.g., name, age, gender, photos).

**Impact:** Masking enabled without field specification means no fields are actually hidden, defeating the purpose.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Diversity Config → Masking. Specify fields to mask in masking_config.""",

    "Match scores should be consistent between PCS and TA.": """**Purpose:** Validates that match score thresholds and algorithms are consistent between the career site (PCS) and Talent Acquisition modules.

**Impact:** Inconsistent scoring can confuse candidates (seeing different match levels) and affect recruiter trust in AI matching.

**To Fix:** Review strong_match_threshold in both PCS and TA configurations. Ensure algorithm versions and thresholds are aligned.""",

    "Microsite configuration incomplete. Go to integrations/pcsx_base_config Microsites and verify configuration.": """**Purpose:** Validates that each microsite has complete configuration including branding, domain mapping, job filters, and content.

**Impact:** Incomplete configuration causes microsites to display incorrectly or show wrong job listings.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Microsites. Complete all configuration sections for each microsite.""",

    "Microsite isolation should be configured properly.": """**Purpose:** Validates that candidate profiles and applications are properly isolated between the parent career site and microsites when required.

**Impact:** Without proper isolation, candidate data may leak between sites or candidates may need to re-register.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Microsites. Configure profile_isolation and application_isolation settings.""",

    "Mobile configurations should be correctly defined using device_configuration settings.": """**Purpose:** Validates that mobile-specific configurations are defined for the career site, ensuring proper display on mobile devices.

**Impact:** Without mobile configuration, the career site may not display correctly on phones and tablets.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config. Configure device_configuration settings for mobile display.""",

    "PCS base configuration not enabled. Go to integrations/pcsx_base_config and set enabled: true.": """**Purpose:** Validates that PCS (Personalized Career Site) base configuration is enabled, which is the foundation for all career site functionality.

**Impact:** Without base configuration enabled, the career site is completely inaccessible to candidates.

**To Fix:** Navigate to Admin Console → Talent Experience → Career Site & Referrals. Set enabled: true in pcsx_base_config.""",

    "People You May Work With not enabled. Go to integrations/pcsx_base_config position_details_config sections_config and enable pymww_config section.": """**Purpose:** Validates that "People You May Work With" feature is enabled on job detail pages, showing potential colleagues.

**Impact:** Without PYMWW, candidates don't see potential team members, reducing engagement and conversion.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Position Details → Sections. Enable pymww_config section.""",

    "Profile fields not configured. Go to integrations/candidate_profile_config and define profile fields.": """**Purpose:** Validates that candidate profile fields are defined (name, email, phone, experience, education, skills) for profile creation.

**Impact:** Without field configuration, candidates cannot create complete profiles, affecting match quality.

**To Fix:** Navigate to Admin Console → Talent Experience → Candidate Profile Config. Define profile fields and mark which are required/optional.""",

    "Profile sections not configured. Go to integrations/profile_display_config and ensure at least these sections are enabled.": """**Purpose:** Validates that key profile sections are enabled for displaying candidate information to recruiters (Overview, Experience, Education, Skills).

**Impact:** Missing sections prevent recruiters from viewing important candidate information.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Profile Display Config. Enable required sections.""",

    "Referral workflow not configured. Go to integrations/smart_apply_config Referrals and configure workflow.": """**Purpose:** Validates that the referral workflow is fully configured with submission form, tracking stages, and notifications.

**Impact:** Without workflow configuration, the employee referral process is incomplete or non-functional.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Referrals. Configure submission form, tracking, and notifications.""",

    "Scheduling center filters should have appropriate facet limits.": """**Purpose:** Validates that scheduling center filters have appropriate maximum values (facet_limit) to prevent overwhelming filter options.

**Impact:** Without limits, filters may show too many options, making the interface difficult to use.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling Config → Filters. Set appropriate facet_limit values for each filter.""",

    "Scheduling configuration not enabled. Go to integrations/scheduling_config and set enabled: true.": """**Purpose:** Validates that smart scheduling feature is enabled for interview scheduling functionality.

**Impact:** Without enablement, interview scheduling features are completely unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling Config. Set enabled: true.""",

    "Scheduling templates not found. Go to integrations/scheduling_config and create at least one template.": """**Purpose:** Validates that at least one scheduling template exists defining interview structure (type, duration, participants).

**Impact:** Without templates, interviews cannot be scheduled as there's no defined structure.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling Templates. Create templates with duration, interview type, and participant roles.""",

    "Search filters missing. Go to integrations/pcsx_base_config Search and configure filters.": """**Purpose:** Validates that job search filters are configured on the career site (location, department, job type, etc.).

**Impact:** Without filters, candidates can search but cannot refine results, leading to poor user experience.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Search. Configure filters for location, department, job type.""",

    "Search filters not configured. Go to integrations/global_search_config and configure filters.": """**Purpose:** Validates that search filters are configured for global talent search (skills, location, experience, etc.).

**Impact:** Without filters, recruiters cannot effectively narrow down candidate search results.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Global Search Config. Configure filters for skills, location, experience, contact consent.""",

    "Search not configured. Go to integrations/pcsx_base_config Search and configure search settings.": """**Purpose:** Validates that job search functionality is configured on the career site.

**Impact:** Without search configuration, candidates cannot find jobs on the career site.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Search. Configure search settings including filters and display options.""",

    "Selection criteria missing. Go to integrations/pcsx_base_config position_details_config sections_config pymww_config and add the fq.": """**Purpose:** Validates that PYMWW (People You May Work With) selection criteria are configured to determine which employees are shown.

**Impact:** Without selection criteria, PYMWW may show irrelevant employees or none at all.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Position Details → PYMWW. Add filter query (fq) for employee selection.""",

    "SEO not configured. Go to integrations/pcsx_base_config SEO and configure meta tags and structured data.": """**Purpose:** Validates that SEO configuration is set up with meta tags, structured data, and sitemap for search engine visibility.

**Impact:** Poor SEO configuration reduces career site visibility in search engine results.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → SEO. Configure title templates, meta descriptions, structured data, and sitemap.""",

    "Smart Apply not enabled. Go to integrations/smart_apply_config and set enabled: true.": """**Purpose:** Validates that Smart Apply is enabled for one-click applications with ATS integration.

**Impact:** Without Smart Apply, applications require more steps and may not sync properly to the ATS.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Set enabled: true and configure ATS integration.""",

    "Smart campaigns not enabled. Go to integrations/campaign_config and set enabled: true.": """**Purpose:** Validates that smart campaigns feature is enabled for automated candidate nurture workflows.

**Impact:** Without enablement, automated campaign features for candidate engagement are unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Campaign Config. Set enabled: true.""",

    "Smart referrals not enabled. Go to integrations/smart_apply_config and enable referrals functionality.": """**Purpose:** Validates that smart referral feature is enabled for employee referrals with AI matching.

**Impact:** Without enablement, employee referral functionality with AI matching is unavailable.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Enable referrals.""",

    "SMS integration not configured. Go to  integrations/email_config and verify SMS provider and credentials.": """**Purpose:** Validates that SMS integration is configured with Twilio credentials for candidate text messaging.

**Impact:** Without SMS configuration, recruiters cannot send text messages to candidates.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Config. Configure Twilio account SID, auth token, and phone number.""",

    "Source parameters not configured. Go to integrations/source_map_config and configure source tracking.": """**Purpose:** Validates that source tracking parameters (UTM codes, referral sources) are configured for attribution.

**Impact:** Without parameter configuration, candidate sources are not captured correctly.

**To Fix:** Navigate to Admin Console → Talent Experience → Source Map Config. Configure UTM parameter mapping and source codes.""",

    "Source sync not configured. Go to integrations/smart_apply_config Source Mapping and configure source field mapping.": """**Purpose:** Validates that source tracking data is mapped to sync with applications to the ATS.

**Impact:** Without source sync, source attribution data is lost when applications sync to the ATS.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config → Source Mapping. Map source field to ATS source field.""",

    "Source tracking not enabled. Go to integrations/pcsx_base_config Source Tracking and set enabled: true.": """**Purpose:** Validates that source tracking is enabled for capturing where candidates come from (job boards, campaigns, referrals).

**Impact:** Without source tracking, recruitment marketing effectiveness cannot be measured.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Source Tracking. Set enabled: true.""",

    "SSL certificate issue detected. Go to integrations/domain_whitelabeling_config and verify SSL certificate.": """**Purpose:** Validates that SSL certificate is valid, not expired, and properly configured for secure HTTPS access.

**Impact:** SSL issues cause security warnings or block access to the career site entirely.

**To Fix:** Navigate to Admin Console → Talent Experience → Domain Config. Check certificate expiration. Upload new certificate if needed.""",

    "ta_email_template_variables_cj": """**Purpose:** Validates that email templates use consistent and valid variable placeholders for candidate and job information.

**Impact:** Invalid variables cause email personalization to fail, showing placeholder text to candidates.

**To Fix:** Review email templates and ensure all variables match the supported variable list. Use {candidate_name}, {position_title}, {company_name}, etc.""",

    "Talent communities not enabled. Go to integrations/community_home_config and set enabled: true.": """**Purpose:** Validates that talent communities feature is enabled for managing talent pools and prospect engagement.

**Impact:** Without enablement, talent community features for nurturing prospects are unavailable.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Community Home Config. Set enabled: true.""",

    "Talent network join not enabled. Go to integrations/smart_apply_config and enable talent network join option.": """**Purpose:** Validates that Talent Network join is enabled, allowing candidates to join the talent pool without applying to a specific position.

**Impact:** Without enablement, talent pool growth is limited to only active applicants.

**To Fix:** Navigate to Admin Console → Talent Experience → Smart Apply Config. Enable talent network join option (enableTalentNetwork: true).""",

    "Template permissions should be correctly configured.": """**Purpose:** Validates that job requisition template permissions are properly configured, controlling who can use which templates.

**Impact:** Incorrect permissions may prevent users from creating requisitions or allow unauthorized template access.

**To Fix:** Review template permissions. Ensure appropriate users/roles have access to relevant templates.""",

    "Tracking scripts invalid. Go to integrations/tracking_pixel_config and verify JavaScript syntax.": """**Purpose:** Validates that tracking scripts (Google Analytics, pixel tags) have valid JavaScript syntax and are assigned to correct events.

**Impact:** Invalid scripts cause tracking failures, creating gaps in analytics data.

**To Fix:** Navigate to Admin Console → Talent Experience → Tracking Pixel Config. Validate JavaScript syntax. Test tracking in browser developer tools.""",

    "WhatsApp integration not configured. Go to integrations/email_config and verify WhatsApp Business API configuration.": """**Purpose:** Validates that WhatsApp Business API integration is configured for candidate messaging via WhatsApp.

**Impact:** Without WhatsApp configuration, recruiters cannot communicate with candidates via WhatsApp, which is preferred in many regions.

**To Fix:** Navigate to Admin Console → Provisioning → Email & SMS Config. Configure WhatsApp Twilio account SID, auth token, and messaging service ID.""",

    "Withdraw functionality not enabled. Go to integrations/pcsx_base_config Applications and enable withdraw application option.": """**Purpose:** Validates that application withdrawal is enabled, allowing candidates to withdraw their applications.

**Impact:** Without withdrawal capability, candidates cannot remove applications, which may be required for compliance.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Applications. Enable withdraw option.""",

    "Withdraw workflow not configured. Go to integrations/pcsx_base_config Applications Withdraw and configure workflow.": """**Purpose:** Validates that the withdrawal workflow includes confirmation dialog, ATS sync, and candidate notification.

**Impact:** Incomplete workflow may cause withdrawals to not sync to ATS or candidates to not receive confirmation.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Applications → Withdraw. Configure confirmation and ATS sync.""",

    "Workflow automation not enabled. Go to integrations/workflow_automation_config and set enabled: true.": """**Purpose:** Validates that workflow automation feature is enabled for creating automated candidate workflows.

**Impact:** Without enablement, automated workflows cannot be created or executed.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Workflow Automation Config. Set enabled: true.""",

    "Workflow triggers not configured. Go to workflows and configure triggers with valid events.": """**Purpose:** Validates that at least one workflow trigger is configured with valid events and conditions for automation.

**Impact:** Without triggers, automated workflows cannot execute as there's no defined trigger condition.

**To Fix:** Navigate to Admin Console → Workflows. Configure at least one trigger with event type (stage change, application, etc.) and conditions.""",

    "position_hiring_band_data_quality": """**Purpose:** Measures the percentage of positions with hiring band data defined. Hiring bands determine job level for eligibility filtering.

**Impact:** Positions without hiring bands cannot be properly filtered for internal mobility eligibility.

**To Fix:** Ensure positions have hiring_band field populated via ATS integration or manual assignment.""",

    "role_levels_in_internal_mobility_config_quality": """**Purpose:** Validates that role levels defined in Talent Design are also configured in Internal Mobility for proper eligibility calculations.

**Impact:** Missing level configurations cause eligibility rules to fail for certain levels.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Ensure all levels from Talent Design are configured in job bands.""",

    "employee_levels_in_internal_mobility_config_quality": """**Purpose:** Validates that employee levels are properly configured in Internal Mobility settings, enabling correct band-based job eligibility.

**Impact:** Without proper level configuration, employees may not see appropriate job opportunities.

**To Fix:** Navigate to Admin Console → Talent Management → Internal Mobility. Verify all employee levels are mapped in the configuration.""",

    "community_home": """**Purpose:** Validates that Community Home configuration is complete with available_filters, filter_to_fq_data_map, and columns for the dashboard.

**Impact:** Missing configuration causes the Community Home page to be non-functional or display incorrectly.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Communities. Configure available_filters, filter_to_fq_data_map, and columns.""",

    "community_workflows": """**Purpose:** Validates that community_workflow_config is defined per community type with valid display_name and workflow steps.

**Impact:** Without workflow configuration, communities cannot progress prospects through engagement stages.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Community Workflow Config. Define workflows with stages for each community type.""",

    "leads_workflow": """**Purpose:** Validates that the Leads Workflow tab is configured on the pipeline page, providing access to sourced/matched candidates.

**Impact:** Missing Leads tab prevents recruiters from accessing the candidate sourcing workflow.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Pipeline & Workflows. Enable leads tab in workflow_config.""",

    "applicants_workflow": """**Purpose:** Validates that the Applicants Workflow tab is configured on the pipeline page for viewing applied candidates.

**Impact:** Missing Applicants tab prevents recruiters from viewing and managing job applicants.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Pipeline & Workflows. Enable applicants tab in workflow_config.""",

    "all_job_req_templates_in_stage_transition_map": """**Purpose:** Validates that all job requisition template IDs are included in the stage transition map, ensuring stage advances work across all position types.

**Impact:** Missing templates cause stage advance failures, preventing candidates from progressing in the pipeline.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Workflows. Ensure all job_req_template_ids are in template_to_stage_transition_map.""",

    "application_stage_advances_per_job_req_template_rule": """**Purpose:** Measures the success rate of stage advances per job requisition template. Target: 90%+ success rate.

**Impact:** Low success rate indicates stage transition map issues causing ATS sync failures.

**To Fix:** Review stage transition map for failing templates. Verify stage mapping to ATS. Check ATS API connectivity.""",

    "recruiter_missing_communication_email": """**Purpose:** Identifies users with send_messages permission who don't have a communication email configured.

**Impact:** Users without communication email cannot send messages to candidates, blocking engagement.

**To Fix:** Navigate to Admin Console → Provisioning → Manage Users. Add communication_email for all users with PERM_SEND_MESSAGES.""",

    "communication_channels": """**Purpose:** Validates that communication channels (SMS, WhatsApp) are configured for interview scheduling notifications.

**Impact:** Missing channels limit notification options if candidates prefer non-email communication.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Enable SMS and WhatsApp channels as needed.""",

    "extension_communities_disabled_text": """**Purpose:** Validates that a clear message is configured when Communities feature is disabled in the Chrome Extension.

**Impact:** Without clear messaging, extension users may be confused about feature unavailability.

**To Fix:** Configure descriptive disabled text explaining why Communities is unavailable and how to enable.""",

    "extension_reminder_action": """**Purpose:** Validates that reminder functionality is configured in the Chrome Extension for team-wide candidate reminder visibility.

**Impact:** Without reminders, team members may duplicate outreach efforts or miss follow-ups.

**To Fix:** Configure reminder_action in extension configuration to enable team-wide reminder visibility.""",

    "app_configs": """**Purpose:** Validates that hostname configurations are set for LinkedIn, Naukri, and GitHub in the Chrome Extension.

**Impact:** Missing hostname configuration prevents profile parsing from these job sites.

**To Fix:** Configure app_configs with correct hostnames for each supported site in extension settings.""",

    "extension_actions": """**Purpose:** Validates that all extension actions (save candidate, mark status, set reminder) are properly configured.

**Impact:** Missing or misconfigured actions prevent recruiters from managing candidates through the extension.

**To Fix:** Configure all actions and sub-actions in extension configuration for complete candidate management.""",

    "feedback_report": """**Purpose:** Validates that feedback report columns are configured for consolidated interview feedback viewing.

**Impact:** Misconfigured reports affect how recruiters and hiring managers review interview feedback.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback. Configure report columns and formatting.""",

    "dashboard_columns_list": """**Purpose:** Validates that feedback dashboard columns are configured for the Interview Feedback Center.

**Impact:** Missing columns reduce dashboard usefulness for managing feedback across interviews.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Interview Feedback. Configure dashboard_columns_list.""",

    "scheduling_config": """**Purpose:** Validates that smart scheduling is enabled with calendar integration for interview scheduling.

**Impact:** Without configuration, interview scheduling features cannot be used.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Set enabled: true and configure calendar provider.""",

    "scheduling_timezone": """**Purpose:** Validates that a default timezone is configured for interview scheduling to prevent time confusion.

**Impact:** Missing timezone can cause scheduling errors and incorrect time display.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Set default timezone.""",

    "standard_schedule_action": """**Purpose:** Validates that the scheduling action button is enabled on pipeline and profile pages.

**Impact:** Without the action, recruiters cannot initiate interview scheduling from the candidate context.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Enable schedule action in pipeline configuration.""",

    "enabled_for_scheduling": """**Purpose:** Validates that a calendar provider is configured for interview scheduling integration.

**Impact:** Without calendar provider, interviews cannot be synchronized with calendars.

**To Fix:** Navigate to Admin Console → Talent Acquisition → Scheduling. Configure calendarProvider (Google Calendar, Microsoft 365).""",

    # New rules - matched by Rule Name when Rule ID is empty
    "position_sync_lag_rule": """**Purpose:** Monitors the median time lag between when positions are updated in the ATS and when they are synced to Eightfold. Target threshold: 60 minutes for most ATSs.

**Impact:** High sync lag means position updates (new jobs, closures, title changes) appear delayed in Eightfold, causing candidates to apply to outdated listings and recruiters to work with stale data.

**To Fix:** Check ATS API connectivity and rate limits. Review sync schedules in Admin Console → Provisioning → Sync Settings. Investigate ATS webhook configuration if applicable. Check ats_sync_log for error patterns.""",

    "application_submissions_per_job_req_template_week_rule": """**Purpose:** Measures successful application submissions per job requisition template over the past 7 days. Ensures each configured template has at least the minimum threshold of successful submissions.

**Impact:** Templates with zero or low submissions indicate either configuration issues (questionnaire mapping, field validation) or traffic problems. This affects recruiting pipeline health.

**To Fix:** Review questionnaire configuration for failing templates. Check field mapping in Smart Apply. Verify template is associated with open positions. Review ats_write_log for submission errors.""",

    "pcs_and_ta_match_score_consistency": """**Purpose:** Validates that match score thresholds and algorithms are consistent between the career site (PCS) and Talent Acquisition modules.

**Impact:** Inconsistent scoring causes candidates to see different match levels on the career site vs. what recruiters see, eroding trust in AI recommendations.

**To Fix:** Ensure strong_match_threshold values are aligned between PCS and TA configurations. Verify algorithm versions match.""",

    "microsite_profile_and_application_isolation": """**Purpose:** Validates that candidate profiles and applications are properly isolated between the parent career site and microsites when isolation is required.

**Impact:** Without proper isolation, candidate data may leak between sites, or candidates may need to re-register when moving between parent site and microsites.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config → Microsites. Configure profile_isolation and application_isolation settings per microsite requirements.""",

    "pcs_mobil_config_cj": """**Purpose:** Validates that mobile-specific configurations are defined for the career site using device_configuration settings.

**Impact:** Without mobile configuration, the career site may not display correctly on phones and tablets, affecting candidate experience.

**To Fix:** Navigate to Admin Console → Talent Experience → PCS Config. Configure device_configuration settings for mobile responsiveness and mobile-specific layouts.""",
}


def enhance_descriptions(input_file, output_file):
    """Read TSV file and enhance descriptions based on the mapping."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        rows = list(reader)
    
    if not rows:
        print("Error: Empty file")
        return
    
    # Find column indices
    header = rows[0]
    rule_id_idx = None
    rule_name_idx = None
    cursor_desc_idx = None
    
    for i, col in enumerate(header):
        if col.strip().lower() == 'rule id':
            rule_id_idx = i
        elif col.strip().lower() == 'rule name':
            rule_name_idx = i
        elif 'cursor generated description' in col.strip().lower():
            cursor_desc_idx = i
    
    if rule_id_idx is None:
        print("Error: Could not find 'Rule ID' column")
        return
    
    if cursor_desc_idx is None:
        print("Error: Could not find 'Cursor Generated Description' column")
        return
    
    print(f"Found Rule ID at column {rule_id_idx}, Rule Name at column {rule_name_idx}, Cursor Generated Description at column {cursor_desc_idx}")
    
    # Process each row
    enhanced_count = 0
    not_enhanced = []
    for i, row in enumerate(rows[1:], start=1):
        if len(row) <= max(rule_id_idx, cursor_desc_idx):
            continue
        
        rule_id = row[rule_id_idx].strip()
        rule_name = row[rule_name_idx].strip() if rule_name_idx is not None and len(row) > rule_name_idx else ""
        
        # Try Rule ID first, then Rule Name if Rule ID is empty
        lookup_key = rule_id if rule_id else rule_name
        
        if lookup_key in ENHANCED_DESCRIPTIONS:
            # Replace newlines with <br> for TSV compatibility
            enhanced = ENHANCED_DESCRIPTIONS[lookup_key].replace('\n\n', '<br><br>').replace('\n', ' ')
            row[cursor_desc_idx] = enhanced
            enhanced_count += 1
        else:
            not_enhanced.append(f"Row {i+1}: {lookup_key[:50]}...")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(rows)
    
    print(f"Enhanced {enhanced_count} rule descriptions")
    print(f"Output written to {output_file}")
    
    if not_enhanced:
        print(f"\nRules NOT enhanced ({len(not_enhanced)}):")
        for r in not_enhanced:
            print(f"  - {r}")


if __name__ == "__main__":
    input_file = "/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv"
    output_file = "/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_enhanced_v2.tsv"
    
    enhance_descriptions(input_file, output_file)
