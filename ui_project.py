import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
from Project import main

class RedditAutomationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Automation Tool")
        self.create_widgets()
        self.is_running = False
        self.thread = None
        self.stop_event = threading.Event()

    def create_widgets(self):
        
        heading_label = tk.Label(self.root, text="Reddit Automation Tool", font=("Helvetica", 16))
        heading_label.pack(pady=10)

        search_terms_label = tk.Label(self.root, text="Search Terms:", font=("Helvetica", 12))
        search_terms_label.pack(pady=5)

        self.search_terms_text = tk.Text(self.root, height=5, width=50)
        self.search_terms_text.pack(pady=5)

        profile_name_label = tk.Label(self.root, text="Current Profile Name:", font=("Helvetica", 12))
        profile_name_label.pack(pady=5)

        self.profile_name_text = tk.StringVar()
        profile_name_entry = tk.Entry(self.root, textvariable=self.profile_name_text, font=("Helvetica", 12))
        profile_name_entry.pack(pady=5)

        status_label = tk.Label(self.root, text="Status:", font=("Helvetica", 14))
        status_label.pack(pady=5)

        self.status_text = tk.StringVar()
        status_entry = tk.Entry(self.root, textvariable=self.status_text, font=("Helvetica", 14), width=50)
        status_entry.pack(pady=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        scroll_time_label = tk.Label(frame, text="Scroll Time (minutes):", font=("Helvetica", 12))
        scroll_time_label.grid(row=0, column=0, padx=5)

        self.scroll_time = tk.StringVar()
        scroll_time_entry = tk.Entry(frame, textvariable=self.scroll_time, font=("Helvetica", 12))
        scroll_time_entry.grid(row=0, column=1, padx=5)

        port_number_label = tk.Label(self.root, text="Port Number:", font=("Helvetica", 12))
        port_number_label.pack(pady=5)

        self.port_number = tk.StringVar()
        port_number_entry = tk.Entry(self.root, textvariable=self.port_number, font=("Helvetica", 12))
        port_number_entry.pack(pady=5)

        upvote_rate_label = tk.Label(frame, text="Posts to upvote:", font=("Helvetica", 12))
        upvote_rate_label.grid(row=0, column=2, padx=5)

        self.upvote_rate = tk.StringVar()
        upvote_rate_entry = tk.Entry(frame, textvariable=self.upvote_rate, font=("Helvetica", 12))
        upvote_rate_entry.grid(row=0, column=3, padx=5)

        progress_label = tk.Label(self.root, text="Progress:", font=("Helvetica", 12))
        progress_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate', maximum=1200)
        self.progress.pack(pady=5)

        self.progress_text = tk.StringVar()
        self.progress_label = tk.Label(self.root, textvariable=self.progress_text, font=("Helvetica", 12))
        self.progress_label.pack(pady=5)

        run_button = tk.Button(self.root, text="Run", command=self.run_main_thread, font=("Helvetica", 12))
        run_button.pack(pady=20)

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_main, font=("Helvetica", 12))
        stop_button.pack(pady=20)

    def update_ui(self, search_terms, profile_name, status):
        def update():
            if search_terms is not None:
                self.search_terms_text.delete(1.0, tk.END)
                self.search_terms_text.insert(tk.END, "\n".join(search_terms))
            if profile_name is not None:
                self.profile_name_text.set(profile_name)
            if status is not None:
                self.status_text.set(status)
        self.root.after(0, update)

    def update_progress(self, value, total_time):
        def update():
            self.progress['value'] = value
            minutes_passed = value // 60
            self.progress_text.set(f"{minutes_passed}/{total_time} mins")
            self.root.update_idletasks()
        self.root.after(0, update)

    def run_main_thread(self):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run_main_loop)
            self.thread.start()

    def run_main_loop(self):
        while not self.stop_event.is_set():
            try:
                scroll_time = int(self.scroll_time.get())
                upvote_rate = int(self.upvote_rate.get())
                port_number = int(self.port_number.get())
                self.progress['maximum'] = scroll_time * 60
                main(self.update_ui, self.stop_event, scroll_time, upvote_rate, port_number, self.update_progress)
            except Exception as e:
                if self.is_running:  # Only show error if it wasn't stopped manually
                    messagebox.showerror("Error", f"An error occurred: {e}")
                self.restart_main()  # Restart the main function if an error occurs
            finally:
                if self.stop_event.is_set():
                    break

    def stop_main(self):
        self.is_running = False
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
            self.profile_name_text.set("Stopped")
            self.status_text.set("Stopped by user")
            self.progress['value'] = 0
            self.progress_text.set("0/0 mins")

    def restart_main(self):
        self.stop_main()
        self.run_main_thread()

# Create the main window
root = tk.Tk()
app = RedditAutomationTool(root)

print("Starting UI...")

# Run the application
root.mainloop()
