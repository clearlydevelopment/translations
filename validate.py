import os
import json

# Allowed folder names (language codes from facepunch documentation)
ALLOWED_LANGUAGES = {"ar", "bg", "zh-cn", "zh-tw", "cs", "da", "nl", "en", "fi", "fr", "de", "el", "hu", "it", "ja", "ko", "no", "en-pt", "pl", "pt", "pt-br", "ro", "ru", "es", "es-419", "sv", "th", "tr", "uk", "vn"}


def get_folder_structure(root):
    """Recursively get all files and their relative paths in a directory, ignoring hidden folders."""
    structure = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        rel_dir = os.path.relpath(dirpath, root)
        structure[rel_dir] = sorted(filenames)
    return structure


def check_folder_names(base_path):
    """Check that only allowed language folders exist, ignoring hidden folders."""
    folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and not d.startswith('.')]
    invalid_folders = [f for f in folders if f not in ALLOWED_LANGUAGES]
    return invalid_folders


def compare_structure(base_path, reference_lang="en"):
    """Check that all folders have the same structure as the reference language folder."""
    reference_path = os.path.join(base_path, reference_lang)
    reference_structure = get_folder_structure(reference_path)

    issues = {}
    for lang in ALLOWED_LANGUAGES:
        if lang == reference_lang:
            continue
        lang_path = os.path.join(base_path, lang)
        if not os.path.exists(lang_path):
            print(f"⚠️  Warning: {lang} is needed")
            continue

        lang_structure = get_folder_structure(lang_path)
        if lang_structure != reference_structure:
            issues[lang] = "Folder structure mismatch"

    return issues


def validate_json_structure(base_path, reference_lang="en"):
    """Check that JSON files have the same structure as their reference language counterparts."""
    reference_path = os.path.join(base_path, reference_lang)
    reference_jsons = {
        os.path.relpath(os.path.join(dp, f), reference_path): os.path.join(dp, f)
        for dp, _, filenames in os.walk(reference_path)
        for f in filenames if f.endswith(".json")
    }

    issues = {}
    for lang in ALLOWED_LANGUAGES:
        if lang == reference_lang:
            continue
        lang_path = os.path.join(base_path, lang)
        if not os.path.exists(lang_path):
            continue
        for rel_path, ref_file in reference_jsons.items():
            lang_file = os.path.join(lang_path, rel_path)
            if not os.path.exists(lang_file):
                issues[lang] = f"Missing JSON file: {rel_path}"
                continue
            try:
                with open(ref_file, "r", encoding="utf-8") as rf, open(lang_file, "r", encoding="utf-8") as lf:
                    ref_data = json.load(rf)
                    lang_data = json.load(lf)
                    if ref_data.keys() != lang_data.keys():
                        issues[lang] = f"JSON structure mismatch in {rel_path}"
            except json.JSONDecodeError:
                issues[lang] = f"Invalid JSON in {rel_path}"
    return issues


def main():
    base_path = os.getcwd()
    
    invalid_folders = check_folder_names(base_path)
    if invalid_folders:
        print(f"Invalid language folders found: {invalid_folders}")
        exit(1)
    
    structure_issues = compare_structure(base_path)
    if structure_issues:
        print(f"Structure issues: {structure_issues}")
        exit(1)
    
    json_issues = validate_json_structure(base_path)
    if json_issues:
        print(f"JSON structure issues: {json_issues}")
        exit(1)
    
    print("Validation passed!")
    exit(0)


if __name__ == "__main__":
    main()
