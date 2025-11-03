# newsletter.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, END
import database
import main
import emailer

# This global list stores the articles after "Load Preview" is clicked,
# so the "Send" button can use the full data for the HTML email.
current_articles_list = []

def load_preview():
    """Fetches articles, stores them, and shows a plain-text preview."""
    global current_articles_list
    try:
        current_articles_list = main.generate_newsletter()
        if not current_articles_list:
            messagebox.showwarning("No Articles", "No articles were found.")
            return

        # Format a plain-text preview
        preview_text = "--- TODAY'S TENNESSEE NEWS ---\n\n"
        for item in current_articles_list:
            preview_text += (
                f"{item.get('title', 'Untitled')}\n\n"
                f"{item.get('summary', 'No summary.')}\n\n"
                f"Read more: {item.get('url', '#')}\n"
                f"{'-'*60}\n\n"
            )

        preview_box.delete("1.0", END)
        preview_box.insert(END, preview_text)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate newsletter:\n{e}")
        current_articles_list = [] # Reset on error

def send_newsletter():
    """Sends the full HTML newsletter using the stored article list."""
    if not current_articles_list:
        messagebox.showerror("Error", "Please load a preview before sending.")
        return
    
    try:
        subscribers = database.get_subscribers()
        if not subscribers:
            messagebox.showwarning("No Subscribers", "No subscribers to send to.")
            return
        
        for email in subscribers:
            emailer.send_email(email, current_articles_list) 
        
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

preview_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=20)
preview_box.pack(padx=20, pady=10)

send_btn_frame = tk.Frame(root, bg="white")
send_btn_frame.pack(pady=10)

tk.Button(send_btn_frame, text="Load Preview", command=load_preview, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10)
tk.Button(send_btn_frame, text="Send Newsletter", command=send_newsletter, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10)

root.mainloop()