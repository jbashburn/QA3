# newsletter.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, END
import database
import main
import emailer
import datetime
import webbrowser  # <-- NEW: Import the webbrowser module

# This global list stores the articles after "Load Preview" is clicked
current_articles_list = []
email_subject = "Today's Top Business & Finance News"

# --- NEW: Function to open the clicked link ---
def open_link(event):
    """Handles the click event on a tagged link."""
    try:
        # Get the index of the character that was clicked
        index = preview_box.index(tk.CURRENT)
        
        # Get the whole line of text at that index
        line = preview_box.get(f"{index} linestart", f"{index} lineend")
        
        # Find the URL in that line
        if "Read more: " in line:
            url = line.split("Read more: ")[1].strip()
            
            # Check if it's a valid http link and open it
            if url.startswith("http"):
                webbrowser.open_new_tab(url)
    except Exception as e:
        print(f"Error opening link: {e}")
    
    # This stops the click from doing anything else (like adding a newline)
    return "break"

def load_preview():
    """Fetches articles, stores them, and shows a plain-text preview."""
    global current_articles_list
    try:
        current_articles_list = main.generate_newsletter()
        if not current_articles_list:
            messagebox.showwarning("No Articles", "No articles were found.")
            return

        # --- UPDATE: Must make the box editable to change it ---
        preview_box.config(state=tk.NORMAL)
        preview_box.delete("1.0", END)

        now = datetime.datetime.now().strftime("%I:%M:%S %p")
        preview_box.insert(END, f"--- TODAY'S BUSINESS NEWS (Fetched at: {now}) ---\n\n")

        # --- UPDATE: Insert articles one by one to apply tags ---
        for item in current_articles_list:
            title = item.get('title', 'Untitled')
            summary = item.get('summary', 'No summary.')
            url = item.get('url', '#')

            # Insert title (let's make it bold!)
            preview_box.insert(END, f"{title}\n\n", "bold_title") # <-- NEW
            
            # Insert summary
            preview_box.insert(END, f"{summary}\n\n")
            
            # Insert the clickable link
            preview_box.insert(END, f"Read more: {url}\n", "link") # <-- NEW
            
            # Insert the separator
            preview_box.insert(END, f"{'-'*60}\n\n")
        
        # --- UPDATE: Make the box read-only again ---
        preview_box.config(state=tk.DISABLED)

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
            emailer.send_email(email, current_articles_list, email_subject) 
        
        messagebox.showinfo("Sent", f"Newsletter sent to {len(subscribers)} subscribers!")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send newsletter:\n{e}")

# --- GUI Setup ---

root = tk.Tk()
root.title("Newsletter Sender")
root.geometry("700x550")
root.configure(bg="white")
root.resizable(False, False)

# --- Your updated GUI text ---
tk.Label(root, text="Business News Preview & Sender", font=("Helvetica", 20, "bold"), fg="#A382CA", bg="white").pack(pady=(20, 10))
tk.Label(root, text="Load a preview of the newsletter, then send it to all subscribers.", font=("Helvetica", 12), bg="white").pack(pady=(0, 10))

preview_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=20)
preview_box.pack(padx=20, pady=10)

# --- NEW: Configure the tags for our links and titles ---
preview_box.tag_config("link", foreground="blue", underline=True)
preview_box.tag_config("bold_title", font=("Helvetica", 13, "bold"))

# --- NEW: Bind mouse events to the "link" tag ---
preview_box.tag_bind("link", "<Button-1>", open_link) # Left-click
preview_box.tag_bind("link", "<Enter>", lambda e: preview_box.config(cursor="hand2")) # Mouse enter
preview_box.tag_bind("link", "<Leave>", lambda e: preview_box.config(cursor=""))     # Mouse leave

# --- Make the text box read-only from the start ---
preview_box.config(state=tk.DISABLED) # <-- NEW

send_btn_frame = tk.Frame(root, bg="white")
send_btn_frame.pack(pady=10)

# --- Your updated buttons/colors ---
tk.Button(send_btn_frame, text="Refresh News", command=load_preview, bg="#95A7FF", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10)
tk.Button(send_btn_frame, text="Send Newsletter", command=send_newsletter, bg="#95A7FF", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10)

# Auto-load the preview
root.after(1, load_preview)

root.mainloop()