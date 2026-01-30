import os
import hashlib
from collections import defaultdict

def scan_for_duplicates(folder_path):
    """
    Scans a folder for duplicate files.
    Logic:
    1. Group files by size (because checking size is very fast).
    2. If files have the same size, they *might* be duplicates.
    3. Only then, check the hash (content fingerprint) to be 100% sure.
    """
    
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    print(f"Scanning folder: {folder_path}...")

    # Dictionary to group files by their size
    # Structure: { file_size_in_bytes: [list_of_file_paths] }
    files_by_size = defaultdict(list)

    # Step 1: Walk through all folders and subfolders
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            try:
                # getting file size is fast!
                file_size = os.path.getsize(filepath)
                
                # Add it to our list
                files_by_size[file_size].append(filepath)
            except OSError:
                # Skip files we can't read (permission errors, etc.)
                continue

    # Step 2: Filter for potential duplicates
    # We only care about sizes that appear more than once
    potential_duplicates = []
    
    for size, file_list in files_by_size.items():
        if len(file_list) > 1:
            # If more than 1 file has this size, it's a candidate!
            potential_duplicates.extend(file_list)

    print(f"Found {len(potential_duplicates)} candidates based on size.")

    # Step 3: Verify with Hashing (The slow but accurate part)
    # Dictionary to group files by their hash
    # Structure: { hash_string: [list_of_file_paths] }
    files_by_hash = defaultdict(list)

    for filepath in potential_duplicates:
        try:
            # Calculate the hash
            file_hash = get_file_hash(filepath)
            if file_hash:
                files_by_hash[file_hash].append(filepath)
        except Exception as e:
            print(f"Could not hash {filepath}: {e}")

    # Step 4: Report Results
    print("\n--- Duplicate Results ---")
    duplicate_count = 0
    
    for file_hash, file_list in files_by_hash.items():
        # If a hash appears more than once, we have confirmed duplicates!
        if len(file_list) > 1:
            duplicate_count += 1
            print(f"\nGroup {duplicate_count} (Hash: {file_hash})")
            for path in file_list:
                print(f" - {path}")
    
    if duplicate_count == 0:
        print("\nNo duplicates found!")

def get_file_hash(filepath):
    """
    Calculates the MD5 hash of a file.
    This creates a unique 'fingerprint' of the file's content.
    """
    hasher = hashlib.md5()
    
    # Open file in binary mode
    with open(filepath, "rb") as f:
        # Read in chunks (4096 bytes) so we don't crash memory with large files
        chunk = f.read(4096)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(4096)
            
    return hasher.hexdigest()

if __name__ == "__main__":
    # Ask the user for a folder to scan
    folder = input("Enter the folder path to scan (or press Enter for current folder): ").strip()
    
    if not folder:
        folder = "." # Current directory
        
    scan_for_duplicates(folder)
