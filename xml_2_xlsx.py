import xml.etree.ElementTree as ET
import pandas as pd
import os

# --- Configuration (Hardcoded for Simplicity) ---
XML_INPUT_FILE = 'testing.xml'
EXCEL_OUTPUT_FILE = 'pytest_report.xlsx'

def main():
    """Reads a JUnit XML file and converts the test results to an Excel file."""
    data = []

    print(f"Starting XML to XLSX conversion...")

    # 1. Read and Parse the XML File
    try:
        tree = ET.parse(XML_INPUT_FILE)
        root = tree.getroot()
    except Exception as e:
        # Combined FileNotFoundError and ParseError handling for simplicity
        print(f"Error processing '{XML_INPUT_FILE}': {e}.")
        return

    # 2. Extract Test Case Data
    # Iterate through all testsuite and testcase elements
    for testsuite in root.findall('.//testsuite'):
        for testcase in testsuite.findall('testcase'):

            # Simplified status determination
            status = 'passed'
            log_detail = ''

            # Check for failure, error, or skip tags and set status/log
            for tag in ['failure', 'error', 'skipped']:
                element = testcase.find(tag)
                if element is not None:
                    status = tag  # Status is the tag name itself (e.g., 'failure')
                    log_detail = element.text.strip() if element.text else ''
                    break

            # Collect details
            data.append({
                'test_name': testcase.get('name', 'N/A'),
                'class_name': testcase.get('classname', 'N/A'),
                'time_sec': float(testcase.get('time', '0')), # Convert time to float immediately
                'status': status,
                'log': log_detail,
            })

    if not data:
        print("No test case data found in the XML report.")
        return

    # 3. Create DataFrame and Write to Excel (XLSX)
    try:
        df = pd.DataFrame(data)
        # Use openpyxl engine to write .xlsx file
        df.to_excel(EXCEL_OUTPUT_FILE, sheet_name='Pytest Results', index=False, engine='openpyxl')
        print(f'SUCCESS: Excel report created at {EXCEL_OUTPUT_FILE}')
    except Exception as e:
        print(f"Error writing Excel file: {e}. Ensure 'pandas' and 'openpyxl' are installed.")

if __name__ == '__main__':
    main()
