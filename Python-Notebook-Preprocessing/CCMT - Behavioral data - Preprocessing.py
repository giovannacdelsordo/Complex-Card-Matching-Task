#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Complex Card Matching Task
# Copyright (C) 2025  Giovanna Del Sordo
# Licensed under the GNU General Public License v3.0 or later.
# See the LICENSE file or <https://github.com/giovannacdelsordo/Complex-Card-Matching-Task/blob/faf3ffe3f0b5109642ff9f68b086cc10bc26339c/LICENSE> for details.


# In[ ]:


## Classify exploration and exploitation trials AND save all participant data as a single Excel file


# In[ ]:


import pandas as pd
import os
import numpy as np

# Path to the folder containing participant files
folder_path = ""

# Directory where you want to save the Excel file
output_directory = ""

# Function to extract subject number from filename
def extract_subject_number(filename):
    # Extract digits from filename
    subject_number = ''.join(filter(str.isdigit, filename))
    return subject_number

# Function to process each CSV file
def process_csv_file(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Initialize column "State"
    df["State"] = "None"
    
    # Extract subject number from filename
    subject_number = extract_subject_number(os.path.basename(file_path))
    
    # Add subject number as a new column
    df.insert(0, "SubjectNumber", subject_number)
    
    # Organize dataset by difficulty and block number
    difficulties = df["difficulty"].unique()
    all_blocks_df = pd.DataFrame()  # Initialize an empty DataFrame to store all blocks

    for d in difficulties:
        df_d = df.loc[df["difficulty"] == d]
        blocksNumbers = df_d["blockNumber"].unique()
        for b in blocksNumbers:
            df_b = df_d.loc[df_d["blockNumber"] == b].copy()  # Create a copy of the DataFrame
            df_b.reset_index(inplace=True)
            ## COLUMN STATE
            # Set first line of each block as Exploration
            df_b.at[0, "State"] = "T1"
            # Second line
            df_b.at[1, "State"] = "Exploitation" if df_b["accuracy"].loc[1:3].sum() == 3 else "Exploration"
            # Third line
            df_b.at[2, "State"] = "Exploitation" if df_b["accuracy"].loc[1:3].sum() == 3 or df_b["accuracy"].loc[2:4].sum() == 3 else "Exploration"
            # Fourth to eighth lines
            for i in range(3, 8):
                df_b.at[i, "State"] = "Exploitation" if (
                    df_b["accuracy"].loc[i-2:i].sum() == 3 or
                    df_b["accuracy"].loc[i-1:i+1].sum() == 3 or
                    df_b["accuracy"].loc[i:i+2].sum() == 3 or
                    df_b["accuracy"].loc[i-2:i+2].sum() == 4
                ) else "Exploration"
            # Ninth line
            df_b.at[8, "State"] = "Exploitation" if (
                df_b["accuracy"].loc[6:8].sum() == 3 or
                df_b["accuracy"].loc[7:9].sum() == 3 or
                df_b["accuracy"].loc[5:9].sum() == 4 or 
                df_b["accuracy"].loc[8:9].sum() == 2
            ) else "Exploration"
            # Tenth line
            df_b.at[9, "State"] = "Exploitation" if df_b["accuracy"].loc[7:9].sum() == 3 else "Exploration"

            # Concatenate df_b to the all_blocks_df
            all_blocks_df = pd.concat([all_blocks_df, df_b], ignore_index=True)

    # Return the processed DataFrame
    return all_blocks_df

# Initialize an empty list to store DataFrames for each file
all_processed_data = []

# Iterate over each file in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        # Process the CSV file and append the result to the list
        processed_data = process_csv_file(file_path)
        all_processed_data.append(processed_data)

# Concatenate all processed DataFrames into a single DataFrame
final_dataframe = pd.concat(all_processed_data, ignore_index=True)

# Path to save the final Excel file
output_file = os.path.join(output_directory, 'processed_behavioral.xlsx')

# Export the final DataFrame to the specified Excel file
final_dataframe.to_excel(output_file, index=False)

print(f"Processed data has been saved to {output_file}")


# In[ ]:


# Classify trials as exploration or exploitation AND save updated files individually


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

