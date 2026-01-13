#!/usr/bin/env python3
"""
Apply refinements to rule descriptions based on codebase verification.
"""

import pandas as pd
import os

# Path to the TSV file
INPUT_FILE = '/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv'
OUTPUT_FILE = '/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv'

# Refinements based on codebase review
REFINEMENTS = {
    'profile_skills_quality': {
        'purpose': 'Checks whether at least 75% of CANDIDATE profiles (not employee profiles) have at least one skill added, ensuring profiles are enriched for recommendations and skill-based workflows in Talent Acquisition.',
        'impact': 'Insufficient skills on profiles will reduce the effectiveness of candidate recommendations, matching accuracy, and insights across TA modules.'
    },
    'valid_manager_email': {
        'purpose': 'Checks whether most employees have a manager email assigned (presence check). A valid manager email must match the email of an existing employee profile. Note: This checks for presence, not email format validity.',
        'impact': 'If manager emails are missing or don\'t match existing employee profiles, org charts may be incomplete, and features relying on manager-based permissions (approvals, insights) may not function correctly.'
    },
    'employee_thin_profile_quality': {
        'purpose': 'Ensures at least 95% of employees have enriched (non-thin) profiles with sufficient data for accurate matching, recommendations, and workforce insights.',
        'impact': 'A high percentage of thin profiles limits the effectiveness of Talent Management features, reduces the quality of recommendations, and impacts analytics and reporting accuracy.'
    },
    'recruiter_missing_communication_email': {
        'purpose': 'Validates that all users with the PERM_SEND_MESSAGES role permission have a properly configured communication email. It checks each user for a designated communication email and verifies that the address is authorized for use.',
        'impact': 'Users without properly configured communication emails will be unable to send messages to candidates, disrupting recruiter outreach and communication workflows.'
    }
}

def apply_refinements():
    """Apply refinements to the TSV file."""
    # Read the TSV file
    df = pd.read_csv(INPUT_FILE, sep='\t', dtype=str)
    
    # Find the Rule ID and Cursor Generated Description columns
    rule_id_col = None
    cursor_desc_col = None
    
    for col in df.columns:
        if 'Rule ID' in col:
            rule_id_col = col
        if 'Cursor Generated Description' in col:
            cursor_desc_col = col
    
    if not rule_id_col or not cursor_desc_col:
        print(f"Could not find required columns. Found: {df.columns.tolist()}")
        return
    
    print(f"Found columns: Rule ID='{rule_id_col}', Cursor Desc='{cursor_desc_col}'")
    
    # Apply refinements
    updated_count = 0
    for idx, row in df.iterrows():
        rule_id = str(row[rule_id_col]).strip() if pd.notna(row[rule_id_col]) else ''
        
        if rule_id in REFINEMENTS:
            refinement = REFINEMENTS[rule_id]
            new_desc = f"**Purpose:** {refinement['purpose']} **Impact:** {refinement['impact']}"
            df.at[idx, cursor_desc_col] = new_desc
            print(f"Updated: {rule_id}")
            updated_count += 1
    
    # Save the updated TSV
    df.to_csv(OUTPUT_FILE, sep='\t', index=False)
    print(f"\nApplied {updated_count} refinements to {OUTPUT_FILE}")

if __name__ == '__main__':
    apply_refinements()
