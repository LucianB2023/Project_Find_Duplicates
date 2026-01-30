# Simple Duplicate Finder

A simple, educational Python project to find duplicate files in a folder, written in Python 3.

## How it Works
This program uses a smart two-step process to find duplicates efficiently:

1.  **Group by Size**: First, it checks the size of every file and flags files with the same size as potential duplicates.
    *   *Why?* Getting a file's size is extremely fast. If two files have different sizes, they definitely aren't duplicates.
2.  **Check Hash**: For files flagged as potential duplicates, it calculates a "hash" (a unique digital fingerprint) of the file's content.
    *   *Why?* If two files have the same size and the same hash, their content is identical and it's the final confirmation that the files are duplicates.

## How to Run

1.  Make sure you have Python installed.
2.  Run the script:
    ```bash
    python3 find_duplicates.py
    ```
3.  Enter the folder path when prompted (or press Enter to scan the current folder).

## Features
*   Recursively scans subfolders.
*   Ignores unique files quickly (optimization).
*   Uses MD5 hashing for accuracy.

## Future Plans
*   Add GUI interface to the program.
*   Add more file types to scan for duplicates.
*   Add more methods to find duplicates.
*   Add more features to the program.
