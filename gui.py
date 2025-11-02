# gui.py

import tkinter as tk
from tkinter import messagebox
import database  # assumes add_subscriber(email) returns True/False

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

# GUI setup
root = tk.Tk()
root.title("Daily Value News")
root.configure(bg="white")
root.geometry("400x250")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Daily Value News", font=("Helvetica", 22, "bold"), fg="#2196F3", bg="white")
title.pack(pady=(20, 5))

# Description
desc = tk.Label(root, text="Stay informed with Tennessee's top stories.\nSubscribe to our daily newsletter below.", font=("Helvetica", 10), fg="black", bg="white")
desc.pack(pady=(0, 15))

# Email entry with placeholder
email_entry = tk.Entry(root, width=35, font=("Helvetica", 12), fg="gray")
email_entry.insert(0, "Enter your email")
email_entry.bind("<FocusIn>", clear_placeholder)
email_entry.pack(pady=5)

# Subscribe button
subscribe_btn = tk.Button(root, text="Subscribe", command=subscribe, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5)
subscribe_btn.pack(pady=15)

root.mainloop()