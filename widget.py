import tkinter as tk
from github import Github
import requests
import datetime
from bs4 import BeautifulSoup

GITHUB_USERNAME = 'Raghav-2611'

def get_contributions_html():
    """Fetches GitHub contribution HTML data."""
    url = f"https://github.com/users/{GITHUB_USERNAME}/contributions"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None

def parse_contributions(contributions_html):
    """Parses contribution HTML to calculate current streak, max streak, and total contributions."""
    soup = BeautifulSoup(contributions_html, 'html.parser')
    streak = max_streak = current_streak = total_contributions = 0

    for rect in soup.find_all('rect', {'data-count': True}):
        count = int(rect['data-count'])
        total_contributions += count
        if count > 0:
            streak += 1
            current_streak = streak
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return current_streak, max_streak, total_contributions

def update_contributions(auto_refresh=False):
    """Fetches and updates the contribution data in the widget."""
    contributions_html = get_contributions_html()
    if contributions_html:
        current_streak, max_streak, total_contributions = parse_contributions(contributions_html)
        refresh_widget(current_streak, max_streak, total_contributions)
    else:
        streak_label.config(text="Error fetching contributions.")
        max_streak_label.config(text="")
        total_contributions_label.config(text="")
    if auto_refresh:
        root.after(3600000, lambda: update_contributions(auto_refresh=True))  # Refresh every hour

def refresh_widget(streak, max_streak, total_contributions):
    """Updates the widget display with new streak data."""
    streak_label.config(text=f"Current Streak: {streak} days")
    max_streak_label.config(text=f"Max Streak: {max_streak} days")
    total_contributions_label.config(text=f"Total Contributions: {total_contributions} this year")
    update_label.config(text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    progress_bar.coords(progress_fill, 10, 10, 10 + (streak * 3), 40)

def minimize_window():
    """Minimizes the widget window to the taskbar."""
    root.iconify()

def close_window():
    """Closes the widget window."""
    root.destroy()

def create_widget(streak, max_streak, total_contributions):
    """Creates the Tkinter UI for the GitHub Contribution Tracker widget."""
    global root, streak_label, max_streak_label, total_contributions_label, update_label, progress_bar, progress_fill

    root = tk.Tk()
    root.title("GitHub Contribution Tracker")
    root.configure(bg="#f0f0f0")
    root.geometry("400x240")
    root.resizable(False, False)

    main_frame = tk.Frame(root, bg="#ffffff", bd=0, relief="solid")
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(anchor="nw", pady=5)

    tk.Button(button_frame, text=" ", command=close_window, bg="#ff5f57", relief="flat", width=2, height=1).grid(row=0, column=0, padx=2)
    tk.Button(button_frame, text=" ", command=minimize_window, bg="#ffbd2e", relief="flat", width=2, height=1).grid(row=0, column=1, padx=2)

    tk.Label(main_frame, text="GitHub Contribution Tracker", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#333333").pack(pady=5)

    streak_label = tk.Label(main_frame, text=f"Current Streak: {streak} days", font=("Helvetica", 11), bg="#ffffff", fg="#555555")
    streak_label.pack()
    max_streak_label = tk.Label(main_frame, text=f"Max Streak: {max_streak} days", font=("Helvetica", 11), bg="#ffffff", fg="#555555")
    max_streak_label.pack()
    total_contributions_label = tk.Label(main_frame, text=f"Total Contributions: {total_contributions} this year", font=("Helvetica", 11), bg="#ffffff", fg="#555555")
    total_contributions_label.pack()

    progress_bar = tk.Canvas(main_frame, width=300, height=20, bg="white", bd=0, highlightthickness=0)
    progress_bar.pack(pady=10)
    progress_bar.create_rectangle(10, 5, 300, 20, outline="#cccccc", width=1)
    progress_fill = progress_bar.create_rectangle(10, 5, 10 + (streak * 3), 20, fill="#4db6ac", outline="")

    update_label = tk.Label(main_frame, text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", font=("Helvetica", 8), bg="#ffffff", fg="#999999")
    update_label.pack(pady=5)

    tk.Button(main_frame, text="Refresh Now", command=update_contributions, bg="#4db6ac", fg="white", relief="flat").pack(pady=5)

    update_contributions(auto_refresh=True)
    root.mainloop()

if __name__ == "__main__":
    contributions_html = get_contributions_html()
    if contributions_html:
        current_streak, max_streak, total_contributions = parse_contributions(contributions_html)
        create_widget(current_streak, max_streak, total_contributions)
    else:
        print("Could not retrieve contributions.")
