import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from project import SpamDetector, EmailScanner

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SpamDetectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spam Detection System")
        self.geometry("700x600")
        
        self.detector = SpamDetector()
        self.is_trained = False
        
        self.create_widgets()
        
        # Start training in a separate thread
        self.status_label.configure(text="Initializing and downloading data...")
        threading.Thread(target=self.initialize_system, daemon=True).start()

    def create_widgets(self):
        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Input area expands

        # Title
        self.title_label = ctk.CTkLabel(self, text="Spam Mail Detector", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Status
        self.status_label = ctk.CTkLabel(self, text="Status: Waiting...", text_color="gray")
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Input Area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)

        self.input_label = ctk.CTkLabel(self.input_frame, text="Enter Message:", font=ctk.CTkFont(size=14))
        self.input_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.message_input = ctk.CTkTextbox(self.input_frame, height=150)
        self.message_input.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, padx=20, pady=10)

        self.check_btn = ctk.CTkButton(self.btn_frame, text="Check Message", command=self.check_message, state="disabled", width=150, height=40)
        self.check_btn.grid(row=0, column=0, padx=10)
        
        self.scan_btn = ctk.CTkButton(self.btn_frame, text="Scan Email Inbox", command=self.scan_email, state="disabled", width=150, height=40, fg_color="#E91E63", hover_color="#C2185B")
        self.scan_btn.grid(row=0, column=1, padx=10)

        # Result Area
        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.grid(row=4, column=0, padx=20, pady=20)
        
        self.result_label = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.result_label.pack()

    def initialize_system(self):
        try:
            if self.detector.load_data():
                self.after(0, lambda: self.status_label.configure(text="Training model..."))
                self.detector.train()
                self.is_trained = True
                self.after(0, self.enable_buttons)
                self.after(0, lambda: self.status_label.configure(text="System Ready", text_color="green"))
            else:
                self.after(0, lambda: self.status_label.configure(text="Error loading data", text_color="red"))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="red"))

    def enable_buttons(self):
        self.check_btn.configure(state="normal")
        self.scan_btn.configure(state="normal")

    def check_message(self):
        message = self.message_input.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showwarning("Input Error", "Please enter a message.")
            return
        
        prediction = self.detector.predict(message)
        if prediction == 'spam':
            self.result_label.configure(text="SPAM 🚨", text_color="red")
        else:
            self.result_label.configure(text="NOT SPAM (Ham) ✅", text_color="green")

    def scan_email(self):
        dialog = ctk.CTkInputDialog(text="Enter your Email:", title="Email Login")
        email_user = dialog.get_input()
        if not email_user:
            return
            
        dialog_pass = ctk.CTkInputDialog(text="Enter App Password:", title="Email Login")
        email_pass = dialog_pass.get_input()
        if not email_pass:
            return

        self.status_label.configure(text="Scanning emails...")
        
        # Run scan in thread
        threading.Thread(target=self.run_email_scan, args=(email_user, email_pass), daemon=True).start()

    def run_email_scan(self, user, password):
        scanner = EmailScanner()
        if scanner.connect(user, password):
            emails = scanner.fetch_emails(limit=5)
            scanner.close()
            
            results = []
            for mail in emails:
                content = f"{mail['subject']} {mail['body']}"
                pred = self.detector.predict(content)
                status = "SPAM" if pred == 'spam' else "HAM"
                results.append(f"[{status}] {mail['subject'][:30]}...")
            
            result_text = "\n".join(results)
            self.after(0, lambda: messagebox.showinfo("Scan Results", result_text))
            self.after(0, lambda: self.status_label.configure(text="Scan Complete", text_color="green"))
        else:
            self.after(0, lambda: messagebox.showerror("Error", "Connection failed. Check credentials."))
            self.after(0, lambda: self.status_label.configure(text="Connection Failed", text_color="red"))

if __name__ == "__main__":
    app = SpamDetectorGUI()
    app.mainloop()
