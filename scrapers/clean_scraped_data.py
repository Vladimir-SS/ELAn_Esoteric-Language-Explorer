import json

def clean_year(year):
    if year and isinstance(year, str):
        if 'unknown' in year.lower():
            return None  # Set to None if 'unknown'
        if '-' in year: # some languages have a range of years (e.g., '2023-2024')
            return year.split('-')[0]
    return year

def clean_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for language in data:
        if 'YearCreated' in language:
            language['YearCreated'] = clean_year(language['YearCreated'])

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data cleaned and saved to '{output_file}'.")

input_file = 'data/esolangs-data.json'
output_file = 'data/esolangs-cleaned.json'
clean_data(input_file, output_file)