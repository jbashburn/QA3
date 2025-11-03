# manage_subscribers.py

import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END
import database

# --- Core Functions ---

def populate_subscriber_list():
    """Clears and re-loads the subscriber listbox."""
    subscriber_listbox.delete(0, END)
    for email in database.get_subscribers():
        subscriber_listbox.insert(END, email)

def add_email():
    """Adds the email from the entry box to the database."""
    email = email_entry.get().strip()
    if not email or "@" not in email or "." not in email:
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    if database.add_subscriber(email):
        messagebox.showinfo("Email Added", f"{email} has been added.")
        populate_subscriber_list()
        email_entry.delete(0, END) # Clear entry box on success
    else:
        messagebox.showwarning("Already Added", f"{email} is already on the list.")

def delete_selected_subscriber():
    """Deletes the currently selected email."""
    try:
        selected_email = subscriber_listbox.get(subscriber_listbox.curselection()[0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_email}?"):
            if database.delete_subscriber(selected_email):
                messagebox.showinfo("Deleted", f"{selected_email} has been deleted.")
                populate_subscriber_list()
            else:
                messagebox.showerror("Error", f"Failed to delete {selected_email}.")
    except IndexError:
        messagebox.showwarning("No Selection", "Please select an email to delete.")

# --- GUI Setup ---

root = tk.Tk()
root.title("Subscriber Manager")
root.geometry("500x450") # Made window shorter
root.configure(bg="white")
root.resizable(False, False)

tk.Label(root, text="Subscriber Manager", font=("Helvetica", 20, "bold"), fg="#2196F3", bg="white").pack(pady=(20, 10))

# --- Add Email Section ---
add_frame = tk.Frame(root, bg="white")
add_frame.pack(pady=10)

email_entry = tk.Entry(add_frame, width=30, font=("Helvetica", 12))
email_entry.pack(side=tk.LEFT, padx=5)

tk.Button(add_frame, text="Add Email", command=add_email, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=10).pack(side=tk.LEFT)

# --- Manage Subscribers Section ---
list_frame = tk.Frame(root)
list_frame.pack(pady=(10, 5))

scrollbar = Scrollbar(list_frame, orient=tk.VERTICAL)
subscriber_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, width=50, height=10, font=("Helvetica", 12))
scrollbar.config(command=subscriber_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
subscriber_listbox.pack(side=tk.LEFT)

# --- Delete Button ---
tk.Button(root, text="Delete Selected", command=delete_selected_subscriber, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(pady=10)

# --- Initial Load & Main Loop ---
populate_subscriber_list()
root.mainloop()