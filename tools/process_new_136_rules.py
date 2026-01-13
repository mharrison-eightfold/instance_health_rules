#!/usr/bin/env python3
"""
Process the 136 new Instance Health rules (AI, Security, Analytics, TIP).
Add config references where missing (#N/A) and generate enhanced descriptions.
"""

import csv
import re

# Config reference mappings for rules with #N/A
CONFIG_REFERENCE_MAP = {
    # AI Rules - Internal Positions
    "internal_positions_calibrated_rule": "calibration_config → position calibration settings",
    "internal_positions_with_location_rule": "Position Sync (ATS) → position.location",
    "internal_positions_with_skills_rule": "Position calibration → skills / AI skill inference",
    "internal_positions_with_multiple_skills_rule": "Position calibration → skills (minimum 3 required)",
    "internal_positions_with_job_band_rule": "ijp_config → job_bands / position.hiring_band",
    
    # AI Rules - Employee Profiles
    "claimed_employee_profiles_with_levels": "Employee Sync (HRIS) → employee.level / ijp_config → job_bands",
    "claimed_employee_profiles_with_skills": "Employee profile → skills / Profile Assistant",
    "claimed_employee_profiles_open_to_mentor": "career_hub_base_config → mentorship.enabled / Employee profile settings",
    
    # AI Rules - Projects
    "projects_with_multiple_skills_rule": "Project definition → skills (minimum 3 required)",
    "projects_with_ideal_candidates_rule": "Project calibration → ideal_candidates (minimum 3)",
    "projects_with_location_rule": "Project definition → location",
    
    # AI Rules - Courses
    "courses_with_skills_rule": "Course Sync (LMS) → course.skills",
    "courses_with_description_rule": "Course Sync (LMS) → course.description (minimum 50 words)",
    
    # AI Rules - Roles
    "role_levels_in_internal_mobility_config_quality": "ijp_config → career_navigator_seniority_ordering / job_bands",
    "role_job_code_quality": "role_library_config → roles.job_code / Role Sync (HRIS)",
    "role_lob_quality": "role_library_config → roles.business_function / Role Sync (HRIS)",
    "role_skills_quality": "role_library_config → roles.skills (minimum 3 required)",
    
    # AI Rules - Mentors
    "mentor_profiles_with_rich_data": "Employee profile → skills, experience, topics / mentorship settings",
    
    # Security Rules
    "is_pcs_seo_optimization_for_sandbox_true": "pcsx_base_config → seo_config.enabled (sandbox should be false)",
    "num_external_domains": "external_account_for_group_id config (max 20 domains)",
    "max_campaign_limit": "campaign_config → max_per_campaign (max 2000)",
    "email_loopback_prod": "email_loopback_gate (should be disabled for prod)",
    "email_loopback_non_prod": "email_loopback_gate (should be enabled for sandbox)",
    "provision_user_accounts_prod": "user_provisioning_config → provision_from_employee_sync",
    "custom_session_timeout_config": "custom_session_timeout_config (max 24 hours)",
    "employee_profile_visibility": "career_hub_base_config → profile_visibility / unclaimed_employee_visibility",
    "candidate_sync_failure_rule": "ats_config → sync settings / sync error monitoring",
    "position_sync_failure_rule": "ats_config → sync settings / sync error monitoring",
    "employee_sync_failure_rule": "ats_config → sync settings / sync error monitoring",
    "num_rejections_rule": "Operational metrics → rejection tracking / statistical analysis",
    "application_failures_rule": "Operational metrics → application error tracking",
    "profile_data_retention_rule": "data_retention_config → talent pool rules (max 10%)",
    "unsubscribe_requests_volume_rule": "email_config → unsubscribe tracking",
    "emails_sent_to_employees": "email_config → employee email frequency limits",
    "num_emails_rule": "email_config → email volume monitoring",
    "num_admin_accounts_rule": "Admin Console → Manage Users → admin role count",
    "data_subject_requests": "data_retention_config → GDPR/CCPA request tracking",
    
    # Analytics Rules - Employee
    "employee_level_quality": "Employee Sync (HRIS) → profile.data_json.employee.level",
    "employee_location_country_quality": "Employee Sync (HRIS) → profile.data_json.employee.location_country",
    "employee_email_quality": "Employee Sync (HRIS) → profile.data_json.employee.email",
    "employee_is_alumni_and_termination_date_discrepancy_quality": "Employee Sync (HRIS) → employee.is_alumni / employee.termination_date",
    "employee_first_name_quality": "Employee Sync (HRIS) → profile.data_json.employee.first_name",
    "employee_last_name_quality": "Employee Sync (HRIS) → profile.data_json.employee.last_name",
    "employee_hiring_date_quality": "Employee Sync (HRIS) → profile.data_json.employee.hire_date",
    "employee_location_quality": "Employee Sync (HRIS) → profile.data_json.employee.location",
    "employee_manager_id_quality": "Employee Sync (HRIS) → profile.data_json.employee.manager_id",
    "employee_manager_email_quality": "Employee Sync (HRIS) → profile.data_json.employee.manager_email",
    "employee_division_quality": "Employee Sync (HRIS) → profile.data_json.employee.division",
    "employee_internal_candidate_id_quality": "Employee Sync (HRIS) → employee.internal_candidate_id linkage",
    
    # Analytics Rules - Profile
    "profile_first_name_quality": "Candidate Sync (ATS) → profile.first_name",
    "profile_last_name_quality": "Candidate Sync (ATS) → profile.last_name",
    
    # Analytics Rules - Application Funnel
    "application_funnel_more_new_applicants_than_phonescreen": "ats_config → stage_map / diversity_dashboard_config → application_stage_map",
    "application_funnel_more_phonescreen_than_onsite": "ats_config → stage_map / diversity_dashboard_config → application_stage_map",
    "application_funnel_more_onsite_than_offer": "ats_config → stage_map / diversity_dashboard_config → application_stage_map",
    "application_funnel_more_offer_than_hired": "ats_config → stage_map / diversity_dashboard_config → application_stage_map",
    
    # Analytics Rules - Application Quality
    "application_source_type_quality": "Candidate Sync (ATS) → application.source_type",
    "application_offer_stage_group_quality": "ats_config → stage_map → offer stage group",
    "phonescreen_stage_group_quality": "ats_config → stage_map → phonescreen stage group",
    "application_new_applicant_stage_group_quality": "ats_config → stage_map → new_applicant stage group",
    "application_onsite_or_interview_stage_group_quality": "ats_config → stage_map → onsite stage group",
    "application_hired_stage_group_quality": "ats_config → stage_map → hired stage group",
    "application_stage_group_quality": "ats_config → stage_map → all stage groups (not 'Others')",
    "application_rejection_reason_quality": "Candidate Sync (ATS) → application.rejection_reason",
    "application_hired_ts_quality": "Candidate Sync (ATS) → application.hired_ts",
    "application_ts_quality": "Candidate Sync (ATS) → application.application_ts",
    "application_profile_id_quality": "Candidate Sync (ATS) → application.profile_id",
    "application_id_quality": "Candidate Sync (ATS) → application.application_id",
    "application_stage_ts_quality": "Candidate Sync (ATS) → application.stage_ts",
    "application_status_quality": "Candidate Sync (ATS) → application.status",
    "application_active_status_quality": "Candidate Sync (ATS) → application.status = 'active'",
    "application_hired_ts_and_hired_stagegroup_discrepancy_quality": "ats_config → stage_map / application.hired_ts consistency",
    
    # Analytics Rules - Position
    "position_status_data_quality": "Position Sync (ATS) → position.status",
    "position_location_country_quality": "Position Sync (ATS) → position.location_country",
    "position_hiring_manager_name_data_quality": "Position Sync (ATS) → position.hiring_manager_name",
    "position_title_data_quality": "Position Sync (ATS) → position.title",
    "position_business_unit_data_quality": "Position Sync (ATS) → position.business_unit",
    "position_hiring_manager_email_data_quality": "Position Sync (ATS) → position.hiring_manager_email",
    "position_job_function_data_quality": "Position Sync (ATS) → position.job_function",
    "position_creation_ts_data_quality": "Position Sync (ATS) → position.creation_ts",
    "open_position_recruiter_name_data_quality": "Position Sync (ATS) → position.recruiter_name",
    "open_position_recruiter_email_data_quality": "Position Sync (ATS) → position.recruiter_email",
    
    # Analytics Rules - Stage Mapping
    "stagemap_hired": "ats_config → stage_map → hired stage group mapping",
    "stagemap_hired_equal_to_diversity_config_hired": "ats_config → stage_map / diversity_dashboard_config → hired consistency",
    "all_stage_transition_map_stages_in_diversity_dashboard_config": "diversity_dashboard_config → application_stage_map completeness",
    "application_stage_map_index_consistency": "diversity_dashboard_config → application_stage_map index continuity",
    "application_stage_group_funnel_shape_consistency": "diversity_dashboard_config → application_stage_map funnel shape",
    
    # Analytics Rules - Classification
    "custom_fields_v2_position_is_open": "custom_fields_v2 → position → is_open field mapping",
    "internal_app_regex": "ats_config → internal_app_regex source type classification",
    "referral_regex": "ats_config → referral_regex source type classification",
    "internal_applications": "ats_config → internal_app_regex percentage tracking",
    "referral_applications": "ats_config → referral_regex percentage tracking",
    
    # TIP Rules - Platform
    "talent_lake_provisioned": "Talent Lake provisioning / Data Warehouse enablement",
    "data_retention_config": "data_retention_config → GDPR/CCPA compliance rules",
    "email_loopback": "email_loopback_gate / loopback_whitelisted_recipient_emails",
    "oauth_enabled": "integration_systems → [adaptor] → oauth_settings",
    
    # TIP Rules - Sync
    "position_sync_lag_rule": "ats_config → position sync / sync_lag_threshold (60 min)",
    "candidate_sync_lag_rule": "ats_config → candidate sync / sync_lag_threshold (60 min)",
    "employee_sync_lag_rule": "ats_config → employee sync / sync_lag_threshold (24 hours)",
    
    # TIP Rules - Webhooks
    "candidate_webhook_sync_rule": "integration_systems → webhook_settings (90% success rate)",
    "position_webhook_sync_rule": "integration_systems → webhook_settings (90% success rate)",
    "webhook_event_failure_rule": "integration_systems → webhook_settings health",
    "webhook_enabled": "integration_systems → webhook_settings.status = enabled",
    
    # TIP Rules - Custom Fields
    "custom_fields_v2_application_reason": "custom_fields_v2 → application → reason (rejection reasons)",
    "custom_fields_v2_position_recruiter": "custom_fields_v2 → position → recruiter field mapping",
    "custom_fields_v2_position_hiring_manager": "custom_fields_v2 → position → hiring_manager field mapping",
    "custom_fields_v2_position_hiring_band": "custom_fields_v2 → position → hiring_band field mapping",
    "custom_fields_v2_position_job_function": "custom_fields_v2 → position → job_function field mapping",
    "custom_fields_v2_position_business_unit": "custom_fields_v2 → position → business_unit field mapping",
    "custom_fields_v2_application_race": "custom_fields_v2 → application → race (EEOC)",
    "custom_fields_v2_application_gender": "custom_fields_v2 → application → gender (EEOC)",
    "custom_fields_v2_application_disability_status": "custom_fields_v2 → application → disability_status (EEOC)",
    "custom_fields_v2_application_veteran_status": "custom_fields_v2 → application → veteran_status (EEOC)",
    "custom_fields_v2_candidate_race": "custom_fields_v2 → candidate → race (EEOC)",
    "custom_fields_v2_candidate_gender": "custom_fields_v2 → candidate → gender (EEOC)",
    "custom_fields_v2_candidate_disability_status": "custom_fields_v2 → candidate → disability_status (EEOC)",
    "custom_fields_v2_candidate_veteran_status": "custom_fields_v2 → candidate → veteran_status (EEOC)",
    
    # TIP Rules - Workday Specific
    "candidate_raas_list_report": "Workday → RAAS List Report for candidates",
    "position_raas_list_report": "Workday → RAAS List Report for positions",
    "questionnaire_raas_list_report": "Workday → RAAS List Report for questionnaires",
    
    # TIP Rules - Job Posting Sites
    "internal_job_posting_sites": "enterprise_config → internal_job_posting_sites (Workday/Taleo)",
    "external_job_posting_sites": "enterprise_config → external_job_posting_sites (Workday/Taleo/SF/Greenhouse)",
    
    # TIP Rules - Application Sources
    "add_application_sources_referral": "integration_systems → add_application_sources → referral (iCIMS/Jobvite)",
    "add_application_sources_employee": "integration_systems → add_application_sources → employee (iCIMS/Jobvite)",
    "add_application_sources_applied": "integration_systems → add_application_sources → applied (iCIMS/Jobvite)",
    "internal_app_regex_source_type": "integration_systems → internal_app_regex → source_type",
    "career_site_source_id": "integration_systems → career_site_source_id (SuccessFactors)",
    
    # TIP Rules - SuccessFactors Specific
    "list_terminated_employees": "integration_systems → list_terminated_employees (SuccessFactors)",
    "stage_advance_using_odata": "integration_systems → stage_advance_using_odata (SuccessFactors)",
    "hide_skipped_statuses_in_application_trail": "integration_systems → hide_skipped_statuses_in_application_trail (SF)",
    "internal_to_external_candidate_profile_conversion_rule": "SuccessFactors → internal to external conversion setting",
    
    # TIP Rules - Support
    "reply_to_eightfold_support_email_validation": "email_config → reply_to (not support@eightfold.ai)",
}

