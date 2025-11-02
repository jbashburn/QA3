# newsletter_gui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
import database
import main
import emailer

def clear_placeholder(event):
    if email_entry.get() == "Enter your email":
        email_entry.delete(0, tk.END)
        email_entry.config(fg="black")

def subscribe():
    email = email_entry.get().strip()
    if email == "" or email == "Enter your email":
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    if "@" in email and "." in email:
        success = database.add_subscriber(email)
        if success:
            messagebox.showinfo("Subscribed", f"{email} has been added to Daily Value News!")
        else:
            messagebox.showwarning("Already Subscribed", f"{email} is already on the list.")
        email_entry.delete(0, tk.END)
        email_entry.insert(0, "Enter your email")
        email_entry.config(fg="gray")
    else:
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")

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
        messagebox.showinfo("Sent", f"Newsletter sent to {len(subscribers)} subscribers!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send newsletter:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Daily Value News")
root.geometry("700x650")
root.configure(bg="white")

# Title
title = tk.Label(root, text="Daily Value News", font=("Helvetica", 22, "bold"), fg="#2196F3", bg="white")
title.pack(pady=(20, 5))

# Description
desc = tk.Label(root, text="Subscribe and preview Tennessee's top stories.", font=("Helvetica", 12), fg="black", bg="white")
desc.pack(pady=(0, 10))

# Email entry
email_entry = tk.Entry(root, width=35, font=("Helvetica", 12), fg="gray")
email_entry.insert(0, "Enter your email")
email_entry.bind("<FocusIn>", clear_placeholder)
email_entry.pack(pady=5)

# Subscribe button
subscribe_btn = tk.Button(root, text="Subscribe", command=subscribe, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5)
subscribe_btn.pack(pady=10)

# Preview box
preview_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=20)
preview_box.pack(padx=10, pady=10)

# Button frame
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)

load_btn = tk.Button(btn_frame, text="Load Preview", command=load_preview, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
load_btn.pack(side=tk.LEFT, padx=10)

send_btn = tk.Button(btn_frame, text="Send Newsletter", command=send_newsletter, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
send_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()