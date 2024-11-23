import tkinter as tk
from tkinter import messagebox
from github import Github
import requests
import datetime
from bs4 import BeautifulSoup

GITHUB_USERNAME = 'Raghav-2611'
DEFAULT_REFRESH_INTERVAL = 3600000 


class GitHubTrackerApp:
    def __init__(self, root):
        self.root = root
        self.refresh_interval = DEFAULT_REFRESH_INTERVAL
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the main UI components."""
        self.root.title("GitHub Contribution Tracker")
        self.root.geometry("450x300")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        self.create_menu()

        main_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Label(main_frame, text="GitHub Contribution Tracker", font=("Helvetica", 16, "bold"),
                 bg="#ffffff", fg="#333333").pack(pady=5)

        self.streak_label = tk.Label(main_frame, text="Current Streak: Loading...", font=("Helvetica", 12),
                                     bg="#ffffff", fg="#555555")
        self.streak_label.pack()
        self.max_streak_label = tk.Label(main_frame, text="Max Streak: ", font=("Helvetica", 12),
                                         bg="#ffffff", fg="#555555")
        self.max_streak_label.pack()
        self.total_contributions_label = tk.Label(main_frame, text="Total Contributions: ", font=("Helvetica", 12),
                                                  bg="#ffffff", fg="#555555")
        self.total_contributions_label.pack()

        self.progress_bar = tk.Canvas(main_frame, width=300, height=20, bg="white", bd=0, highlightthickness=0)
        self.progress_bar.pack(pady=10)
        self.progress_bar.create_rectangle(10, 5, 300, 20, outline="#cccccc", width=1)
        self.progress_fill = self.progress_bar.create_rectangle(10, 5, 10, 20, fill="#4db6ac", outline="")

        tk.Button(main_frame, text="Refresh Now", command=self.update_data, bg="#4db6ac", fg="white",
                  font=("Helvetica", 10), relief="flat").pack(pady=10)

        self.status_label = tk.Label(main_frame, text="Last updated: Never", font=("Helvetica", 9),
                                     bg="#ffffff", fg="#999999")
        self.status_label.pack()

        self.update_data(auto_refresh=True)

    def create_menu(self):
        """Create the application menu bar."""
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def fetch_contributions_html(self):
        """Fetch GitHub contributions HTML."""
        url = f"https://github.com/users/{GITHUB_USERNAME}/contributions"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.log_error(f"Error retrieving data: {e}")
            return None

    def parse_contributions(self, html):
        """Parse the contribution HTML and extract stats."""
        soup = BeautifulSoup(html, 'html.parser')
        streak, max_streak, total_contributions = 0, 0, 0

        for rect in soup.find_all('rect', {'data-count': True}):
            count = int(rect['data-count'])
            total_contributions += count
            if count > 0:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return streak, max_streak, total_contributions

    def update_data(self, auto_refresh=False):
        """Update the widget with the latest contribution data."""
        html = self.fetch_contributions_html()
        if html:
            current_streak, max_streak, total_contributions = self.parse_contributions(html)
            self.update_ui(current_streak, max_streak, total_contributions)
        else:
            self.display_error()

        if auto_refresh:
            self.root.after(self.refresh_interval, lambda: self.update_data(auto_refresh=True))

    def update_ui(self, streak, max_streak, total_contributions):
        """Update the UI with the fetched data."""
        self.streak_label.config(text=f"Current Streak: {streak} days")
        self.max_streak_label.config(text=f"Max Streak: {max_streak} days")
        self.total_contributions_label.config(text=f"Total Contributions: {total_contributions} this year")
        self.status_label.config(text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        self.progress_bar.coords(self.progress_fill, 10, 10, 10 + (streak * 3), 20)

    def display_error(self):
        """Display an error message."""
        self.streak_label.config(text="Error fetching contributions.")
        self.max_streak_label.config(text="")
        self.total_contributions_label.config(text="")
        self.status_label.config(text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")

    def open_settings(self):
        """Open the settings dialog."""
        messagebox.showinfo("Settings", "Settings options will be available soon.")

    def show_about(self):
        """Show the about dialog."""
        messagebox.showinfo("About", "GitHub Contribution Tracker\nVersion 1.0\nCreated by Raghav-2611")

    def log_error(self, message):
        """Log errors to a file."""
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - {message}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubTrackerApp(root)
    root.mainloop()