# Code reference mappings
CODE_REFERENCE_MAP = {
    # AI/Data Health Rules
    "internal_positions": "www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py",
    "claimed_employee": "www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py",
    "projects_with": "www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py",
    "courses_with": "www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py",
    "role_": "www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py",
    "mentor_profiles": "www/data_audit/platform_health/data_health/product_data_health_evaluation_rules.py",
    
    # Security/Operational Rules
    "sync_failure": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "sync_lag": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "num_rejections": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "application_failures": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "profile_data_retention": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "unsubscribe": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "emails_sent": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "num_emails": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "num_admin": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    "data_subject": "www/data_audit/platform_health/operational_health/operational_health_evaluation_rules.py",
    
    # Analytics/Data Quality Rules
    "employee_level": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_location": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_email": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_first": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_last": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_hiring": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_manager": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_division": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_internal": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "employee_is_alumni": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "profile_first": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "profile_last": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_funnel": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_source": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_offer": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "phonescreen_stage": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_new": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_onsite": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_hired": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_stage": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_rejection": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_ts": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_profile": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_id": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_status": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "application_active": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_status": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_location": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_hiring": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_title": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_business": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_job": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "position_creation": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "open_position": "www/data_audit/platform_health/data_health/data_health_evaluation_rules.py",
    "stagemap": "www/data_audit/platform_health/config_health/ats_config_health_configurable_rules.py",
    "all_stage_transition": "www/data_audit/platform_health/config_health/ats_config_health_configurable_rules.py",
    
    # Config Health Rules
    "custom_fields": "www/data_audit/platform_health/config_health/ats_config_health_configurable_rules.py",
    "internal_app": "www/data_audit/platform_health/config_health/ats_config_health_configurable_rules.py",
    "referral_": "www/data_audit/platform_health/config_health/ats_config_health_configurable_rules.py",
    "webhook": "www/integrations_console/config_health/config_health_rule.py",
    "oauth": "www/integrations_console/config_health/config_health_rule.py",
    "raas": "www/integrations_console/config_health/config_health_rule.py",
    "job_posting_sites": "www/integrations_console/config_health/config_health_rule.py",
    "add_application_sources": "www/integrations_console/config_health/config_health_rule.py",
    "career_site_source": "www/integrations_console/config_health/config_health_rule.py",
    "list_terminated": "www/integrations_console/config_health/config_health_rule.py",
    "stage_advance": "www/integrations_console/config_health/config_health_rule.py",
    "hide_skipped": "www/integrations_console/config_health/config_health_rule.py",
    "internal_to_external": "www/integrations_console/config_health/config_health_rule.py",
    "reply_to": "www/integrations_console/config_health/config_health_rule.py",
    
    # Platform Rules
    "talent_lake": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "data_retention": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "email_loopback": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "is_pcs_seo": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "num_external": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "max_campaign": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "provision_user": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "session_timeout": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
    "employee_profile_visibility": "www/data_audit/platform_health/config_health/product_config_health_configurable_rules.py",
}


