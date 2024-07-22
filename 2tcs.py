import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, Menu
import language_tool_python

# Initialize the LanguageTool object
tool = language_tool_python.LanguageTool('en-US')

# Function to check and correct grammar errors
def check_grammar():
    text = text_area.get("1.0", tk.END)
    matches = tool.check(text)
    
    corrected_text = tool.correct(text)
    
    result_area.delete("1.0", tk.END)
    result_area.insert(tk.END, corrected_text)
    
    error_display.delete("1.0", tk.END)
    text_area.tag_remove('highlight', '1.0', tk.END)
    
    for match in matches:
        error_display.insert(tk.END, f"Error: {match.message}\n"
                                    f"Context: {match.context}\n"
                                    f"Suggested Correction: {match.replacements}\n\n")
        start = f"{match.offset + 1}.0"
        end = f"{match.offset + match.errorLength + 1}.0"
        text_area.tag_add('highlight', start, end)
    text_area.tag_config('highlight', background='yellow', foreground='red')

# Function to load text from a file
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, text)

# Function to save corrected text to a file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            corrected_text = result_area.get("1.0", tk.END)
            file.write(corrected_text)
        messagebox.showinfo("File Saved", "The corrected text has been saved successfully.")

# Function to handle real-time error detection
def on_text_change(event):
    check_grammar()

# Function to switch language
def switch_language(lang_code):
    global tool
    tool = language_tool_python.LanguageTool(lang_code)
    check_grammar()

# Undo and redo functions
def undo():
    text_area.edit_undo()

def redo():
    text_area.edit_redo()

# Create the main window
root = tk.Tk()
root.title("Grammar and Spelling Checker")

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add File menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Load Text", command=load_file)
file_menu.add_command(label="Save Corrected Text", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit menu
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)

# Add Language menu
language_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Language", menu=language_menu)
language_menu.add_command(label="English (US)", command=lambda: switch_language('en-US'))
language_menu.add_command(label="English (UK)", command=lambda: switch_language('en-GB'))
language_menu.add_command(label="French", command=lambda: switch_language('fr'))

# Label for user input
tk.Label(root, text="Input Text:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

# Text area for user input
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.grid(row=1, column=0, padx=10, pady=5)
text_area.bind('<<Modified>>', on_text_change)

# Button to check grammar
check_button = tk.Button(root, text="Check Grammar", command=check_grammar)
check_button.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

# Label for corrected text
tk.Label(root, text="Corrected Text:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

# Text area for displaying corrected text
result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
result_area.grid(row=4, column=0, padx=10, pady=5)

# Label for error details
tk.Label(root, text="Error Details:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

# Text area for displaying errors
error_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
error_display.grid(row=6, column=0, padx=10, pady=5)

# Run the application
root.mainloop()
