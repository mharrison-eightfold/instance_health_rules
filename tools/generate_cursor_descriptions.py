#!/usr/bin/env python3
"""
Generate Cursor Descriptions for Instance Health Rules
=======================================================
This script processes the Instance Health Rules TSV and adds a 
"Cursor Generated Description" column with standardized Purpose/Impact format.
"""

import csv
import re
import sys

# Input data - paste the TSV content or read from file
INPUT_FILE = '/home/ec2-user/de_app_1/documentation/instance_health_rules_input.tsv'
OUTPUT_FILE = '/home/ec2-user/de_app_1/documentation/PCS_TM_TA_rules_with_cursor_descriptions.tsv'


def clean_html(text):
    """Remove HTML tags from text"""
    if not text:
        return ""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Clean up whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def extract_purpose_impact(description):
    """Extract or infer purpose and impact from existing description"""
    if not description:
        return None, None
    
    desc = clean_html(description)
    
    # Check if already has [Purpose] format
    purpose_match = re.search(r'\[Purpose\]\s*(.+?)(?:\[Impact\]|Impact of Failure|$)', desc, re.IGNORECASE | re.DOTALL)
    impact_match = re.search(r'(?:\[Impact\]|Impact of Failure)\s*(.+?)$', desc, re.IGNORECASE | re.DOTALL)
    
    if purpose_match:
        purpose = purpose_match.group(1).strip()
    else:
        # Try to extract purpose from description before "Impact"
        parts = re.split(r'Impact of Failure|If not configured|Without this|If missing|If not enabled', desc, maxsplit=1, flags=re.IGNORECASE)
        purpose = parts[0].strip() if parts else desc
    
    if impact_match:
        impact = impact_match.group(1).strip()
    else:
        # Try to extract impact
        impact_patterns = [
            r'Impact of Failure\s*(.+?)$',
            r'If not configured,?\s*(.+?)$',
            r'Without this.*?,?\s*(.+?)$',
            r'If missing,?\s*(.+?)$',
            r'If not enabled,?\s*(.+?)$',
            r'Missing.*?can\s*(.+?)$',
        ]
        impact = None
        for pattern in impact_patterns:
            match = re.search(pattern, desc, re.IGNORECASE | re.DOTALL)
            if match:
                impact = match.group(1).strip()
                break
    
    return purpose, impact


def generate_cursor_description(row):
    """Generate a standardized Purpose/Impact description for a rule"""
    rule_name = row.get('Rule Name', '')
    rule_id = row.get('Rule ID', '')
    description = row.get('Description', '')
    product_area = row.get('Product Area', '')
    feature_alignment = row.get('Feature Alignment', '')
    updated_desc = row.get('Updated Description (If needed)', '')
    
    # Use updated description if available
    source_desc = updated_desc if updated_desc and updated_desc.strip() and updated_desc.strip() != 'NA' else description
    
    if not source_desc or source_desc.strip() == '':
        return f"**Purpose:** Validates that {rule_name} is properly configured in the system. **Impact:** If this rule fails, the related functionality may not work as expected, potentially affecting user experience and system operations."
    
    purpose, impact = extract_purpose_impact(source_desc)
    
    # Clean up purpose
    if purpose:
        purpose = purpose.strip()
        # Remove leading punctuation
        purpose = re.sub(r'^[\s\.\,\:\;]+', '', purpose)
        # Capitalize first letter
        if purpose:
            purpose = purpose[0].upper() + purpose[1:] if len(purpose) > 1 else purpose.upper()
    
    # Clean up impact
    if impact:
        impact = impact.strip()
        impact = re.sub(r'^[\s\.\,\:\;]+', '', impact)
        if impact:
            impact = impact[0].upper() + impact[1:] if len(impact) > 1 else impact.upper()
    
    # Generate fallback descriptions if needed
    if not purpose or len(purpose) < 20:
        purpose = f"Validates that {rule_name} is properly configured for {product_area or 'the system'}."
    
    if not impact or len(impact) < 20:
        impact = f"If this rule fails, {rule_name.lower()} functionality may not work correctly, potentially affecting dependent features and user workflows."
    
    # Ensure proper ending punctuation
    if purpose and not purpose.endswith('.'):
        purpose += '.'
    if impact and not impact.endswith('.'):
        impact += '.'
    
    return f"**Purpose:** {purpose} **Impact:** {impact}"


def process_tsv(input_file, output_file):
    """Process the TSV file and add Cursor Generated Description column"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        # Read all content
        content = f.read()
    
    # Split into lines
    lines = content.strip().split('\n')
    
    if not lines:
        print("Error: No data found in input file")
        return
    
    # Find the actual header row (the one with SKU, Product Area, etc.)
    header_row_idx = 0
    header = None
    for i, line in enumerate(lines):
        cols = line.split('\t')
        if 'SKU' in cols or 'Product Area' in cols[:5]:
            header_row_idx = i
            header = cols
            break
    
    if header is None:
        # Try to find Description column in any row
        for i, line in enumerate(lines):
            cols = line.split('\t')
            for col in cols:
                if col.strip() == 'Description':
                    header_row_idx = i
                    header = cols
                    break
            if header:
                break
    
    if header is None:
        print("Error: Could not find header row")
        return
    
    print(f"Found header at row {header_row_idx}")
    print(f"Found {len(header)} columns in header")
    print(f"Header: {header[:10]}...")  # Print first 10 columns
    
    # Find Description column index
    desc_index = -1
    for i, col in enumerate(header):
        if 'Description' in col and 'Updated' not in col and 'Cursor' not in col:
            desc_index = i
            break
    
    if desc_index == -1:
        print("Error: Could not find Description column")
        print(f"Columns: {header}")
        return
    
    print(f"Description column found at index {desc_index}")
    
    # Create new header with Cursor Generated Description after Description
    new_header = header[:desc_index+1] + ['Cursor Generated Description'] + header[desc_index+1:]
    
    # Process data rows
    output_rows = [new_header]
    rules_processed = 0
    
    # Start processing from the row after the header
    for line_num, line in enumerate(lines[header_row_idx+1:], start=header_row_idx+2):
        if not line.strip():
            continue
        
        cols = line.split('\t')
        
        # Skip empty rows or rows that are just tabs
        if len(cols) < 3 or not any(c.strip() for c in cols[:5]):
            continue
        
        # Pad columns if needed
        while len(cols) < len(header):
            cols.append('')
        
        # Create row dict for easier access
        row = {header[i]: cols[i] if i < len(cols) else '' for i in range(len(header))}
        
        # Generate cursor description
        cursor_desc = generate_cursor_description(row)
        
        # Create new row with cursor description inserted
        new_row = cols[:desc_index+1] + [cursor_desc] + cols[desc_index+1:]
        output_rows.append(new_row)
        rules_processed += 1
    
    print(f"Processed {rules_processed} rules")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in output_rows:
            writer.writerow(row)
    
    print(f"Output written to {output_file}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        INPUT_FILE = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_FILE = sys.argv[2]
    
    process_tsv(INPUT_FILE, OUTPUT_FILE)
