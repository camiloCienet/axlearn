import pandas as pd
from pandas import DataFrame
from typing import List
import glob
import os
import sys
import json

def process_and_write_to_json(name_folder: str, modes: List[str]):
    # Get the current working directory
    current_path = os.getcwd()

    # Join the current path with the folder name
    folder_path = os.path.join(current_path, name_folder)
    print(f"Current folder directory: {folder_path}")

    # Get a list of CSV file   cpu_tests_all_results.csv. Here is where all
    # tests are for cpu.
    all_files = glob.glob(os.path.join(folder_path,"csv_results", "cpu_tests_all_results.csv"))

    # List to hold all row dictionaries
    all_data = []
    output_filename = f'failed_tests_#{name_folder.split("#")[1]}.json'

    # Loop through the list of file paths
    for file_path in all_files:
        try:
            df = pd.read_csv(file_path)
            failed_ut_df = df[df["status"] == "failed"]

            # Iterate through each row and convert to a dictionary
            for _, row in failed_ut_df.iterrows():
                all_data.append(row.to_dict())
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if "excel" in modes:
      df_to_excel(failed_ut_df,folder_path, output_filename)

    total_failed_ut = {
        "total_failed_ut":len(all_data),
    }
    all_data.append(total_failed_ut)

    # Write all collected dictionaries to a single JSON file inside run_#xx/csv_results
    path_to_outpu_json = os.path.join(name_folder,output_filename)
    with open(path_to_outpu_json, 'w') as f:
        json.dump(all_data, f, indent=4)

def df_to_excel(df: DataFrame,path_folder,sheet_name: str):
  path_to_output_xlsx = os.path.join(path_folder,'axlearn-arc.xlsx')

  # Check if the file already exists
  writer_kwargs = {}
  if os.path.exists(path_to_output_xlsx):
      # Use append mode if the file exists
      mode = 'a'
      writer_kwargs = {'if_sheet_exists': 'replace'}
  else:
      # Use write mode if the file does not exist
      mode = 'w'

  with pd.ExcelWriter(path_to_output_xlsx, engine='openpyxl', mode=mode, **writer_kwargs) as writer:
      df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a folder name as a command-line argument.")
        sys.exit(1)

    name_folder = sys.argv[1]
    process_and_write_to_json(name_folder,modes=["excel"])
