#!/usr/bin/env python3

import os

import tkinter as tk

from tkinter import scrolledtext, messagebox, filedialog

from log_generator import generate_log


def save_file(logs: list[str], file_name: str = "logs.txt") -> None:
    folder_path = directory_input.get()
    if not folder_path:
        messagebox.showerror("Error", "Select a directory first!")
        return

    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, "w") as file:
            file.writelines(logs)
        messagebox.showinfo("Success", f"Logs saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")


def select_directory() -> None:
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        directory_input.delete(0, tk.END)
        directory_input.insert(0, folder_selected)


def generate_logs(event=None) -> None:
    try:
        log_count = int(logs_count_input.get())
        if log_count <= 0:
            messagebox.showerror("Error", "Log count must be greater than 0")
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")
        return

    text_output.delete(1.0, tk.END)
    logs = []

    for _ in range(log_count):
        log, tag = generate_log()
        logs.append(log)
        text_output.insert(tk.END, log, tag)

    if save_file_flag.get():
        save_file(logs)


# Main window
root = tk.Tk()
root.title("Log Generator")
root.geometry("1400x900")

# Input logs count
tk.Label(root, text="Enter log count:").pack(pady=8)
logs_count_input = tk.Entry(root)
logs_count_input.pack(pady=8)
logs_count_input.bind("<Return>", generate_logs)

# Select directory
tk.Label(root, text="Select Directory:").pack(pady=5)
directory_input = tk.Entry(root, width=50)
directory_input.pack(pady=5)
btn_select_directory = tk.Button(root, text="Browse...", command=select_directory)
btn_select_directory.pack(pady=5)

# Save to file switcher
save_file_flag = tk.BooleanVar()
save_file_checkbox = tk.Checkbutton(root, text="Save to file", variable=save_file_flag)
save_file_checkbox.pack(pady=8)

# Generate button
btn_generate = tk.Button(root, text="Generate Logs", command=generate_logs)
btn_generate.pack(pady=20)

# Logs text output
text_output = scrolledtext.ScrolledText(root, height=35)
text_output.pack(fill="x", padx=150)

text_output.tag_config("warning", foreground="red")
text_output.tag_config("info", foreground="blue")
text_output.tag_config("event", foreground="green")
text_output.tag_config("trace", foreground="gray")
text_output.tag_config("default", foreground="black")

root.mainloop()
