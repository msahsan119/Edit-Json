import tkinter as tk
from tkinter import filedialog, messagebox
import json

class JsonEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python JSON Editor")
        self.root.geometry("800x600")

        # Current file path
        self.current_file = None

        # --- UI Layout ---
        
        # Toolbar Frame
        self.toolbar = tk.Frame(self.root, bg="#eeeeee")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open = tk.Button(self.toolbar, text="Open File", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_save = tk.Button(self.toolbar, text="Save", command=self.save_file)
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_format = tk.Button(self.toolbar, text="Format (Prettify)", command=self.format_json)
        self.btn_format.pack(side=tk.LEFT, padx=5, pady=5)

        # Text Area with Scrollbar
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Using a monospaced font for code readability
        self.text_area = tk.Text(self.text_frame, 
                                 undo=True, 
                                 font=("Courier New", 12), 
                                 yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.text_area.yview)

        # Status Bar
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    # Format with 4 spaces for better editing
                    formatted_content = json.dumps(content, indent=4)
                    
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, formatted_content)
                self.current_file = file_path
                self.status.config(text=f"Editing: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def format_json(self):
        """Validates and reformats the text currently in the editor."""
        raw_text = self.text_area.get(1.0, tk.END).strip()
        if not raw_text:
            return
        try:
            parsed = json.loads(raw_text)
            formatted = json.dumps(parsed, indent=4)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, formatted)
            self.status.config(text="JSON Formatted Successfully")
        except json.JSONDecodeError as e:
            messagebox.showerror("Invalid JSON", f"Syntax Error: {e}")

    def save_file(self):
        # Get content from text area
        raw_text = self.text_area.get(1.0, tk.END).strip()
        
        # Basic validation before saving
        try:
            json_data = json.loads(raw_text)
        except json.JSONDecodeError as e:
            messagebox.showerror("Save Error", f"Cannot save! Invalid JSON syntax:\n{e}")
            return

        # If no file is open, treat "Save" as "Save As"
        if not self.current_file:
            self.current_file = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4)
                self.status.config(text=f"Saved: {self.current_file}")
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonEditor(root)
    root.mainloop()
