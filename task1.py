import os
import pandas as pd
import jsonlines

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

        df = pd.DataFrame(data)

        combined_data = pd.concat([combined_data, df], ignore_index=True)

# Filter the combined DataFrame for English data
english_data = combined_data[combined_data['locale'] == 'en-US']

# Iterate through unique locales (languages) other than English
unique_locales = combined_data['locale'].unique()
unique_locales = unique_locales[unique_locales != 'en-US']  # Exclude English

for locale in unique_locales:
    # Filter data for the current language
    language_data = combined_data[combined_data['locale'] == locale]

    # Merge with the English data using 'id' as the key
    merged_data = english_data[['id', 'utt', 'annot_utt']].merge(
        language_data[['id', 'utt', 'annot_utt']], on='id', suffixes=('_en', f'_{locale}')
    )

    # Create an Excel writer for the output file in the specified directory
    output_filename = os.path.join('Compiled_data', f'en-{locale}.xlsx')
    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        # Write the merged_data DataFrame to the Excel file
        merged_data.to_excel(writer, sheet_name=f'{locale}', index=False)