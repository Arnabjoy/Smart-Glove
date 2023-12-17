import os
import pandas as pd

# List of directories
directories = ["Training_set/2", "Training_set/3",
               "Training_set/4", "Training_set/5"]  # include the dataset that needs to be combined in training

# List of letters
letters = ["Not_wearing_glove", "wore_glove", "letter_A", "letter_C", "Number_9", "letter_I", "letter_M", "Number_10",
           "letter_X", "letter_Y"]

# Output directory for combined files
output_directory = "Training_set/combined_data"

# Creating the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Looping through each gesture
for letter in letters:
    # List to store dataframes for each directory
    dataframes = []

    # Loop through directories
    for directory in directories:
        file_path = os.path.join(directory, f"{letter}.csv")

        # Check if the file exists in the directory
        if os.path.exists(file_path):
            # Read the CSV file into a dataframe
            df = pd.read_csv(file_path)

            # Append the dataframe to the list
            dataframes.append(df)

    # Combine all dataframes into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the combined dataframe to a new CSV file in the output directory
    combined_file_path = os.path.join(output_directory, f"{letter}.csv")
    combined_df.to_csv(combined_file_path, index=False)

    print(f"Combined data for {letter} saved to {combined_file_path}")
