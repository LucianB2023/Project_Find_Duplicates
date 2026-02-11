import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import subprocess
import sys
from find_duplicates import scan_for_duplicates

class DuplicateFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate File Finder")
        self.root.geometry("600x400")
        
        self.selected_folder = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        
        self.duplicates = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Simple Duplicate Finder", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Folder Selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(folder_frame, text="Folder:").pack(side=tk.LEFT)
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, width=40)
        self.folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(folder_frame, text="Browse...", command=self.browse_folder).pack(side=tk.LEFT)
        
        # Scan Button
        self.scan_btn = ttk.Button(main_frame, text="Start Scan", command=self.start_scan)
        self.scan_btn.pack(pady=10)
        
        # Status Label (No progress bar, just text)
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Helvetica", 10))
        self.status_label.pack(pady=5)
        
        # Show Results Button (Hidden initially)
        self.show_res_btn = ttk.Button(main_frame, text="Show Results", command=self.open_results_window, state=tk.DISABLED)
        self.show_res_btn.pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
            
    def start_scan(self):
        folder = self.selected_folder.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
            
        self.scan_btn.config(state=tk.DISABLED)
        self.show_res_btn.config(state=tk.DISABLED)
        self.status_var.set("Scanning...") # Simple status logit
        
        # Run in thread so GUI doesn't freeze
        thread = threading.Thread(target=self.run_scan_thread, args=(folder,))
        thread.start()
        
    def run_scan_thread(self, folder):
        try:
            # Run the scan
            self.duplicates = find_duplicates(folder)
            
            # Update UI on main thread
            self.root.after(0, self.on_scan_complete)
            
        except Exception as e:
            # Handle errors on main thread
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, self.reset_ui)

    def on_scan_complete(self):
        self.scan_btn.config(state=tk.NORMAL)
        
        count = len(self.duplicates)
        
        if count > 0:
            self.status_var.set(f"Scan Complete. Found {count} groups.")
            self.show_res_btn.config(state=tk.NORMAL)
            self.open_results_window() # Auto open results
        else:
            self.status_var.set("Scan Complete. No duplicates found.")
            messagebox.showinfo("Result", "No duplicates found!")

    def reset_ui(self):
        self.scan_btn.config(state=tk.NORMAL)
        self.status_var.set("Ready")

    def open_results_window(self):
        if not self.duplicates:
            return
        ResultsWindow(self.root, self.duplicates)


class ResultsWindow:
    def __init__(self, parent, duplicates):
        self.window = tk.Toplevel(parent)
        self.window.title("Duplicate Results")
        self.window.geometry("600x500")
        self.duplicates = duplicates
        
        self.check_vars = {} # map file path -> IntVar
        
        self.create_ui()
        
    def create_ui(self):
        # Top Controls
        top_frame = ttk.Frame(self.window, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Button(top_frame, text="Delete All (Keep One per Group)", command=self.delete_all_duplicates).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT)
        
        # Main Scrollable Area
        container = ttk.Frame(self.window)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate
        self.populate_list()
        
    def populate_list(self):
        for i, group in enumerate(self.duplicates):
            # Calculate size of first file (assuming all same)
            try:
                first_file = group[0]
                size = os.path.getsize(first_file)
            except:
                size = 0
                
            group_frame = ttk.LabelFrame(self.scrollable_frame, text=f"Group {i+1} - Size: {size} bytes", padding=5)
            group_frame.pack(fill=tk.X, expand=True, pady=5)
            
            for filepath in group:
                var = tk.IntVar()
                self.check_vars[filepath] = var
                
                # Checkbox
                chk = ttk.Checkbutton(group_frame, text=filepath, variable=var)
                chk.pack(anchor="w")
                
    def delete_all_duplicates(self):
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete all duplicates? One copy from each group will be kept."):
            return
            
        count = 0
        for group in self.duplicates:
            # Sort files for stability (alphabetical)
            files = sorted(group)
            # Keep the first one, delete the rest
            to_delete = files[1:] 
            
            for f in to_delete:
                if self.send_to_trash(f):
                    count += 1
                    
        messagebox.showinfo("Done", f"Moved {count} files to trash.")
        self.window.destroy()

    def delete_selected(self):
        to_delete = [path for path, var in self.check_vars.items() if var.get() == 1]
        
        if not to_delete:
            messagebox.showwarning("Warning", "No files selected.")
            return

        if not messagebox.askyesno("Confirm", f"Delete {len(to_delete)} selected files?"):
            return
            
        count = 0
        for f in to_delete:
            if self.send_to_trash(f):
                count += 1
                
        messagebox.showinfo("Done", f"Moved {count} files to trash.")
        self.window.destroy()

    def send_to_trash(self, filepath):
        """
        Sends a file to the trash/recycle bin in a cross-platform way.
        """
        try:
            if sys.platform == 'win32':
                # Windows Recycle Bin using PowerShell and VisualBasic
                # This avoids installing send2trash or other dependencies
                cmd = [
                    'powershell', '-Command',
                    f'Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("{filepath}", "OnlyErrorDialogs", "SendToRecycleBin")'
                ]
                # Check=True runs it and raises error if exit code != 0
                # Using subprocess.run with waiting to ensure it finishes
                subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Linux/Unix safe delete (trash-put or gio trash)
                # Trying common tools
                try:
                    subprocess.run(['gio', 'trash', filepath], check=True)
                except (FileNotFoundError, subprocess.CalledProcessError):
                    subprocess.run(['trash-put', filepath], check=True)
                    
            print(f"Recycled: {filepath}")
            return True
            
        except Exception as e:
            print(f"Error checking trash method for {filepath}: {e}")
            
            # Fallback to permanent delete if user accepts? 
            # Or just fail safe. Let's fail safe for now to avoid data loss.
            # But let's verify if the file still exists, maybe it was deleted.
            if not os.path.exists(filepath):
                 return True # treating as success if gone
                 
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinderGUI(root)
    root.mainloop()
