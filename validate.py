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
    warnings = 0
    folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and not d.startswith('.')]
    invalid_folders = [f for f in folders if f not in ALLOWED_LANGUAGES]
    return (invalid_folders, warnings)


def compare_structure(base_path, reference_lang="en"):
    """Check that all folders have the same structure as the reference language folder."""
    reference_path = os.path.join(base_path, reference_lang)
    reference_structure = get_folder_structure(reference_path)

    warnings = 0
    issues = {}
    for lang in ALLOWED_LANGUAGES:
        if lang == reference_lang:
            continue
        lang_path = os.path.join(base_path, lang)
        if not os.path.exists(lang_path):
            print(f"⚠️  Warning: {lang} is needed")
            warnings = warnings + 1
            continue
        # Check each file of the lang folder if it idoesn't exist in the reference lang folder add an issue
        for rel_dir, files in get_folder_structure(lang_path).items():
            if rel_dir not in reference_structure:
                issues[lang] = f"Extra folder: {rel_dir}"

    return (issues, warnings)


def validate_json_structure(base_path, reference_lang="en"):
    """Check that JSON files have the same structure as their reference language counterparts."""
    reference_path = os.path.join(base_path, reference_lang)
    reference_jsons = {
        os.path.relpath(os.path.join(dp, f), reference_path): os.path.join(dp, f)
        for dp, _, filenames in os.walk(reference_path)
        for f in filenames if f.endswith(".json")
    }

    warnings = 0
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
                print(f"⚠️  Warning: Missing JSON file: {rel_path}")
                warnings = warnings + 1
                continue
            try:
                with open(ref_file, "r", encoding="utf-8") as rf, open(lang_file, "r", encoding="utf-8") as lf:
                    ref_data = json.load(rf)
                    lang_data = json.load(lf)
                    if ref_data.keys() != lang_data.keys():
                        issues[lang] = f"JSON structure mismatch in {rel_path}"
            except json.JSONDecodeError:
                issues[lang] = f"Invalid JSON in {rel_path}"
    return (issues, warnings)


def main():
    warnings = 0
    base_path = os.getcwd()

    (invalid_folders, tmp_warning) = check_folder_names(base_path)
    warnings = warnings + tmp_warning
    tmp_warning = 0
    if invalid_folders:
        print(f"Invalid language folders found: {invalid_folders}")
        exit(1)

    (structure_issues, tmp_warning) = compare_structure(base_path)
    warnings = warnings + tmp_warning
    tmp_warning = 0
    if structure_issues:
        print(f"Structure issues: {structure_issues}")
        exit(1)

    (json_issues, tmp_warning) = validate_json_structure(base_path)
    warnings = warnings + tmp_warning
    tmp_warning = 0
    if json_issues:
        print(f"JSON structure issues: {json_issues}")
        exit(1)

    if (warnings > 0):
        print(f"❗  Validation passed with {warnings} warnings")
        exit(0)
    print(f"✅  Validation passed!")
    exit(0)


if __name__ == "__main__":
    main()
