# Project: Find Duplicates

A Python-based utility tailored to find and manage duplicate files within your directories. Includes both a Command Line Interface (CLI) and a Graphical User Interface (GUI).

## 🎯 Motivation

I wanted to dive deeper into Python and solve a real-world problem while getting familiar with version control.

**The Problem**: managing large collections of music and photos often leads to cluttered folders with multiple copies of the same file.
**The Solution**: A script that efficiently scans, identifies, and helps remove these duplicates.

## ⚙️ How it Works

This program uses a smart two-step process to find duplicates efficiently:

1.  **Group by Size**: First, it checks the size of every file.
    -   *Why?* Getting a file's size is extremely fast. If two files have different sizes, they definitely aren't duplicates.
2.  **Check Hash (MD5)**: For files with identical sizes, it calculates a unique digital fingerprint (hash) of the file's content.
    -   *Why?* If two files have the same size AND the same hash, their content is identical. This confirms they are duplicates.

## ✨ Features

-   **Dual Interface**: Choose between a simple CLI or a user-friendly GUI.
-   **Recursive Scanning**: Scans the selected folder and all its subfolders.
-   **Efficient**: Quickly ignores unique files by size before doing heavy processing.
-   **Safe**: Uses MD5 hashing to ensure files are truly identical before flagging them.

## 🚀 How to Run

### Requirements
-   Python 3.x
-   Tkinter (usually included with Python)

### Option 1: Graphical User Interface (GUI)
The recommended way for visual feedback.

1.  Run the script:
    ```bash
    python gui_main.py
    ```
2.  Click **"Select Folder"** to choose the directory you want to scan.
3.  Click **"Start Scan"**.
4.  View the progress and results in the window.

### Option 2: Command Line Interface (CLI)
For quick, text-based usage.

1.  Run the script:
    ```bash
    python find_duplicates.py
    ```
2.  Paste the folder path when prompted and press Enter.

---
© 2026 LucianB2023
