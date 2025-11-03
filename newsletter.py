# newsletter.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, END
import database
import main
import emailer

# --- Newsletter Functions ---

def load_preview():
    """Generates and displays the newsletter content."""
    try:
        preview_box.delete("1.0", END)
        preview_box.insert(END, main.generate_newsletter())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate newsletter:\n{e}")

def send_newsletter():
    """Sends the content in the preview box to all subscribers."""
    email_body = preview_box.get("1.0", END).strip()
    if not email_body:
        messagebox.showerror("Empty Newsletter", "Newsletter content is empty.")
        return
    try:
        subscribers = database.get_subscribers()
        if not subscribers:
            messagebox.showwarning("No Subscribers", "There are no subscribers in the database to send to.")
            return
            
        for email in subscribers:
            emailer.send_email(email, email_body)
        messagebox.showinfo("Sent", f"Newsletter sent to {len(subscribers)} subscribers!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send newsletter:\n{e}")

# --- GUI Setup ---

root = tk.Tk()
root.title("Newsletter Sender")
root.geometry("700x550")
root.configure(bg="white")
root.resizable(False, False)

tk.Label(root, text="Newsletter Preview & Sender", font=("Helvetica", 20, "bold"), fg="#4CAF50", bg="white").pack(pady=(20, 10))
tk.Label(root, text="Load a preview of the newsletter, then send it to all subscribers.", font=("Helvetica", 12), bg="white").pack(pady=(0, 10))

# --- Newsletter Preview Section ---
preview_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=20)
preview_box.pack(padx=20, pady=10)

send_btn_frame = tk.Frame(root, bg="white")
send_btn_frame.pack(pady=10)

tk.Button(send_btn_frame, text="Load Preview", command=load_preview, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10)
tk.Button(send_btn_frame, text="Send Newsletter", command=send_newsletter, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10)

root.mainloop()