def get_config_reference(rule_id):
    """Get config reference for a rule."""
    if rule_id in CONFIG_REFERENCE_MAP:
        return CONFIG_REFERENCE_MAP[rule_id]
    return ""


def get_code_reference(rule_id):
    """Get code reference for a rule."""
    for pattern, code_ref in CODE_REFERENCE_MAP.items():
        if pattern in rule_id.lower():
            return code_ref
    return "www/data_audit/platform_health/"


def generate_enhanced_description(rule_id, rule_name, original_description, product_area):
    """Generate an enhanced description with Purpose, Impact, and To Fix sections."""
    
    # Clean up original description
    desc = original_description.replace('<br>', ' ').replace('<br/>', ' ')
    desc = re.sub(r'<h5>.*?</h5>', '', desc)
    desc = re.sub(r'\[Purpose\]', '', desc)
    desc = re.sub(r'\[Impact\]', '', desc)
    desc = re.sub(r'"', '', desc)
    desc = desc.strip()
    
    # Extract purpose and impact if present
    purpose = ""
    impact = ""
    
    if "Impact of failure" in desc.lower():
        parts = re.split(r'Impact of failure\.?', desc, flags=re.IGNORECASE)
        purpose = parts[0].strip().rstrip('.')
        if len(parts) > 1:
            impact = parts[1].strip()
    elif "impact" in desc.lower() and ("purpose" in desc.lower() or desc.startswith("[")):
        parts = desc.split("Impact")
        purpose = parts[0].replace("[Purpose]", "").strip().rstrip('.')
        if len(parts) > 1:
            impact = parts[1].strip().lstrip(':').lstrip()
    else:
        purpose = desc
    
    # Generate To Fix based on rule type
    to_fix = generate_fix_instructions(rule_id, product_area)
    
    # Build enhanced description
    enhanced = f"**Purpose:** {purpose if purpose else 'Validates ' + rule_name.lower()}"
    if impact:
        enhanced += f"\n\n**Impact:** {impact}"
    else:
        enhanced += f"\n\n**Impact:** Rule failure indicates data quality or configuration issues that may affect system functionality and reporting accuracy."
    enhanced += f"\n\n**To Fix:** {to_fix}"
    
    return enhanced


