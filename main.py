import tkinter as tk
from tkinter import messagebox
import database as db

# --- Define Colors ---
BG_COLOR = "#FFFFFF"       # White background
BUTTON_COLOR = "#9575CD"   # A nice medium-light purple for the button
BUTTON_ACTIVE = "#7E57C2"  # A slightly darker purple for when clicked
TITLE_COLOR = "#9575CD"    # Light purple title text
TEXT_COLOR = "#000000"     # Black regular text
PLACEHOLDER_COLOR = "grey"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("The Daily Value - Newsletter Subscription")
        self.geometry("400x220") # Increased height slightly for better spacing
        self.configure(bg=BG_COLOR)
        
        # Center the window on launch (optional but nice)
        self.eval('tk::PlaceWindow . center')

        # Main frame
        main_frame = tk.Frame(self, pad_x=20, pad_y=20, bg=BG_COLOR)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Title Label
        title_label = tk.Label(
            main_frame,
            text="The Daily Value",
            font=("Arial", 22, "bold"), # Slightly larger font
            bg=BG_COLOR,
            fg=TITLE_COLOR
        )
        title_label.pack(pady=(0, 5))

        # Subtitle Label
        subtitle_label = tk.Label(
            main_frame,
            text="Get your daily Tennessee news summary.",
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        subtitle_label.pack(pady=(0, 25)) # Increased padding

        # Email Entry
        self.email_entry = tk.Entry(
            main_frame,
            font=("Arial", 12),
            width=30,
            bd=1, # Border
            relief="solid", # Solid border style
        )
        self.email_entry.pack(pady=5, ipady=5) # Slightly taller entry box
        self.email_entry.insert(0, "Enter your email")
        
        # Bind focus events to clear/restore placeholder
        self.email_entry.bind("<FocusIn>", self.on_entry_click)
        self.email_entry.bind("<FocusOut>", self.on_focusout)
        self.email_entry.config(fg=PLACEHOLDER_COLOR)

        # Subscribe Button
        subscribe_button = tk.Button(
            main_frame,
            text="Subscribe",
            font=("Arial", 12, "bold"),
            command=self.subscribe_action,
            bg=BUTTON_COLOR,
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            bd=0, # No border
            activebackground=BUTTON_ACTIVE, # Click color
            activeforeground="white"
        )
        subscribe_button.pack(pady=10)

    def on_entry_click(self, event):
        """Called when the entry box is clicked."""
        if self.email_entry.get() == "Enter your email":
           self.email_entry.delete(0, "end") # delete all the text in the entry
           self.email_entry.config(fg=TEXT_COLOR)

    def on_focusout(self, event):
        """Called when the entry box loses focus."""
        if not self.email_entry.get():
            self.email_entry.insert(0, "Enter your email")
            self.email_entry.config(fg=PLACEHOLDER_COLOR)

    def subscribe_action(self):
        """Handles the subscribe button click."""
        email = self.email_entry.get()
        
        if not email or email == "Enter your email" or "@" not in email:
            # Use messagebox instead of alert
            messagebox.showwarning("Invalid Input", "Please enter a valid email address.")
            return

        # Add to database
        result = db.add_subscriber(email)
        
        # Show success/error message
        if "successful" in result or "already subscribed" in result:
            messagebox.showinfo("Subscription", result)
            # Clear the entry box on success
            if self.email_entry.get() != "Enter your email":
                self.email_entry.delete(0, "end")
                self.on_focusout(None) # Put placeholder back
        else:
            messagebox.showerror("Error", result)

def main():
    # Initialize the database file first
    print("Initializing database for GUI...")
    db.initialize_db()
    
    # Create and run the Tkinter app
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()



