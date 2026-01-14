import json
import uuid
import glob
import os

# Files mentioned in the warning
target_files = [
    "values.ipynb",
    "logical.ipynb",
    "expressions_dataTypes.ipynb",
    "inputs.ipynb",
    "starting.ipynb" # Found in grep search
]

# Set of all seen IDs to ensure global uniqueness across these files (optional but good practice)
seen_ids = set()

def fix_notebook(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = False
    
    if 'cells' in data:
        for cell in data['cells']:
            if 'id' in cell:
                cid = cell['id']
                if cid in seen_ids:
                    # Duplicate found
                    new_id = str(uuid.uuid4())[:8] # Generate a short-ish unique ID
                    # Check for collision (unlikely but possible)
                    while new_id in seen_ids:
                        new_id = str(uuid.uuid4())[:8]
                    
                    print(f"  Duplicate ID found: {cid} -> Replaced with {new_id}")
                    cell['id'] = new_id
                    seen_ids.add(new_id)
                    changed = True
                else:
                    seen_ids.add(cid)
            else:
                # Cell has no ID, generate one
                new_id = str(uuid.uuid4())[:8]
                cell['id'] = new_id
                seen_ids.add(new_id)
                print(f"  Missing ID -> Generated {new_id}")
                changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            # Add a trailing newline which jupyter usually has
            f.write('\n')
        print(f"  Saved changes to {filepath}")
    else:
        print(f"  No duplicates found in {filepath}")

def main():
    root_dir = "/home/gslee/wGitHub/code-workout-python"
    
    # First pass: Collect all existing IDs to avoid collisions with existing ones?
    # Actually, the logic above collects seen_ids as it goes. 
    # But if we process file A then file B, and file B has an ID that file A also has...
    # The first time we see it (in file A), it's added to seen_ids.
    # When we see it again in file B, it will be flagged as duplicate and replaced.
    # This effectively makes IDs unique across the set of processed files.
    # To be totally safe, we should probably preload IDs from valid files, 
    # but scanning these specific files sequentially and enforcing uniqueness roughly solves the user's issue 
    # of "Duplicate identifier". 
    
    for fname in target_files:
        fpath = os.path.join(root_dir, fname)
        if os.path.exists(fpath):
            fix_notebook(fpath)
        else:
            print(f"File not found: {fpath}")

if __name__ == "__main__":
    main()
