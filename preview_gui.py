# preview_gui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
import main  # uses main.generate_newsletter()
import database
import emailer

def load_preview():
    try:
        email_body = main.generate_newsletter()
        preview_box.delete("1.0", tk.END)
        preview_box.insert(tk.END, email_body)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate newsletter:\n{e}")

def send_newsletter():
    email_body = preview_box.get("1.0", tk.END).strip()
    if not email_body:
        messagebox.showerror("Empty Newsletter", "Newsletter content is empty.")
        return

    try:
        subscribers = database.get_subscribers()
        for email in subscribers:
            emailer.send_email(email, email_body)
        messagebox.showinfo("Sent", "Newsletter has been sent to all subscribers!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send newsletter:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Newsletter Preview")
root.geometry("700x550")
root.configure(bg="white")

title = tk.Label(root, text="Preview Newsletter", font=("Helvetica", 18, "bold"), fg="#2196F3", bg="white")
title.pack(pady=10)

preview_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=25)
preview_box.pack(padx=10, pady=10)

btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)

load_btn = tk.Button(btn_frame, text="Load Preview", command=load_preview, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
load_btn.pack(side=tk.LEFT, padx=10)

send_btn = tk.Button(btn_frame, text="Send Newsletter", command=send_newsletter, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
send_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()