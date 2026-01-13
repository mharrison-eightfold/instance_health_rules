#!/usr/bin/env python3
"""
Enhance rule descriptions using technical reference knowledge.
This script generates human-readable, actionable descriptions for Solution Architects
and Functional Consultants.
"""

import pandas as pd
import re

# Path to files
INPUT_FILE = '/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv'
OUTPUT_FILE = '/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv'

# Enhanced descriptions based on codebase analysis
# Format: 'rule_id': {'purpose': '...', 'impact': '...', 'resolution': '...'}
ENHANCED_DESCRIPTIONS = {
    # ==========================================
    # TALENT MANAGEMENT - CORE
    # ==========================================
    'employee_level_quality': {
        'purpose': 'Validates that at least 95% of employee profiles have a job level/band populated. The level field is ingested from your HRIS and stored in employee.level. The system queries the Solr employee index using: profile.data_json.employee.level:[* TO *]',
        'impact': 'Missing employee levels will break Career Navigator (cannot determine appropriate target roles), Internal Mobility (cannot filter jobs by band eligibility), and Succession Planning (cannot identify bench strength by level). Job recommendations will be inaccurate.',
        'resolution': 'Navigate to Admin Console → Data Management → Employee Sync. Verify the level/grade field from your source system is mapped to employee.level. Run a full employee sync. Validate by checking sample profiles.'
    },
    'employee_location_quality': {
        'purpose': 'Validates that at least 95% of employee profiles have a valid location value (not null, empty, or placeholder values like "Unknown", "N/A"). Uses an analytics/Redshift query to count employees with location data.',
        'impact': 'Missing location data will prevent geo-based job recommendations, break location filters in search, affect workforce analytics by geography, and limit personalization of remote/hybrid job suggestions.',
        'resolution': 'Check employee sync mapping for location field. Review source HRIS data for null/empty locations. Replace placeholder values with actual locations. Re-run employee sync after corrections.'
    },
    'employee_business_unit_quality': {
        'purpose': 'Validates that at least 95% of employees have a Business Unit (BU) defined. Business Unit is used for organizational grouping, access permissions, and analytics segmentation.',
        'impact': 'Missing BU values can lead to misaligned access permissions (employees seeing data from wrong BUs), broken analytics dashboards, and ineffective organizational filtering in Talent Hub views.',
        'resolution': 'Verify business_unit field mapping in employee sync configuration. Ensure BU values exist in source HRIS. Standardize BU naming if values are inconsistent.'
    },
    'employee_division_quality': {
        'purpose': 'Validates that at least 95% of employees have a Division (Line of Business/LOB) defined. Division is used to infer business function and auto-initialize role business functions in career workflows.',
        'impact': 'Missing Division/LOB values may result in inaccurate role mapping, broken career pathing logic, incorrect recommendations, and gaps in workforce planning by function.',
        'resolution': 'Check division/department field mapping in employee sync. Ensure LOB values are populated in source system. Consider deriving from department if division not available.'
    },
    'employee_job_code_quality': {
        'purpose': 'Validates that at least 95% of employees have a job code defined. Job codes uniquely identify roles and are critical for linking employees to roles in Talent Design, succession planning, and internal mobility.',
        'impact': 'Missing job codes prevent accurate employee-role mapping, break succession planning bench strength calculations, and affect Career Navigator role initialization.',
        'resolution': 'Map job_code field from HRIS in employee sync configuration. Verify job codes match those defined in Role Library/Talent Design. Run sync after mapping.'
    },
    'employee_level_quality_base_tm': {
        'purpose': 'Validates that most employees have a level defined in their profiles. Levels are used to infer employee seniority and help auto-initialize roles with appropriate seniority for planning and mobility workflows.',
        'impact': 'Missing level data breaks seniority inference, which affects matching accuracy, recommendations quality, and role creation logic in Career Navigator.',
        'resolution': 'Verify level field mapping in employee sync. Common source fields: grade, job_level, band. Run full sync after mapping.'
    },
    'employee_hiring_date_quality': {
        'purpose': 'Validates that at least 95% of employees have a hiring date (start date) defined. Hiring date is used for tenure calculations, workforce analytics, retention tracking, and seniority-based features.',
        'impact': 'Missing hiring dates prevent accurate tenure analytics, affect retention tracking reports, and may break tenure-based eligibility rules for internal mobility.',
        'resolution': 'Map hiring_date or start_date field from HRIS. Accept various date formats (ISO, MM/DD/YYYY). Ensure dates are not in the future.'
    },
    'employee_current_title_seniority_quality': {
        'purpose': 'Validates that most employees have a seniority level derived from their current title. The system uses title parsing and inference to determine seniority when explicit level is not provided.',
        'impact': 'Missing seniority levels lead to inaccurate matching, ineffective internal mobility recommendations, and broken career pathing logic.',
        'resolution': 'Ensure employee titles are populated and descriptive. If seniority cannot be inferred from titles, explicitly map the level field from HRIS.'
    },
    'employee_manager_email_quality': {
        'purpose': 'Validates that at least 95% of employees have their manager\'s email address populated. Manager email is required to build org chart hierarchies and enable manager-based permissions.',
        'impact': 'Missing manager emails break org chart generation, prevent manager-based workflows, disable skill assessments requiring manager input, and affect team view functionality.',
        'resolution': 'Map manager_email field in employee sync. Ensure managers exist as employees in the system. Handle top-level employees (CEO) with null manager gracefully.'
    },
    'employee_manager_id_quality': {
        'purpose': 'Validates that at least 95% of employees have a manager_userid that links to their manager\'s employee record. This creates the reporting structure hierarchy.',
        'impact': 'Missing manager IDs break org chart construction, prevent My Team functionality, and disable manager-based access controls.',
        'resolution': 'Map manager_userid or manager_id from HRIS. Ensure the ID references an existing employee record. Validate referential integrity.'
    },
    'valid_manager_email': {
        'purpose': 'Validates that manager emails assigned to employees match the email of an existing employee profile in the system. This is a presence and reference check, not an email format validation.',
        'impact': 'Invalid manager emails (pointing to non-existent employees) break org chart links, prevent manager-based permissions from working, and cause team view failures.',
        'resolution': 'Export employees with invalid manager emails. Cross-reference manager emails against employee email list. Fix mismatches in source HRIS or add missing manager profiles.'
    },
    'employee_thin_profile_quality': {
        'purpose': 'Validates that at least 95% of employees have enriched (non-thin) profiles with sufficient data. A thin profile lacks key fields like skills, experience, and education.',
        'impact': 'High percentage of thin profiles significantly reduces matching accuracy, recommendation quality, and analytics usefulness across all Talent Management features.',
        'resolution': 'Identify thin profiles via analytics. Enrich via employee sync with additional fields. Enable self-service profile completion. Consider AI-based enrichment.'
    },
    'profile_skills_quality': {
        'purpose': 'Validates that at least 75% of CANDIDATE profiles (note: uses CandidateDataSolrBaseRule) have at least one skill added. Skills are essential for matching and recommendations.',
        'impact': 'Low skill coverage reduces recommendation effectiveness, breaks skill-based job matching, and limits insights across TA modules.',
        'resolution': 'Enable resume parsing for skill extraction. Encourage candidates to add skills during application. Use AI skill inference from experience.'
    },
    
    # Employee Levels in IJP Config
    'employee_levels_in_internal_mobility_config_quality': {
        'purpose': 'Validates that employee level values (from profile.data_json.employee.level) match the job_bands defined in ijp_config. The system queries: employee levels IN [configured job_bands list].',
        'impact': 'Employees with levels not in job_bands cannot be properly evaluated for internal mobility eligibility, will not receive appropriate job recommendations, and may be excluded from succession planning.',
        'resolution': 'Navigate to Admin Console → Talent Management → Internal Mobility. Compare configured job_bands with distinct employee levels (run analytics query). Add missing levels to job_bands or standardize employee levels.'
    },
    'role_levels_in_internal_mobility_config_quality': {
        'purpose': 'Validates that role levels (efcustom_text_job_level) match the job_bands defined in ijp_config. Roles must align with the same band hierarchy as employees.',
        'impact': 'Roles with levels not in job_bands cannot be used for eligibility calculations, break career pathing, and cause succession planning gaps.',
        'resolution': 'Export roles with non-matching levels. Either add levels to ijp_config job_bands or update role levels to match existing bands.'
    },
    
    # Job Bands / Internal Mobility
    'employee_hiring_bands': {
        'purpose': 'Validates that job_bands array is configured in ijp_config. Job bands define the hierarchical levels (e.g., L1-L8, Associate to VP) used throughout Talent Management for eligibility and filtering.',
        'impact': 'Without job_bands configuration, internal mobility filtering will not work, Career Navigator cannot determine appropriate role targets, and band-based recommendations are disabled.',
        'resolution': 'Navigate to Admin Console → Talent Management → Internal Mobility. Add job_bands array with all organizational levels in seniority order: ["Entry", "Associate", "Senior", "Lead", "Manager", "Director", "VP", "Executive"]'
    },
    'job_bands': {
        'purpose': 'Validates that job_bands array is configured in ijp_config. This is the same check as employee_hiring_bands - ensuring the band hierarchy is defined.',
        'impact': 'Job bands are the foundation for internal mobility. Without them, band-based eligibility, job filtering, and career pathing cannot function.',
        'resolution': 'Configure job_bands in Internal Mobility settings. List all levels from entry to executive in order. Match values to what appears in employee.level field.'
    },
    'hiring_band_equivalence': {
        'purpose': 'Validates that hiring_band_equivalence is configured in ijp_config. This groups related job bands that should be treated as equivalent for mobility (e.g., L3 and L4 might both be "mid-level").',
        'impact': 'Without band equivalences, eligibility is too strict (only exact band matches). Employees cannot see or apply to jobs in equivalent bands.',
        'resolution': 'Configure hiring_band_equivalence in Internal Mobility: {"entry": ["L1", "L2"], "mid": ["L3", "L4"], "senior": ["L5", "L6"], "leadership": ["L7", "L8"]}. Ensure bands are listed in seniority order within each group.'
    },
    'filter_by_hiring_band': {
        'purpose': 'Validates that filter_by_hiring_band is enabled in ijp_config. When true, employees only see jobs within their eligible band range based on current level and configured eligibility rules.',
        'impact': 'If disabled (default is 0), employees see all jobs regardless of level, leading to irrelevant recommendations and poor Career Hub experience.',
        'resolution': 'Navigate to Admin Console → Talent Management → Internal Mobility. Set filter_by_hiring_band: true. Prerequisite: job_bands and hiring_band_equivalence must be configured first.'
    },
    
    # Upskilling/Courses
    'upskilling_display_config': {
        'purpose': 'Validates that the Upskilling tab is configured in the employee profile page layout (career_hub_base_config → product_configs.employee.profile_page.tabs.upskilling).',
        'impact': 'Without this tab, employees cannot view their upskilling plans, track skill development progress, or see recommended courses for gap closure from their profile.',
        'resolution': 'Navigate to Admin Console → Talent Management → Career Hub Configuration → Profile Page. Add upskilling to the tabs configuration with enabled: true and appropriate display order.'
    },
    'upskilling_top_nav': {
        'purpose': 'Validates that the Upskilling link is present in the Career Hub top navigation bar, providing quick access to upskilling features.',
        'impact': 'Missing navigation link reduces discoverability of upskilling features and decreases employee engagement with skill development programs.',
        'resolution': 'Navigate to Career Hub Configuration → Navigation. Add upskilling to the top navigation menu with enabled: true.'
    },
    'my_courses': {
        'purpose': 'Validates that "My Courses" section is configured in Career Hub navigation, providing employees access to assigned, in-progress, and completed courses.',
        'impact': 'Without My Courses, employees cannot easily track their learning progress or find assigned courses, reducing participation in development initiatives.',
        'resolution': 'Enable my_courses in Career Hub navigation configuration. Prerequisite: Courses feature must be enabled for the tenant.'
    },
    'explore_course': {
        'purpose': 'Validates that the course exploration/browse feature is enabled (career_hub_explore_config), allowing employees to search and filter available courses.',
        'impact': 'Without explore functionality, employees cannot discover new courses, limiting organic learning and skill development.',
        'resolution': 'Enable course in the explore configuration. Configure appropriate filters (topic, skill, duration, format) for course discovery.'
    },
    'global_search_course': {
        'purpose': 'Validates that courses are included in Global Search results, allowing employees to find courses when searching across all entities.',
        'impact': 'Excluding courses from global search makes them harder to discover, reducing engagement with learning content.',
        'resolution': 'Add "course" to the global search entity types in Career Hub search configuration.'
    },
    'course_skills_count_rule': {
        'purpose': 'Validates that at least 75% of courses have skills tagged. Skill tags enable accurate course recommendations for upskilling plans, Career Navigator, and skill gap closure.',
        'impact': 'Courses without skills cannot be recommended accurately in upskilling workflows, career pathing, or skill-based learning paths.',
        'resolution': 'Enrich courses with skill tags via LMS integration, manual entry, or AI-based extraction from course descriptions. Run course sync with skills mapping enabled.'
    },
    'courses_with_title_rule': {
        'purpose': 'Validates that most courses have titles defined. Titles are essential for identification, discoverability, and skill inference.',
        'impact': 'Courses without titles cannot be identified by users, appear blank in recommendations, and cannot have skills inferred.',
        'resolution': 'Verify course title field mapping in LMS integration. Fix or remove courses without titles in source LMS.'
    },
    'courses_with_description_rule': {
        'purpose': 'Validates that at least 75% of courses have descriptions of 50+ words. Descriptions enable skill inference and help employees evaluate course relevance.',
        'impact': 'Short or missing descriptions reduce learner engagement, prevent accurate skill tagging, and limit AI-based course-to-skill mapping.',
        'resolution': 'Work with L&D team to add meaningful descriptions. Sync descriptions from LMS. Consider using AI to generate descriptions from course content.'
    },
    'courses_with_skills_rule': {
        'purpose': 'Validates that most courses have at least one skill tagged, enabling skill-based filtering and recommendations.',
        'impact': 'Courses without skills cannot be recommended for skill development, limiting upskilling plan effectiveness.',
        'resolution': 'Enable skill extraction in course sync. Manually tag high-priority courses. Use title/description-based skill inference.'
    },
    
    # Recommended Feeds
    'recommended_jobs_filter_list': {
        'purpose': 'Validates that the recommended_jobs feed is configured in career_hub_base_config → feeds, showing personalized job recommendations on the Career Hub home page.',
        'impact': 'Missing job recommendations reduce employee engagement with internal mobility and limit discovery of open positions matching their skills.',
        'resolution': 'Add recommended_jobs to order_of_feeds in home_config. Configure the feed with filter_by_star_threshold (recommend ≥3.25) and appropriate filters (e.g., is_internally_posted:1).'
    },
    'similar_people_filter_list': {
        'purpose': 'Validates that similar_people recommendation feed is configured, showing employees with similar profiles for networking and peer discovery.',
        'impact': 'Missing similar people recommendations limit networking opportunities and peer-based career exploration.',
        'resolution': 'Add similar_people to order_of_feeds. Configure appropriate matching criteria and display count.'
    },
    
    # Projects
    'explore_project': {
        'purpose': 'Validates that project marketplace exploration is configured, allowing employees to browse and discover project opportunities.',
        'impact': 'Without explore, employees cannot find projects matching their interests and skills, limiting gig/project-based development.',
        'resolution': 'Enable project in explore configuration. Set up filters for project discovery (skills required, duration, location).'
    },
    'global_search_project': {
        'purpose': 'Validates that projects are included in Global Search, making them discoverable alongside jobs, people, and courses.',
        'impact': 'Projects excluded from search are harder to find, reducing participation in the project marketplace.',
        'resolution': 'Add "project" to global search entity types.'
    },
    'project_order_of_feeds': {
        'purpose': 'Validates that recommended_projects feed is configured in order_of_feeds, showing project recommendations on Career Hub home.',
        'impact': 'Missing project recommendations limit awareness of gig opportunities aligned with employee skills and interests.',
        'resolution': 'Add recommended_projects to home page order_of_feeds configuration.'
    },
    'projects_with_skills_rule': {
        'purpose': 'Validates that most projects have skills tagged, enabling skill-based matching between employees and project opportunities.',
        'impact': 'Projects without skills cannot be accurately matched to employees, reducing recommendation quality.',
        'resolution': 'Require skills when creating projects. Infer skills from project descriptions. Add skills to existing projects.'
    },
    'projects_with_title_rule': {
        'purpose': 'Validates that most projects have titles defined for identification and discoverability.',
        'impact': 'Projects without titles appear blank and cannot be effectively browsed or recommended.',
        'resolution': 'Require title field when creating projects. Fix or archive titleless projects.'
    },
    'projects_with_description_rule': {
        'purpose': 'Validates that most projects have descriptions, providing context for employee decision-making.',
        'impact': 'Projects without descriptions provide insufficient information for employees to evaluate fit.',
        'resolution': 'Require description when posting projects. Add descriptions to existing projects.'
    },
    
    # Roles
    'role_job_code_quality': {
        'purpose': 'Validates that most roles have a job_code defined, uniquely identifying roles for employee-role mapping and succession planning.',
        'impact': 'Missing role job codes break employee-role linkages, affect succession planning, and reduce matching accuracy.',
        'resolution': 'Define job_code for each role in Talent Design. Ensure codes match those in employee data. Use consistent naming convention.'
    },
    'role_title_quality': {
        'purpose': 'Validates that most roles have titles defined. Role titles drive recommendations and matching in Career Navigator.',
        'impact': 'Roles without titles cannot be recommended, searched, or displayed properly in career pathing.',
        'resolution': 'Ensure all roles in Talent Design have descriptive titles. Sync role titles from HRIS job catalog if available.'
    },
    'role_level_quality': {
        'purpose': 'Validates that most roles have an associated level/band defined, enabling seniority-based matching and career path visualization.',
        'impact': 'Missing role levels break seniority inference, reduce matching accuracy, and affect career planning workflows.',
        'resolution': 'Assign level to each role in Talent Design. Use same level values as in job_bands configuration.'
    },
    'role_lob_quality': {
        'purpose': 'Validates that most roles have a business function/LOB defined, enabling domain-based matching and recommendations.',
        'impact': 'Missing business function reduces recommendation quality and breaks domain-specific career pathing.',
        'resolution': 'Assign business function to each role. Derive from department or job family if not explicitly available.'
    },
    'role_skills_quality': {
        'purpose': 'Validates that most roles have at least 3 skills defined, ensuring role requirements are captured for succession planning and recommendations.',
        'impact': 'Roles with fewer than 3 skills have reduced benchmarking quality and less accurate matching in succession planning.',
        'resolution': 'Enrich roles with required skills in Talent Design. Use AI skill inference from role titles/descriptions. Target 5-10 skills per role.'
    },
    'employee_role_quality': {
        'purpose': 'Validates that employees are assigned to roles in Talent Design, linking them to role requirements for succession and development.',
        'impact': 'Without role assignments, the system cannot determine required skills for employees, reducing accuracy of development and succession planning.',
        'resolution': 'Link employees to roles via job_code matching or manual assignment in Talent Design.'
    },
    
    # ==========================================
    # TALENT MANAGEMENT - LEADER EXPERIENCE
    # ==========================================
    'talent_hub_config': {
        'purpose': 'Validates that Talent Hub configuration exists for HRBPs, enabling access to team planning, succession management, and workforce insights views.',
        'impact': 'Without Talent Hub config, HRBPs cannot access their consolidated talent management view for their assigned populations.',
        'resolution': 'Navigate to Admin Console → Talent Management → HRBP Configuration. Enable Talent Hub with enabled: true. Configure visible tabs and default views.'
    },
    'talent_hub_tab_order': {
        'purpose': 'Validates that Talent Hub tab order is configured, ensuring consistent and logical tab arrangement for HRBP users.',
        'impact': 'Incorrect tab order creates confusing navigation experience for HRBPs.',
        'resolution': 'Configure tab order in HRBP Talent Hub settings. Recommended order: Team Planning, Succession, Insights.'
    },
    'talent_hub_filter_order': {
        'purpose': 'Validates that filter order is configured in Talent Hub, ensuring logical filter arrangement for team planning workflows.',
        'impact': 'Poor filter ordering reduces usability and efficiency for HRBPs managing large populations.',
        'resolution': 'Configure filter order based on most commonly used filters first (e.g., Business Unit, Location, Level).'
    },
    'talent_hub_search_filters': {
        'purpose': 'Validates that search filters are configured in Talent Hub for HRBP population filtering.',
        'impact': 'Missing filters prevent HRBPs from effectively segmenting and analyzing their talent populations.',
        'resolution': 'Add relevant filters: business_unit, location, level, department, manager, performance rating.'
    },
    'team_table_order': {
        'purpose': 'Validates that team planning table columns are displayed in correct order within Talent Hub.',
        'impact': 'Incorrect column order creates confusion and reduces efficiency for HRBPs reviewing team data.',
        'resolution': 'Configure column order in team table settings. Recommended: Name, Title, Level, Performance, Potential, Risk.'
    },
    'team_table_column_config': {
        'purpose': 'Validates that team table column configuration aligns with the defined column order.',
        'impact': 'Misaligned configurations may display incorrect columns or cause rendering issues.',
        'resolution': 'Ensure column configuration matches the columns defined in team_table_order.'
    },
    'profile_search_data_fields': {
        'purpose': 'Validates that profile search data fields are configured for HRBP Talent Hub, enabling effective profile search within team views.',
        'impact': 'Incorrect configuration leads to incomplete or inaccurate search results.',
        'resolution': 'Align profile_search_data_fields with team_table_column_config to ensure consistent search behavior.'
    },
    
    # Succession Planning
    'position_only_plan': {
        'purpose': 'Validates that position-only succession plan configuration is enabled when JIE (Jobs Intelligence Engine) is disabled.',
        'impact': 'Without this configuration, succession planning may not function correctly for position-based planning.',
        'resolution': 'Enable position_only_plan in succession planning configuration if using position-based (not role-based) succession.'
    },
    'hrbp_users_rule': {
        'purpose': 'Validates that users with HRBP (Human Resources Business Partner) permissions have been created to access HRBP-specific features.',
        'impact': 'Without HRBP users, no one can access HRBP features like Talent Hub, limiting HR\'s ability to manage talent.',
        'resolution': 'Create users with HRBP role in User Management. Assign to appropriate business units. Grant necessary permissions.'
    },
    
    # Skill Assessments
    'skill_proficiences': {
        'purpose': 'Validates that skill proficiency tracking is configured for Skill Assessments. Proficiencies allow tracking employee competency levels (Beginner, Intermediate, Advanced, Expert).',
        'impact': 'Without proficiency configuration, skill assessments cannot track competency levels, reducing upskilling effectiveness.',
        'resolution': 'Enable skill proficiencies in Career Hub Configuration → Assessments. Configure proficiency levels and rating scale.'
    },
    'profile_page_skill_assessments': {
        'purpose': 'Validates that Skill Assessments are configured on the employee profile page, enabling direct access for employees to complete assessments.',
        'impact': 'Without profile page integration, employees cannot easily access or complete skill assessments, reducing participation.',
        'resolution': 'Add skill_assessments to profile page sections in Career Hub Configuration.'
    },
    'skill_assessment_default_access': {
        'purpose': 'Validates that access checks for Skill Assessments are enabled, allowing controlled access based on user role (self, manager, peer).',
        'impact': 'Without access checks, assessments may not respect access rules, leading to inconsistent user experience.',
        'resolution': 'Enable default_access for skill_assessment in Career Hub access configuration.'
    },
    'employee_engagement_enabled': {
        'purpose': 'Validates that employee_engagement_enabled is true in career_hub_profile_config, enabling engagement tracking for skill proficiencies, endorsements, and assessments.',
        'impact': 'Without engagement enabled, participation tracking and related workflows will not function.',
        'resolution': 'Set employee_engagement_enabled: true in Career Hub Profile Configuration. Enable specific engagement types as needed.'
    },
    
    # ==========================================
    # TALENT ACQUISITION - CORE
    # ==========================================
    'recruiter_missing_communication_email': {
        'purpose': 'Identifies users with PERM_SEND_MESSAGES permission who lack a properly configured communication email. The system checks all roles with send permission, finds users in those roles, and validates each has an authorized communication email.',
        'impact': 'Affected recruiters cannot send messages to candidates. Outreach campaigns, scheduling communications, and candidate engagement will fail for these users.',
        'resolution': 'Export affected users from rule failure message (shows up to 5). Navigate to User Management for each user. Set their communication email. Ensure email domain is authorized for sending. If email comes from HRIS, update sync mapping.'
    },
    
    # Scheduling
    'scheduling_config': {
        'purpose': 'Validates that scheduling_config exists and has a calendarProvider configured (google_calendar, microsoft_outlook_365, or no_calendar_provider).',
        'impact': 'Without scheduling configuration, interview scheduling features are completely unavailable.',
        'resolution': 'Navigate to Admin Console → Talent Acquisition → Scheduling. Select calendar provider. Configure OAuth credentials for Google/Microsoft. Set default preferences.'
    },
    'scheduling_templates': {
        'purpose': 'Validates that at least one scheduling template exists, defining interview types (phone screen, technical, panel, etc.) with duration and participant requirements.',
        'impact': 'Without templates, recruiters cannot schedule interviews as there are no defined interview formats.',
        'resolution': 'Create scheduling templates for each interview type: Phone Screen (30min), Technical Interview (60min), Panel Interview (90min), etc. Define required participants.'
    },
    'scheduling_timezone': {
        'purpose': 'Validates that a default timezone is configured for scheduling, used when user-specific timezone is unavailable.',
        'impact': 'Missing timezone configuration causes scheduling errors and time zone confusion between interviewers and candidates.',
        'resolution': 'Set default timezone in scheduling configuration. Use a central timezone for the organization (e.g., America/Los_Angeles).'
    },
    'standard_schedule_action': {
        'purpose': 'Validates that the schedule action is enabled on profile/pipeline pages, allowing recruiters to initiate scheduling.',
        'impact': 'Without schedule action, recruiters cannot initiate interview scheduling from candidate profiles.',
        'resolution': 'Enable schedule action in profile actions and pipeline actions configuration.'
    },
    'enabled_for_scheduling': {
        'purpose': 'Validates that calendar provider is configured (Google Calendar or Microsoft Outlook 365) for seamless interview scheduling and calendar sync.',
        'impact': 'Without calendar integration, the system cannot check interviewer availability or create calendar events automatically.',
        'resolution': 'Select and configure calendar provider. For Google: set up OAuth. For Microsoft: configure Exchange/O365 integration.'
    },
    'communication_channels': {
        'purpose': 'Validates that communication channels (SMS, WhatsApp) are configured for interview scheduling notifications.',
        'impact': 'Missing channel configurations may limit how scheduling confirmations reach candidates, reducing confirmation rates.',
        'resolution': 'Configure SMS and/or WhatsApp in scheduling communication settings. Note: This only applies if you use non-email channels.'
    },
    
    # Interview Feedback
    'feedback_config_enabled': {
        'purpose': 'Validates that interview feedback feature is configured and enabled, allowing interviewers to submit structured feedback after interviews.',
        'impact': 'Without feedback configuration, interviewers cannot submit feedback, breaking the hiring decision process.',
        'resolution': 'Navigate to Admin Console → Talent Acquisition → Interview Feedback. Set enabled: true. Create at least one feedback form template.'
    },
    'feedback_forms_configured': {
        'purpose': 'Validates that at least one feedback form template exists with defined questions for interviewers.',
        'impact': 'Without form templates, interviewers have no structure for providing feedback.',
        'resolution': 'Create feedback form templates with rating questions (1-5 scale) and text questions. Create different forms for different interview types if needed.'
    },
    'feedback_report': {
        'purpose': 'Validates that feedback report columns and formatting are configured for consolidated feedback review.',
        'impact': 'Missing configuration prevents proper display of consolidated feedback reports for hiring decisions.',
        'resolution': 'Configure feedback report columns: interviewer, date, rating, recommendation, comments.'
    },
    'dashboard_columns_list': {
        'purpose': 'Validates that dashboard columns are configured for the feedback dashboard, showing relevant feedback attributes.',
        'impact': 'Missing columns reduce dashboard usefulness for hiring managers.',
        'resolution': 'Configure columns based on feedback form fields and hiring process needs.'
    },
    
    # Smart Referrals
    'smart_apply_position_fq': {
        'purpose': 'Validates that position filter query (fq) is configured in smart_apply_config, controlling which positions appear in Smart Apply and Referral workflows.',
        'impact': 'Without position_fq, referrals and applications may surface irrelevant positions, reducing Smart Referral effectiveness.',
        'resolution': 'Configure position_fq in Smart Apply settings. Example: "is_open:1 AND is_posted:1" for all posted open positions.'
    },
    'navbar_my_referrals': {
        'purpose': 'Validates that "My Referrals" section is present in Career Hub navigation, allowing employees to view and manage their referrals.',
        'impact': 'Without My Referrals section, employees cannot track their referral activities, reducing referral program participation.',
        'resolution': 'Add my_referrals to Career Hub navigation configuration.'
    },
    'myreferrals_config': {
        'purpose': 'Validates that My Referrals configuration exists, enabling employees to access and manage referral activities.',
        'impact': 'Missing configuration prevents referral visibility and management.',
        'resolution': 'Configure my_referrals section in Career Hub settings.'
    },
    
    # Workflows
    'leads_workflow': {
        'purpose': 'Validates that the Leads Workflow tab exists on the pipeline page, serving as the initial touchpoint for recruiters beginning to fill positions.',
        'impact': 'Missing Leads tab disrupts the recruitment workflow as recruiters cannot access the lead pipeline.',
        'resolution': 'Configure leads workflow in pipeline workflow configuration. Define lead stages and progression rules.'
    },
    'applicants_workflow': {
        'purpose': 'Validates that Applicants Workflow tab is configured on pipeline page, listing candidates who have applied or are under consideration.',
        'impact': 'Missing Applicants tab prevents recruiters from reviewing and advancing applicants efficiently.',
        'resolution': 'Configure applicants workflow with appropriate stages, columns, and actions.'
    },
    
    # Mobile
    'mobile_app_top_nav': {
        'purpose': 'Validates that navigation is configured for the mobile app, enabling proper user navigation.',
        'impact': 'Missing navigation configuration creates poor mobile app experience.',
        'resolution': 'Configure mobile app navigation in mobile app settings.'
    },
    
    # Internal Mobility
    'ijp_apply_redirect_url': {
        'purpose': 'Validates that redirect URL is configured for internal job applications when ATS doesn\'t support API-based apply. Employees are redirected to apply_url_template or apply_url_config.',
        'impact': 'Without redirect URL, employees may face errors when applying to jobs, causing application failures and frustration.',
        'resolution': 'Configure apply_url_template in ATS configuration with appropriate URL pattern including {{position_id}} placeholder.'
    },
    'careerhub_employee_max_resume_size_bytes': {
        'purpose': 'Validates that maximum resume upload size is configured in Career Hub for internal mobility applications.',
        'impact': 'Without size limit configuration, users may encounter errors uploading large resumes.',
        'resolution': 'Configure max resume size in Career Hub settings. Recommended: 20MB (20971520 bytes).'
    },
    'careerhub_employee_allowed_file_types': {
        'purpose': 'Validates that allowed file extensions for resume uploads are configured in Career Hub for employees.',
        'impact': 'Without file type configuration, employees may not be able to upload resumes in their preferred format.',
        'resolution': 'Configure allowed file types: .pdf, .doc, .docx, .txt, .rtf recommended.'
    },
    
    # ==========================================
    # TALENT ACQUISITION - PCS (Career Site)
    # ==========================================
    'pcsx_base_enabled_cs': {
        'purpose': 'Validates that PCS (Professional Career Site) base configuration is enabled in pcsx_base_config. This is the foundational setting for all career site functionality.',
        'impact': 'Career site will be completely inaccessible to candidates without base configuration enabled.',
        'resolution': 'Navigate to Admin Console → Career Site → Base Configuration. Set enabled: true. Configure minimum required settings.'
    },
    'pcs_logo_configured_cs': {
        'purpose': 'Validates that company logo is uploaded in branding configuration. Logo URL must be valid and not a placeholder.',
        'impact': 'Career site displays without company logo, impacting brand recognition and professional appearance.',
        'resolution': 'Navigate to Career Site → Branding. Upload company logo (recommended: 200x50px PNG with transparent background).'
    },
    'pcs_colors_configured_cs': {
        'purpose': 'Validates that brand colors are configured with valid hex codes (e.g., #146da6). Both primary and secondary colors should be set.',
        'impact': 'Career site uses default colors instead of brand colors, looking generic and unprofessional.',
        'resolution': 'Configure primary and secondary colors in Branding settings using valid hex format (#RRGGBB).'
    },
    'apply_form_configured_cs': {
        'purpose': 'Validates that application form configuration exists, defining required fields, optional fields, and validation rules for job applications.',
        'impact': 'Candidates cannot apply to positions without form configuration.',
        'resolution': 'Configure apply form with resume requirements, required fields (name, email, phone), and optional fields. Set up validation rules.'
    },
    'smart_apply_enabled_cs': {
        'purpose': 'Validates that Smart Apply is enabled with proper ATS integration for application sync.',
        'impact': 'Applications will not sync to ATS, breaking the recruiting workflow. Candidates may apply but applications get lost.',
        'resolution': 'Enable Smart Apply in configuration. Configure ATS integration for application sync. Set push_application_to_ats if needed.'
    },
    'field_mapping_complete_cs': {
        'purpose': 'Validates that field mappings are complete, defining how candidate data maps from Eightfold to ATS fields.',
        'impact': 'Incomplete mappings cause application data to be lost or incorrectly synced to ATS.',
        'resolution': 'Map all required fields: name, email, phone, resume, source, and any custom ATS fields.'
    },
    'search_config_enabled_cs': {
        'purpose': 'Validates that job search is enabled on career site, allowing candidates to search and filter positions.',
        'impact': 'Candidates cannot search for jobs, only browse, creating poor user experience.',
        'resolution': 'Enable search in Career Site configuration. Configure default search behavior and sort options.'
    },
    'search_filters_available_cs': {
        'purpose': 'Validates that search filters are configured (location, department, job type, etc.) for refining job searches.',
        'impact': 'Candidates cannot filter search results, making it difficult to find relevant positions.',
        'resolution': 'Configure filters: Location, Department, Job Type (Full-time, Part-time), Remote/Hybrid, Experience Level.'
    },
    'global_search_enabled_cs': {
        'purpose': 'Validates that global search is enabled for recruiter talent network searching.',
        'impact': 'Recruiters cannot search candidate talent network.',
        'resolution': 'Enable global search and configure search filters for candidate discovery.'
    },
    'search_filters_configured_cs': {
        'purpose': 'Validates that search filters are configured for global search including location, skills, experience, etc.',
        'impact': 'Recruiters cannot effectively filter search results.',
        'resolution': 'Configure filters: Location, Skills, Experience/Seniority, Current Company, Job Title.'
    },
    'talent_network_enabled_cs': {
        'purpose': 'Validates that talent network join feature is enabled, allowing candidates to join without applying to specific positions.',
        'impact': 'Candidates cannot join talent network, limiting talent pool growth.',
        'resolution': 'Enable talent network join in Smart Apply configuration.'
    },
    'talent_network_form_configured_cs': {
        'purpose': 'Validates that talent network join form is configured with required fields.',
        'impact': 'Join form may be incomplete or fail to capture necessary candidate information.',
        'resolution': 'Configure join form: required fields (email, name), optional fields (phone, interests), consent checkboxes.'
    },
    'referrals_enabled_cs': {
        'purpose': 'Validates that smart referral feature is enabled for employee referral programs.',
        'impact': 'Employee referral functionality will not be available, missing key sourcing channel.',
        'resolution': 'Enable referrals in Smart Apply configuration. Configure referral workflow.'
    },
    'referral_workflow_configured_cs': {
        'purpose': 'Validates that referral workflow is configured with submission form, tracking, and optional rewards.',
        'impact': 'Incomplete referral process confuses employees and reduces referral program effectiveness.',
        'resolution': 'Configure referral submission form, status tracking, reward rules (if applicable), and employee dashboard.'
    },
    'source_tracking_enabled_cs': {
        'purpose': 'Validates that source tracking is enabled to capture candidate origins (job boards, social media, referrals, etc.).',
        'impact': 'Cannot track recruitment marketing effectiveness or attribute candidates to sources.',
        'resolution': 'Enable source tracking in Career Site configuration. Configure UTM parameter mapping.'
    },
    'source_parameters_configured_cs': {
        'purpose': 'Validates that source tracking parameters (UTM mapping, referral codes) are configured.',
        'impact': 'Sources are not captured correctly, leading to inaccurate attribution.',
        'resolution': 'Configure UTM parameter mapping (source, medium, campaign), referral codes, and default source.'
    },
    'source_ats_sync_configured_cs': {
        'purpose': 'Validates that source tracking data is mapped to sync with applications to ATS.',
        'impact': 'Source tracking data is lost when applications sync to ATS, breaking source reporting.',
        'resolution': 'Configure source field mapping in Smart Apply to map Eightfold source to ATS source field.'
    },
    'seo_config_valid_cs': {
        'purpose': 'Validates that SEO configuration is set up including meta tags, structured data, and sitemap settings.',
        'impact': 'Career site has poor search engine visibility and rankings, reducing organic traffic.',
        'resolution': 'Configure meta titles/descriptions, enable structured data (JSON-LD), enable sitemap generation, set canonical URLs.'
    },
    'job_feed_enabled_cs': {
        'purpose': 'Validates that job feed generation is enabled for distribution to job boards.',
        'impact': 'Jobs are not distributed to job boards (Indeed, LinkedIn, etc.), limiting reach.',
        'resolution': 'Enable job feed configuration. Configure feed URLs for each job board partner.'
    },
    'job_alerts_enabled_cs': {
        'purpose': 'Validates that job alerts are enabled, allowing candidates to receive personalized job recommendations via email.',
        'impact': 'Candidates will not receive job alert emails, reducing ongoing engagement.',
        'resolution': 'Enable job alerts in notification configuration for candidate product.'
    },
    'job_alert_frequency_configured_cs': {
        'purpose': 'Validates that job alert frequency options are configured (daily, weekly, real-time).',
        'impact': 'Alerts may send too frequently or not at all without proper frequency configuration.',
        'resolution': 'Configure frequency options: Daily, Weekly, Bi-weekly, and optionally Real-time.'
    },
    'login_signup_configured_cs': {
        'purpose': 'Validates that candidate login/signup configuration is set up including authentication method and required fields.',
        'impact': 'Candidates cannot create accounts or log in, preventing saved jobs and application tracking.',
        'resolution': 'Configure authentication method (email/password, SSO, social), required signup fields, password requirements.'
    },
    'profile_sections_defined_cs': {
        'purpose': 'Validates that profile sections (Overview, Experience, Education, Skills) are defined and enabled for candidate profiles.',
        'impact': 'Profile information cannot be displayed to recruiters without section configuration.',
        'resolution': 'Enable profile sections: Overview (required), Experience, Education, Skills, Certifications.'
    },
    'profile_fields_configured_cs': {
        'purpose': 'Validates that candidate profile fields are defined for the living profile experience.',
        'impact': 'Candidates cannot maintain their profile with latest skills and experience.',
        'resolution': 'Configure profile fields: basic info, experience fields, education, skills, certifications. Mark required vs optional.'
    },
    'candidate_profile_enabled_cs': {
        'purpose': 'Validates that candidate profile feature is enabled for living profile functionality.',
        'impact': 'Candidates cannot create or update profiles for future applications.',
        'resolution': 'Enable candidate profile in configuration. Set enabled: true.'
    },
    'custom_domain_configured_cs': {
        'purpose': 'Validates that custom domain (e.g., careers.company.com) is configured instead of default Eightfold domain.',
        'impact': 'Career site uses default Eightfold URL instead of branded company domain.',
        'resolution': 'Configure custom domain in domain whitelabeling. Set up DNS CNAME record. Verify accessibility.'
    },
    'ssl_certificate_valid_cs': {
        'purpose': 'Validates that SSL certificate is present and valid for HTTPS access.',
        'impact': 'Career site shows security warnings or is inaccessible via HTTPS, deterring candidates.',
        'resolution': 'Upload SSL certificate matching domain name. Ensure certificate is not expired and chain is complete.'
    },
    'withdraw_enabled_cs': {
        'purpose': 'Validates that withdraw application feature is enabled, allowing candidates to withdraw their applications.',
        'impact': 'Candidates cannot withdraw applications, leading to poor experience when circumstances change.',
        'resolution': 'Enable withdraw application in Career Site applications configuration.'
    },
    'withdraw_workflow_valid_cs': {
        'purpose': 'Validates that withdraw workflow is configured with confirmation, ATS sync, and candidate notification.',
        'impact': 'Withdrawals may not sync to ATS or candidates may withdraw accidentally.',
        'resolution': 'Configure confirmation dialog, ATS sync for withdrawals, candidate confirmation email.'
    },
    
    # Microsites
    'microsite_configs_valid_cs': {
        'purpose': 'Validates that each microsite has complete configuration including branding, domain, and job filters.',
        'impact': 'Microsites display incorrectly or show wrong job listings.',
        'resolution': 'For each microsite, configure: unique ID, branding settings, domain/subdomain, job filter rules, navigation.'
    },
    
    # Copilot
    'copilot_feature_enabled_cs': {
        'purpose': 'Validates that Copilot feature is explicitly enabled in configuration.',
        'impact': 'Copilot features (AI assistance) not accessible to users.',
        'resolution': 'Enable Copilot in copilot_config. Set enabled: true.'
    },
    'copilot_capabilities_configured_cs': {
        'purpose': 'Validates that specific Copilot capabilities (job description generation, scheduling assistant, etc.) are enabled.',
        'impact': 'Copilot is enabled but has no usable features.',
        'resolution': 'Enable desired capabilities: job_description_generation, scheduling_assistant, candidate_summary, etc.'
    },
    'chatbot_config_enabled_cs': {
        'purpose': 'Validates that candidate-facing chatbot/copilot is configured and enabled.',
        'impact': 'Candidate copilot features not available on career site.',
        'resolution': 'Enable chatbot in chatbotx_config for candidate product.'
    },
    
    # Events
    'event_config_enabled_cs': {
        'purpose': 'Validates that event recruiting feature is configured and enabled.',
        'impact': 'Event recruiting features are inaccessible.',
        'resolution': 'Enable event recruiting in planned_event_config. Set enabled: true.'
    },
    'event_stages_configured_cs': {
        'purpose': 'Validates that event-specific pipeline stages are configured (Registered, Attended, Interviewed, etc.).',
        'impact': 'Candidates in events cannot be moved through stages.',
        'resolution': 'Define event stages in planned_event_workflow_config: Registered, Attended, Interviewed, Shortlisted, etc.'
    },
    'event_home_config_valid_cs': {
        'purpose': 'Validates that event home configuration is set up for event listing display.',
        'impact': 'Events list may not display correctly to recruiters.',
        'resolution': 'Configure event home display settings in planned_event_home_config.'
    },
    
    # Communities
    'community_config_enabled_cs': {
        'purpose': 'Validates that talent communities feature is configured and enabled for talent pool management.',
        'impact': 'Talent communities features are inaccessible.',
        'resolution': 'Enable talent communities in community_home_config. Set enabled: true.'
    },
    'community_stages_configured_cs': {
        'purpose': 'Validates that community pipeline stages are configured for member progression.',
        'impact': 'Community members cannot be managed through pipeline stages.',
        'resolution': 'Define community stages in community_workflow_config for each community type.'
    },
    'community_home': {
        'purpose': 'Validates that community home page is configured with columns, filters, and filter-to-fq mapping.',
        'impact': 'Community Home page may be non-functional or significantly impaired for talent sourcing.',
        'resolution': 'Configure available_filters, filter_to_fq_data_map, and columns in community_home_config.'
    },
    'community_workflows': {
        'purpose': 'Validates that community_workflow_config is defined per community type with valid display_name and workflow steps.',
        'impact': 'Communities cannot progress prospects or reflect status, breaking sourcing workflows.',
        'resolution': 'Configure workflow per community type with display_name and non-empty steps array.'
    },
    
    # Campaigns
    'campaign_config_enabled_cs': {
        'purpose': 'Validates that smart campaigns feature is configured and enabled for candidate nurturing.',
        'impact': 'Campaign features are inaccessible, limiting automated candidate engagement.',
        'resolution': 'Enable smart campaigns in campaign_config. Set enabled: true.'
    },
    'campaign_email_templates_exist_cs': {
        'purpose': 'Validates that email templates for campaigns exist (tagged as campaign_email).',
        'impact': 'Campaigns cannot send emails without templates.',
        'resolution': 'Create email templates in Email Templates, tag them for campaign use.'
    },
    
    # Workflow Automation
    'workflow_automation_enabled_cs': {
        'purpose': 'Validates that workflow automation feature is enabled for automated candidate workflows.',
        'impact': 'Workflow automation features are unavailable.',
        'resolution': 'Enable workflow automation in workflow_automation_config. Set enabled: true.'
    },
    'workflow_triggers_valid_cs': {
        'purpose': 'Validates that at least one workflow trigger is configured with valid event and actions.',
        'impact': 'Workflows cannot execute without trigger configuration.',
        'resolution': 'Configure triggers: stage_change, application_submitted, etc. with associated actions.'
    },
    
    # Diversity
    'diversity_config_enabled_cs': {
        'purpose': 'Validates that diversity configuration exists for bias reduction features like profile masking.',
        'impact': 'Diversity and bias reduction features cannot function.',
        'resolution': 'Initialize diversity configuration in diversity_config.'
    },
    'masking_fields_configured_cs': {
        'purpose': 'Validates that if masking is enabled, specific fields are configured to be masked (age, gender, etc.).',
        'impact': 'Masking feature is enabled but no fields are actually masked.',
        'resolution': 'Configure fields to mask: age, gender, ethnicity, educational_background, photo.'
    },
    
    # Email/SMS/WhatsApp
    'email_config_enabled_cs': {
        'purpose': 'Validates that email configuration exists with reply_to_domain and send_from_domain properly set.',
        'impact': 'Email sending functionality may not work properly.',
        'resolution': 'Configure email settings: reply_to_domain, send_from_domain. Verify domain authentication.'
    },
    'sms_integration_enabled_cs': {
        'purpose': 'Validates that SMS integration is configured with provider credentials (Twilio, etc.) and phone number.',
        'impact': 'SMS messages cannot be sent without provider configuration.',
        'resolution': 'Configure SMS provider (Twilio), set API credentials, add verified from phone number.'
    },
    'whatsapp_integration_enabled_cs': {
        'purpose': 'Validates that WhatsApp Business API integration is configured with provider and phone number.',
        'impact': 'WhatsApp messages cannot be sent without provider configuration.',
        'resolution': 'Configure WhatsApp BSP, set API credentials, verify business phone number.'
    },
    
    # Star Threshold
    'star_threshold': {
        'purpose': 'Validates that pcsx_base_config → search_config → strong_match_threshold is configured to define minimum match criteria for displaying candidates.',
        'impact': 'Without threshold configuration, irrelevant matches may surface, creating poor candidate and recruiter experience.',
        'resolution': 'Configure strong_match_threshold in search_config. Recommended: 3.25 (out of 5 stars).'
    },
    
    # Chrome Extension
    'extension_actions': {
        'purpose': 'Validates that Chrome Extension actions (save candidate, set status, set reminder) are properly configured.',
        'impact': 'Missing actions hinder efficient candidate management from the extension.',
        'resolution': 'Configure all required actions and sub-actions in extension configuration.'
    },
    'extension_reminder_action': {
        'purpose': 'Validates that reminders set on candidate profiles are visible across platforms including EF extension.',
        'impact': 'Without this, team members may duplicate outreach efforts.',
        'resolution': 'Enable reminder_action in extension configuration.'
    },
    'app_configs': {
        'purpose': 'Validates that hostname is set in app_configs for LinkedIn, Naukri, and GitHub extension integration.',
        'impact': 'Missing hostname prevents proper extension interaction with these websites.',
        'resolution': 'Configure hostname for each supported website in extension app_configs.'
    },
    'extension_communities_disabled_text': {
        'purpose': 'Validates that a clear message is displayed when Communities feature is disabled in the extension.',
        'impact': 'Users confused about feature unavailability.',
        'resolution': 'Configure disabled message explaining why Communities is unavailable and what steps to take.'
    },
}

