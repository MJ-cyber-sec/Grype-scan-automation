import json

import csv

import argparse

import sys

from pathlib import Path



def extract_vulnerabilities_to_csv(json_file, csv_file):

    """

    Extract vulnerabilities and remediation suggestions from Grype JSON output to CSV.

    

    Args:

        json_file: Path to the input JSON file

        csv_file: Path to the output CSV file

    """

    

    # Load JSON data

    with open(json_file, 'r') as f:

        data = json.load(f)

    

    # Prepare CSV data

    rows = []

    

    for match in data.get('matches', []):

        vulnerability = match.get('vulnerability', {})

        artifact = match.get('artifact', {})

        fix = vulnerability.get('fix', {})

        

        # Extract vulnerability details

        vuln_id = vulnerability.get('id', 'N/A')

        vuln_description = vulnerability.get('description', 'N/A')

        severity = vulnerability.get('severity', 'N/A')

        data_source = vulnerability.get('dataSource', 'N/A')

        namespace = vulnerability.get('namespace', 'N/A')

        

        # Extract artifact details

        artifact_name = artifact.get('name', 'N/A')

        artifact_version = artifact.get('version', 'N/A')

        artifact_type = artifact.get('type', 'N/A')

        purl = artifact.get('purl', 'N/A')

        

        # Extract remediation information

        fix_state = fix.get('state', 'N/A')

        fix_versions = fix.get('versions', [])

        fix_advisory = fix.get('advisory', 'N/A')

        

        # Handle fix versions

        fix_versions_str = ', '.join(fix_versions) if fix_versions else 'N/A'

        

        # Extract URLs for reference

        urls = vulnerability.get('urls', [])

        urls_str = '; '.join(urls[:3]) if urls else 'N/A'  # Limit to first 3 URLs

        

        row = {

            'Vulnerability ID': vuln_id,

            'Severity': severity,

            'Description': vuln_description,

            'Affected Package': artifact_name,

            'Package Version': artifact_version,

            'Package Type': artifact_type,

            'Package URL': purl,

            'Data Source': data_source,

            'Namespace': namespace,

            'Fix State': fix_state,

            'Fixed in Versions': fix_versions_str,

            'Fix Advisory': fix_advisory,

            'Reference URLs': urls_str,

        }

        

        rows.append(row)

    

    # Sort by severity and vulnerability ID for better readability

    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

    rows.sort(key=lambda x: (

        severity_order.get(x['Severity'], 99),

        x['Vulnerability ID']

    ))

    

    # Write to CSV

    if rows:

        fieldnames = rows[0].keys()

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerows(rows)

        

        print(f"âœ“ Successfully extracted {len(rows)} vulnerabilities to {csv_file}")

        return len(rows)

    else:

        print("No vulnerabilities found in the JSON file.")

        return 0





def main():

    parser = argparse.ArgumentParser(

        description='Extract vulnerabilities from Grype JSON files to CSV',

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog='''

Examples:

  python main.py --path /path/to/json/files

  python main.py --path . --output /custom/csv/output

  python main.py -p ./scans

        '''

    )

    

    parser.add_argument(

        '--path', '-p',

        type=str,

        required=True,

        help='Path to directory containing JSON files from Grype scans'

    )

    

    parser.add_argument(

        '--output', '-o',

        type=str,

        default='csv_result',

        help='Output directory for CSV files (default: csv_result)'

    )

    

    args = parser.parse_args()

    

    # Convert to Path objects

    json_path = Path(args.path)

    output_dir = Path(args.output)

    

    # Validate input path exists

    if not json_path.exists():

        print(f"âŒ Error: Path '{json_path}' not found.", file=sys.stderr)

        sys.exit(1)

    

    if not json_path.is_dir():

        print(f"âŒ Error: '{json_path}' is not a directory.", file=sys.stderr)

        sys.exit(1)

    

    # Create output directory if it doesn't exist

    try:

        output_dir.mkdir(parents=True, exist_ok=True)

    except Exception as e:

        print(f"âŒ Error creating output directory: {str(e)}", file=sys.stderr)

        sys.exit(1)

    

    # Find all JSON files in the directory

    json_files = list(json_path.glob('*.json'))

    

    if not json_files:

        print(f"âš ï¸  No JSON files found in '{json_path}'", file=sys.stderr)

        sys.exit(0)

    

    print(f"Found {len(json_files)} JSON file(s) to process...")

    

    total_vulnerabilities = 0

    successful_files = 0

    failed_files = 0

    

    try:

        for json_file in sorted(json_files):

            try:

                # Generate output CSV filename

                csv_output = output_dir / json_file.stem

                csv_output = csv_output.with_suffix('.csv')

                

                # Extract vulnerabilities

                count = extract_vulnerabilities_to_csv(json_file, csv_output)

                total_vulnerabilities += count

                successful_files += 1

            except Exception as e:

                print(f"âŒ Error processing {json_file.name}: {str(e)}", file=sys.stderr)

                failed_files += 1

        

        # Print summary

        print(f"\n{'='*60}")

        print(f"Processing Summary:")

        print(f"  Total files processed: {successful_files} successful, {failed_files} failed")

        print(f"  Total vulnerabilities extracted: {total_vulnerabilities}")

        print(f"  Output directory: {output_dir.absolute()}")

        print(f"{'='*60}")

        

        sys.exit(0 if failed_files == 0 else 1)

    except Exception as e:

        print(f"âŒ Error: {str(e)}", file=sys.stderr)

        sys.exit(1)





if __name__ == '__main__':

    main()
