#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Complex Card Matching Task
# Copyright (C) 2025  Giovanna Del Sordo
# Licensed under the GNU General Public License v3.0 or later.
# See the LICENSE file or <https://github.com/giovannacdelsordo/Complex-Card-Matching-Task/blob/faf3ffe3f0b5109642ff9f68b086cc10bc26339c/LICENSE> for details.


# In[1]:


## Preprocess each individual BEHAVIORAL data file to create the "State" column


# In[ ]:


import pandas as pd
import os

# Path to the folder containing participant files
folder_path = ""

# Directory where you want to save the updated files
output_directory = ''

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Function to process each CSV file and apply rules
def process_csv_file(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Initialize the "State" column
    df["State"] = "None"

    # Group the data by difficulty and blockNumber
    grouped = df.groupby(["difficulty", "blockNumber"])

    # Process each group
    for (difficulty, blockNumber), group_indices in grouped.groups.items():
        group = df.loc[group_indices]  # Select the group by indices

        # Sort group by trialNumber
        group = group.sort_values("trialNumber")

        # Apply rules to the "State" column
        for i, row in group.iterrows():
            if row["trialNumber"] == 1:
                df.at[i, "State"] = "T1"
            elif row["trialNumber"] == 2:
                df.at[i, "State"] = (
                    "Exploitation"
                    if group["accuracy"].iloc[0:3].sum() == 3
                    else "Exploration"
                )
            elif row["trialNumber"] == 3:
                df.at[i, "State"] = (
                    "Exploitation"
                    if group["accuracy"].iloc[0:3].sum() == 3
                    or group["accuracy"].iloc[1:4].sum() == 3
                    else "Exploration"
                )
            elif 4 <= row["trialNumber"] <= 8:
                idx = row["trialNumber"] - 1
                df.at[i, "State"] = (
                    "Exploitation"
                    if (
                        group["accuracy"].iloc[idx - 2 : idx + 1].sum() == 3
                        or group["accuracy"].iloc[idx - 1 : idx + 2].sum() == 3
                        or group["accuracy"].iloc[idx : idx + 3].sum() == 3
                        or group["accuracy"].iloc[idx - 2 : idx + 3].sum() == 4
                    )
                    else "Exploration"
                )
            elif row["trialNumber"] == 9:
                df.at[i, "State"] = (
                    "Exploitation"
                    if (
                        group["accuracy"].iloc[6:9].sum() == 3
                        or group["accuracy"].iloc[7:10].sum() == 3
                        or group["accuracy"].iloc[5:10].sum() == 4
                    )
                    else "Exploration"
                )
            elif row["trialNumber"] == 10:
                df.at[i, "State"] = (
                    "Exploitation" if group["accuracy"].iloc[7:10].sum() == 3 else "Exploration"
                )

    # Return the processed DataFrame with the original row order preserved
    return df

# Iterate over each CSV file, process, and save updated file
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        # Process the CSV file
        processed_data = process_csv_file(file_path)
        # Save the updated DataFrame to a new CSV in the output directory
        output_file = os.path.join(output_directory, filename)
        processed_data.to_csv(output_file, index=False)

print(f"Updated files have been saved to {output_directory}")


# In[ ]:


## Transfer the "State" column to the pupillometry data files


# In[ ]:


import os
import re
import pandas as pd

# Paths
csv_folder_path = ""
excel_folder_path = ""
output_excel_folder = ""

# Create the output directory if it doesn't exist
os.makedirs(output_excel_folder, exist_ok=True)

# Function to extract subject number using regex
def extract_subject_number(filename):
    match = re.search(r'\d+', filename)
    return match.group() if match else None

# Function to update Excel files with State data from CSV
def update_excel_file(csv_df, excel_file_path, output_path):
    try:
        # Load the Excel file
        excel_data = pd.ExcelFile(excel_file_path, engine="openpyxl")  # Ensure correct engine
        updated_sheets = {}

        # Loop through each sheet in the Excel file
        for sheet_name in excel_data.sheet_names:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

            # Check if required columns exist
            if {"difficulty", "blockNumber", "trialNumber"}.issubset(df.columns):
                if "State" not in df.columns:
                    df["State"] = None

                for _, csv_row in csv_df.iterrows():
                    difficulty = csv_row["difficulty"]
                    block_number = csv_row["blockNumber"]
                    trial_number = csv_row["trialNumber"]
                    state = csv_row["State"]

                    matching_rows = (
                        (df["difficulty"] == difficulty) &
                        (df["blockNumber"] == block_number) &
                        (df["trialNumber"] == trial_number)
                    )

                    df.loc[matching_rows, "State"] = state

            updated_sheets[sheet_name] = df

        # Save the updated Excel file in valid `.xlsx` format
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet_name, updated_df in updated_sheets.items():
                updated_df.to_excel(writer, index=False, sheet_name=sheet_name)

    except Exception as e:
        print(f"Error updating Excel file {excel_file_path}: {e}")

# Process each CSV file
for csv_filename in os.listdir(csv_folder_path):
    if csv_filename.endswith(".csv"):
        try:
            # Read the processed CSV file
            csv_path = os.path.join(csv_folder_path, csv_filename)
            csv_df = pd.read_csv(csv_path)

            # Extract subject number from the CSV filename
            csv_subject_number = extract_subject_number(csv_filename)
            if not csv_subject_number:
                print(f"Unable to extract subject number from CSV filename: {csv_filename}")
                continue

            # Find the corresponding Excel file
            matching_excel_file = None
            for excel_filename in os.listdir(excel_folder_path):
                excel_subject_number = extract_subject_number(excel_filename)
                if csv_subject_number == excel_subject_number:
                    matching_excel_file = excel_filename
                    break

            if matching_excel_file:
                excel_path = os.path.join(excel_folder_path, matching_excel_file)
                output_excel_path = os.path.join(output_excel_folder, matching_excel_file)

                # Update the Excel file
                update_excel_file(csv_df, excel_path, output_excel_path)
            else:
                print(f"No matching Excel file found for subject number {csv_subject_number}")
        except Exception as e:
            print(f"Error processing CSV file {csv_filename}: {e}")

print(f"Updated Excel files have been saved to {output_excel_folder}")

