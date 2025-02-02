import json

PARADIGM_REPLACEMENTS = {
    "particle-automat": "particle-automaton",
    "object-oriented": "object-oriented",
    "multip": "multi-paradigm"
}

COMPUTATIONAL_CLASS_REPLACEMENTS = {
    "turing-complete": "turing-complete",
    "linear-bounded-automat": "linear-bounded-automaton",
    "finite-state-automat": "finite-state-automaton",
    "turing-tarpit": "turing-tarpit",
    "pushdown-automat": "push-down-automaton",
    "push-down-automat": "push-down-automaton"
}

def clean_paradigms(paradigms):
    flattened_paradigms = []

    for paradigm in paradigms:
        flattened_paradigms.extend(paradigm.split(":"))

    cleaned_paradigms = []

    for paradigm in flattened_paradigms:
        paradigm = paradigm.strip("\"")

        for pattern, correct_version in PARADIGM_REPLACEMENTS.items():
            if pattern in paradigm and pattern != paradigm:
                paradigm = correct_version

        paradigm = paradigm.replace("-paradigm", "") if paradigm != "multi-paradigm" else paradigm

        if paradigm and paradigm not in cleaned_paradigms:
            cleaned_paradigms.append(paradigm)

    return cleaned_paradigms

def clean_computational_classes(classes):
    cleaned_classes = []

    for cls in classes:
        cls_lower = cls.lower()

        if "category:" in cls_lower:
            cls = cls[cls_lower.index("category:") + len("category:"):]

        for pattern, correct_version in COMPUTATIONAL_CLASS_REPLACEMENTS.items():
            if pattern in cls and pattern != cls:
                print(f"Replacing '{pattern}' with '{correct_version}' in '{cls}'")
                cls = correct_version

        if cls and cls not in cleaned_classes:
            cleaned_classes.append(cls)

    return cleaned_classes


def final_clean_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for language in data:
        if 'Categories' in language:
            language['Categories'] = [category for category in language['Categories'] if not is_year(category)]

        remove_empty_values(language, ['Paradigms', 'Dimensions', 'MemorySystem', 'ComputationalClass'])

        if language.get('Paradigms'):
            language['Paradigms'] = clean_paradigms(language['Paradigms'])

        if language.get('ComputationalClass'):
            language['ComputationalClass'] = clean_computational_classes(language['ComputationalClass'])

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Final data cleaned and saved to '{output_file}'.")


def remove_empty_values(language, fields):
    for field in fields:
        if field in language and isinstance(language[field], list):
            language[field] = [item for item in language[field] if item != ""]
        elif field in language and isinstance(language[field], str):
            if language[field].strip() == "":
                language[field] = None


def is_year(value):
    return value.isdigit() and len(value) == 4

input_file = 'data/esolangs-cleaned.json'
output_file = 'data/esolangs-data-final.json'

final_clean_data(input_file, output_file)