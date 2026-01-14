import json
import uuid
import os

target_files = [
    "values.ipynb",
    "logical.ipynb",
    "expressions_dataTypes.ipynb",
    "inputs.ipynb",
    "starting.ipynb"
]

# Set to track all IDs across all processed files to ensure global uniqueness
seen_ids = set()

def clean_notebook_ids(filepath):
    print(f"Cleaning {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return
    
    changed = False
    if 'cells' in data:
        for cell in data['cells']:
            # 1. Remove 'id' from metadata if present (conflicts with top-level id and causes warnings)
            if 'metadata' in cell and 'id' in cell['metadata']:
                print(f"  Removing metadata.id: {cell['metadata']['id']}")
                del cell['metadata']['id']
                changed = True
            
            # 2. Ensure top-level 'id' exists and is unique across ALL files
            if 'id' not in cell:
                new_id = str(uuid.uuid4())[:8]
                while new_id in seen_ids:
                    new_id = str(uuid.uuid4())[:8]
                cell['id'] = new_id
                seen_ids.add(new_id)
                changed = True
            else:
                current_id = cell['id']
                if current_id in seen_ids:
                    # Duplicate found - regenerate
                    new_id = str(uuid.uuid4())[:8]
                    while new_id in seen_ids:
                        new_id = str(uuid.uuid4())[:8]
                    print(f"  Duplicate top-level ID found: {current_id} -> Replaced with {new_id}")
                    cell['id'] = new_id
                    seen_ids.add(new_id)
                    changed = True
                else:
                    seen_ids.add(current_id)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            # Ensure single newline at end of file
            f.write('\n')
        print(f"  --> Updated {filepath}")
    else:
        print(f"  --> No changes needed for {filepath}")

def main():
    root_dir = "/home/gslee/wGitHub/code-workout-python"
    for fname in target_files:
        fpath = os.path.join(root_dir, fname)
        if os.path.exists(fpath):
            clean_notebook_ids(fpath)
        else:
            print(f"File not found: {fpath}")

if __name__ == "__main__":
    main()