def generate_fix_instructions(rule_id, product_area):
    """Generate fix instructions based on rule ID and product area."""
    
    rule_lower = rule_id.lower()
    
    # AI Rules
    if "internal_positions_calibrated" in rule_lower:
        return "Navigate to each open position and complete the calibration process by adding ideal candidates and adjusting skill requirements."
    elif "internal_positions_with_location" in rule_lower:
        return "Ensure positions have location data in the ATS. Check Position Sync mappings and verify location field is correctly mapped."
    elif "internal_positions_with_skills" in rule_lower:
        return "Calibrate positions by adding skills manually or enable AI skill inference. Verify calibration_config settings."
    elif "internal_positions_with_multiple_skills" in rule_lower:
        return "Review position calibration to ensure at least 3 skills are assigned to each position for accurate matching."
    elif "internal_positions_with_job_band" in rule_lower:
        return "Configure job bands in ijp_config and ensure positions have hiring_band populated in the ATS integration."
    elif "claimed_employee_profiles_with_levels" in rule_lower:
        return "Verify employee level data is synced from HRIS. Configure level mappings in ijp_config → job_bands."
    elif "claimed_employee_profiles_with_skills" in rule_lower:
        return "Encourage employees to add skills via Profile Assistant. Enable skill inference from job titles."
    elif "claimed_employee_profiles_open_to_mentor" in rule_lower:
        return "Enable mentorship in career_hub_base_config and encourage employees to opt-in as mentors."
    elif "projects_with_multiple_skills" in rule_lower:
        return "Add at least 3 skills to each project definition to improve matching accuracy."
    elif "projects_with_ideal_candidates" in rule_lower:
        return "Calibrate projects by adding at least 3 ideal candidates to guide employee recommendations."
    elif "projects_with_location" in rule_lower:
        return "Ensure all projects have a location assigned in the project definition."
    elif "courses_with_skills" in rule_lower:
        return "Map skills to courses during LMS sync or manually add skills to course records."
    elif "courses_with_description" in rule_lower:
        return "Ensure courses have descriptions of at least 50 words in the LMS for accurate recommendations."
    elif "role_levels" in rule_lower:
        return "Configure career_navigator_seniority_ordering in ijp_config with all role levels."
    elif "role_job_code" in rule_lower:
        return "Ensure job codes are synced from HRIS and mapped correctly in role_library_config."
    elif "role_lob" in rule_lower:
        return "Map business functions to roles in role_library_config or sync from HRIS."
    elif "role_skills" in rule_lower:
        return "Add at least 3 skills to each role in role_library_config for accurate skill gap analysis."
    elif "mentor_profiles_with_rich_data" in rule_lower:
        return "Encourage mentors to complete their profiles with skills, experience, and mentorship topics."
    
    # Security Rules
    elif "is_pcs_seo" in rule_lower:
        return "Disable SEO optimization for sandbox environments in pcsx_base_config → seo_config.enabled = false."
    elif "num_external_domains" in rule_lower:
        return "Review and reduce external domains in external_account_for_group_id config to 20 or fewer."
    elif "max_campaign" in rule_lower:
        return "Set max_per_campaign in campaign_config to 2000 or less."
    elif "email_loopback" in rule_lower:
        return "Configure email_loopback_gate: enable for sandbox, disable for production environments."
    elif "provision_user" in rule_lower:
        return "Enable user_provisioning_config to provision accounts only from Employee Sync data."
    elif "session_timeout" in rule_lower:
        return "Set custom_session_timeout_config to 24 hours or less for security compliance."
    elif "employee_profile_visibility" in rule_lower:
        return "Review profile_visibility settings in career_hub_base_config for unclaimed employee profiles."
    elif "sync_failure" in rule_lower:
        return "Investigate sync errors in Integration Console. Check API credentials and field mappings."
    elif "num_rejections" in rule_lower:
        return "Review recent rejection activity for anomalies. Check workflow automation rules."
    elif "application_failures" in rule_lower:
        return "Investigate application submission errors. Check ATS connectivity and field validation."
    elif "profile_data_retention" in rule_lower:
        return "Review data_retention_config rules and ensure proper purge schedules are configured."
    elif "unsubscribe" in rule_lower:
        return "Review unsubscribe volume and ensure email content meets compliance standards."
    elif "emails_sent_to_employees" in rule_lower:
        return "Configure email frequency limits in email_config to prevent over-messaging."
    elif "num_emails" in rule_lower:
        return "Monitor email volume and ensure campaign limits are properly configured."
    elif "num_admin" in rule_lower:
        return "Review admin accounts in Admin Console → Manage Users. Remove unnecessary admin access."
    elif "data_subject" in rule_lower:
        return "Process pending data subject requests and ensure GDPR/CCPA compliance workflows are active."
    
    # Analytics Rules - Employee
    elif "employee_level" in rule_lower:
        return "Ensure employee level field is mapped in HRIS integration. Check Employee Sync field mappings."
    elif "employee_location_country" in rule_lower:
        return "Map location_country field in HRIS integration. Verify country data is available."
    elif "employee_email" in rule_lower:
        return "Ensure employee email field is correctly mapped and populated in HRIS sync."
    elif "employee_is_alumni" in rule_lower:
        return "Verify termination_date is populated for all alumni employees in HRIS."
    elif "employee_first_name" in rule_lower:
        return "Ensure first_name field is mapped and populated in HRIS integration."
    elif "employee_last_name" in rule_lower:
        return "Ensure last_name field is mapped and populated in HRIS integration."
    elif "employee_hiring_date" in rule_lower:
        return "Map hire_date field in HRIS integration for accurate analytics."
    elif "employee_location" in rule_lower:
        return "Ensure location field is mapped in HRIS integration."
    elif "employee_manager_id" in rule_lower:
        return "Map manager_id field in HRIS integration. Required for org chart functionality."
    elif "employee_manager_email" in rule_lower:
        return "Map manager_email field in HRIS integration for reporting and notifications."
    elif "employee_division" in rule_lower:
        return "Map division/LOB field in HRIS integration for business unit analytics."
    elif "employee_internal_candidate" in rule_lower:
        return "Ensure employee records are linked to internal candidate profiles during sync."
    
    # Analytics Rules - Application/Position
    elif "application_funnel" in rule_lower:
        return "Review stage mappings in ats_config → stage_map. Ensure funnel progression is logical."
    elif "application_source_type" in rule_lower:
        return "Map source_type field in ATS integration for accurate source tracking."
    elif "stage_group" in rule_lower:
        return "Configure stage mappings in ats_config → stage_map or diversity_dashboard_config → application_stage_map."
    elif "stagemap" in rule_lower:
        return "Configure stage group mappings in ats_config → stage_map. Ensure all stages are mapped."
    elif "all_stage_transition" in rule_lower:
        return "Ensure all stages in stage_transition_map are also mapped in diversity_dashboard_config."
    elif "position_status" in rule_lower:
        return "Ensure position status field is mapped in ATS integration."
    elif "position_location" in rule_lower:
        return "Map position location_country field in ATS integration."
    elif "position_hiring_manager" in rule_lower:
        return "Map hiring manager fields in ATS integration via custom_fields_v2."
    elif "position_title" in rule_lower:
        return "Ensure position title field is mapped in ATS integration."
    elif "position_business" in rule_lower:
        return "Map business_unit field in ATS integration via custom_fields_v2."
    elif "position_job_function" in rule_lower:
        return "Map job_function field in ATS integration."
    elif "position_creation" in rule_lower:
        return "Ensure creation_ts field is captured during position sync."
    elif "recruiter_name" in rule_lower or "recruiter_email" in rule_lower:
        return "Map recruiter fields in ATS integration via custom_fields_v2."
    elif "rejection_reason" in rule_lower:
        return "Map rejection reason field in ATS integration via custom_fields_v2."
    elif "hired_ts" in rule_lower:
        return "Ensure hired_ts is populated when applications reach hired stage."
    elif "application_ts" in rule_lower:
        return "Verify application_ts is captured during application sync."
    elif "profile_id" in rule_lower:
        return "Ensure applications are linked to profile records during sync."
    elif "application_id" in rule_lower:
        return "Verify application_id is populated for all applications."
    elif "stage_ts" in rule_lower:
        return "Ensure stage_ts is captured for all stage transitions."
    elif "application_status" in rule_lower:
        return "Verify status field is populated for all applications."
    elif "internal_app_regex" in rule_lower:
        return "Configure internal_app_regex in ats_config to classify internal applications by source_type."
    elif "referral" in rule_lower:
        return "Configure referral_regex in ats_config to classify referral applications by source_type."
    elif "custom_fields_v2_position_is_open" in rule_lower:
        return "Map is_open field in custom_fields_v2 → position configuration."
    
    # TIP Rules
    elif "talent_lake" in rule_lower:
        return "Contact Eightfold support to provision Talent Lake for your instance."
    elif "data_retention_config" in rule_lower:
        return "Configure at least one data retention rule in data_retention_config for GDPR/CCPA compliance."
    elif "oauth" in rule_lower:
        return "Configure OAuth settings in integration_systems for supported ATS adaptors."
    elif "webhook" in rule_lower:
        return "Enable and configure webhook settings in integration_systems for real-time sync."
    elif "custom_fields_v2" in rule_lower:
        return "Configure field mappings in Integration Console → Field Mapping → custom_fields_v2."
    elif "raas" in rule_lower:
        return "Configure RAAS List Reports in Workday for the specified entity type."
    elif "job_posting_sites" in rule_lower:
        return "Configure job posting site IDs in enterprise_config for internal/external classification."
    elif "add_application_sources" in rule_lower:
        return "Configure application source mappings in integration_systems for correct source tagging."
    elif "career_site_source" in rule_lower:
        return "Set career_site_source_id in ATS config for SuccessFactors application writeback."
    elif "list_terminated" in rule_lower:
        return "Enable list_terminated_employees in SuccessFactors integration settings."
    elif "stage_advance_using_odata" in rule_lower:
        return "Enable stage_advance_using_odata for SuccessFactors OData API integration."
    elif "hide_skipped" in rule_lower:
        return "Enable hide_skipped_statuses_in_application_trail for cleaner SF application history."
    elif "questionnaire_raas" in rule_lower:
        return "Configure RAAS List Report for questionnaires in Workday for smart_apply or TA profile questions."
    elif "internal_to_external" in rule_lower:
        return "Enable internal to external candidate conversion in SuccessFactors. This requires SF admin configuration."
    elif "reply_to" in rule_lower:
        return "Update reply_to email in email_config from support@eightfold.ai to customer support email."
    
    # Default
    return f"Review the configuration settings for this rule in Admin Console or Integration Console."


