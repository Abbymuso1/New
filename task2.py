import os
import pandas as pd
import jsonlines
from sklearn.model_selection import train_test_split

# Define the folder where your JSONL files are located
data_folder = 'data'

# Initialize an empty DataFrame to store the combined data for all languages
combined_data = pd.DataFrame(columns=['id', 'locale', 'utt', 'annot_utt'])

# Iterate through all files in the folder
for filename in os.listdir(data_folder):
    if filename.endswith('.jsonl'):
        file_path = os.path.join(data_folder, filename)

        # Open and read the JSONL file
        with open(file_path, 'r') as jsonl_file:
            data = list(jsonlines.Reader(jsonl_file))

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)

        # Append the data to the combined DataFrame
        combined_data = pd.concat([combined_data, df], ignore_index=True)

# Define the languages for which you want to generate JSONL files
languages = ['en-US', 'sw-KE', 'de-DE']
splits = ['train', 'test', 'dev']

# Iterate through languages and splits to generate JSONL files
for language in languages:
    for split in splits:
        # Filter data for the current language
        filtered_data = combined_data[combined_data['locale'] == language]

        # Split the data into train, test, and dev
        train_data, test_dev_data = train_test_split(filtered_data, test_size=0.4, random_state=42)
        test_data, dev_data = train_test_split(test_dev_data, test_size=0.5, random_state=42)

        if split == 'train':
            split_data = train_data
        elif split == 'test':
            split_data = test_data
        else:
            split_data = dev_data

        # Define the output JSONL filename
        output_filename = os.path.join('Split_data', f'{language}-{split}.jsonl')

        # output_filename = f'{language}-{split}.jsonl'

        # Write the split data to the output JSONL file
        with open(output_filename, 'w', newline='', encoding='utf-8') as jsonl_file:
            jsonlines.Writer(jsonl_file).write_all(split_data.to_dict(orient='records'))