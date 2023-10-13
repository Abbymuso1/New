import os
import pandas as pd
import jsonlines
import json

# Define the folder where your JSONL files are located
data_folder = 'Split_data'

# Initialize an empty DataFrame to store the combined data for all languages
combined_data = pd.DataFrame(columns=['id', 'locale', 'utt', 'annot_utt'])

# Initialize dictionaries to store translations for each language
translations = {}

# Iterate through all files in the folder
for filename in os.listdir(data_folder):
    if filename.endswith('.jsonl'):
        file_path = os.path.join(data_folder, filename)

        # Check if the filename indicates a training set by searching for 'train'
        if 'train' in filename:
            # Determine the target language (xx) based on the filename
            target_language = filename.split('-train')[0]

            # Open and read the JSONL file
            with open(file_path, 'r') as jsonl_file:
                data = list(jsonlines.Reader(jsonl_file))

            # Convert the data into a DataFrame
            df = pd.DataFrame(data)

            # Append the data to the combined DataFrame
            combined_data = pd.concat([combined_data, df], ignore_index=True)

            # Create translations from the target language (xx) to English (en)
            if target_language != 'en-US':
                target_data = df[df['locale'] == target_language]
                if not target_data.empty:
                    if target_language not in translations:
                        translations[target_language] = {}
                    for _, row in target_data.iterrows():
                        translations[target_language][row['id']] = {
                            'id': row['id'],
                            'utt': row['utt']
                        }

# Combine translations into a single dictionary with English (en) as the base language
en_translations = {}
for _, row in combined_data[combined_data['locale'] == 'en-US'].iterrows():
    en_translations[row['id']] = {
        'id': row['id'],
        'utt': row['utt']
    }

# Include Swahili (sw) and German (de) translations in the combined translations
if 'sw-KE' in translations and 'de-DE' in translations:
    for id, en_translation in en_translations.items():
        if id in translations['sw-KE'] and id in translations['de-DE']:
            translations['sw-KE'][id]['en-US'] = en_translation
            translations['de-DE'][id]['en-US'] = en_translation

# Create a JSON file with the combined translations
with open('combined_translations.json', 'w', encoding='utf-8') as json_file:
    json.dump(translations, json_file, ensure_ascii=False, indent=4)