def generate_enhanced_description(rule_id, existing_desc, original_desc):
    """Generate enhanced description using technical reference knowledge."""
    
    if rule_id in ENHANCED_DESCRIPTIONS:
        enhanced = ENHANCED_DESCRIPTIONS[rule_id]
        purpose = enhanced.get('purpose', '')
        impact = enhanced.get('impact', '')
        resolution = enhanced.get('resolution', '')
        
        # Format as Purpose/Impact with optional Resolution hint
        if resolution:
            return f"**Purpose:** {purpose} **Impact:** {impact} **To Fix:** {resolution}"
        else:
            return f"**Purpose:** {purpose} **Impact:** {impact}"
    
    # Return existing description if no enhancement available
    return existing_desc if existing_desc else original_desc

def enhance_descriptions():
    """Enhance all rule descriptions in the TSV."""
    # Read the TSV file
    df = pd.read_csv(INPUT_FILE, sep='\t', dtype=str)
    
    # Find columns
    rule_id_col = None
    cursor_desc_col = None
    original_desc_col = None
    
    for col in df.columns:
        if 'Rule ID' in col:
            rule_id_col = col
        if 'Cursor Generated Description' in col:
            cursor_desc_col = col
        if col == 'Description':
            original_desc_col = col
    
    if not rule_id_col or not cursor_desc_col:
        print(f"Could not find required columns. Found: {df.columns.tolist()}")
        return
    
    print(f"Found columns: Rule ID='{rule_id_col}', Cursor Desc='{cursor_desc_col}'")
    
    # Apply enhancements
    enhanced_count = 0
    for idx, row in df.iterrows():
        rule_id = str(row[rule_id_col]).strip() if pd.notna(row[rule_id_col]) else ''
        existing_desc = str(row[cursor_desc_col]) if pd.notna(row[cursor_desc_col]) else ''
        original_desc = str(row.get(original_desc_col, '')) if original_desc_col else ''
        
        if rule_id in ENHANCED_DESCRIPTIONS:
            new_desc = generate_enhanced_description(rule_id, existing_desc, original_desc)
            df.at[idx, cursor_desc_col] = new_desc
            print(f"Enhanced: {rule_id}")
            enhanced_count += 1
    
    # Save the updated TSV
    df.to_csv(OUTPUT_FILE, sep='\t', index=False)
    print(f"\nEnhanced {enhanced_count} descriptions in {OUTPUT_FILE}")
    print(f"Total rules with enhancements available: {len(ENHANCED_DESCRIPTIONS)}")

if __name__ == '__main__':
    enhance_descriptions()