def process_rules():
    """Process the 136 new rules and create output TSV."""
    input_file = '/home/ec2-user/de_app_1/documentation/new_rules_136_input.tsv'
    output_file = '/home/ec2-user/de_app_1/documentation/new_rules_136_with_enhanced_descriptions.tsv'
    
    rows = []
    
    # Known product areas to detect column structure
    KNOWN_PRODUCT_AREAS = {'AI', 'Security', 'Analytics', 'Talent Management - Core', 'TM Analytics', 'TA Analytics'}
    
    # Use csv reader with proper quoting to handle multiline fields
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = next(reader)
        
        for row in reader:
            if len(row) < 3:
                continue
            
            # Detect if column structure has Product Area or not
            # TIP rows: SKU | Rule Name | Rule ID | Config Ref | Description | ...
            # Other rows: SKU | Product Area | Rule Name | Rule ID | Config Ref | Description | ...
            
            col1 = row[0].strip() if len(row) > 0 else ""
            col2 = row[1].strip() if len(row) > 1 else ""
            col3 = row[2].strip() if len(row) > 2 else ""
            col4 = row[3].strip() if len(row) > 3 else ""
            
            # Check if col2 is a known product area or looks like a rule name
            if col2 in KNOWN_PRODUCT_AREAS or (col2 and not col2.startswith(('More than', 'Do not', 'Number of', 'Campaign', 'Email', 'Account', 'Session', 'Profile', 'Too many', 'Admin', 'Data', 'Funnel', 'Configure', 'ATS', 'Internal', 'Referral', 'Hired', 'Discrepancy', 'All', 'Application', 'Talent', 'oauth', 'Position', 'Candidate', 'Employee', 'Webhook', 'Custom', 'RAAS', 'internal', 'external', 'add_application', 'career_site', 'list_terminated', 'stage_advance', 'hide_skipped', 'Reply'))):
                # Standard format with Product Area
                sku = col1
                product_area = col2
                rule_name = col3
                rule_id = col4
                config_ref = row[4].strip() if len(row) > 4 else ""
                description = row[5].strip() if len(row) > 5 else ""
                current_feature_id = row[7].strip() if len(row) > 7 else ""
                current_feature_name = row[8].strip() if len(row) > 8 else ""
                action = row[9].strip() if len(row) > 9 else ""
                new_feature = row[10].strip() if len(row) > 10 else ""
                updates = row[11].strip() if len(row) > 11 else ""
            else:
                # TIP format without Product Area column
                sku = col1
                product_area = "Integrations" if "integrations" in str(row).lower() else "Platform"
                rule_name = col2
                rule_id = col3
                config_ref = col4
                description = row[4].strip() if len(row) > 4 else ""
                current_feature_id = row[6].strip() if len(row) > 6 else ""
                current_feature_name = row[7].strip() if len(row) > 7 else ""
                action = row[8].strip() if len(row) > 8 else ""
                new_feature = row[9].strip() if len(row) > 9 else ""
                updates = row[10].strip() if len(row) > 10 else ""
            
            # Skip rows without valid rule_id
            if not rule_id or rule_id == "#N/A":
                continue
            
            # Get or derive config reference
            if config_ref == "#N/A" or not config_ref:
                config_ref = get_config_reference(rule_id)
            
            # Generate enhanced description
            enhanced_desc = generate_enhanced_description(rule_id, rule_name, description, product_area)
            
            # Get code reference
            code_ref = get_code_reference(rule_id)
            
            rows.append({
                "sku": sku,
                "product_area": product_area,
                "rule_name": rule_name,
                "rule_id": rule_id,
                "config_reference": config_ref,
                "description": description,
                "cursor_description": enhanced_desc,
                "code_reference": code_ref,
                "current_feature_id": current_feature_id,
                "current_feature_name": current_feature_name,
                "action": action,
                "new_feature": new_feature,
                "updates": updates,
            })
    
    # Write output file
    output_headers = [
        "SKU",
        "Product Area",
        "Rule Name",
        "Rule ID",
        "Config Reference",
        "Original Description",
        "Cursor Generated Description",
        "Code Reference",
        "Current Feature ID",
        "Current Feature Name",
        "Action",
        "New Feature Alignment",
        "Updates to rule logic"
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(output_headers)
        
        for row in rows:
            writer.writerow([
                row["sku"],
                row["product_area"],
                row["rule_name"],
                row["rule_id"],
                row["config_reference"],
                row["description"],
                row["cursor_description"],
                row["code_reference"],
                row["current_feature_id"],
                row["current_feature_name"],
                row["action"],
                row["new_feature"],
                row["updates"],
            ])
    
    print(f"Created {output_file}")
    print(f"Total rules processed: {len(rows)}")
    
    # Count rules with config references
    with_config = sum(1 for r in rows if r["config_reference"].strip())
    with_desc = sum(1 for r in rows if "**Purpose:**" in r["cursor_description"])
    
    print(f"Rules with config references: {with_config}")
    print(f"Rules with enhanced descriptions: {with_desc}")
    
    return output_file


if __name__ == "__main__":
    process_rules()
