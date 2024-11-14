import tkinter as tk
from github import Github
import requests
import datetime
from bs4 import BeautifulSoup

GITHUB_USERNAME = 'Raghav-2611'
GITHUB_TOKEN = '' 

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

def update_contributions():
    """Fetches and updates the contribution data in the widget."""
    contributions_html = get_contributions_html()
    if contributions_html:
        current_streak, max_streak, total_contributions = parse_contributions(contributions_html)
        refresh_widget(current_streak, max_streak, total_contributions)

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

def create_widget(streak, max_streak, total_contributions):
    """Creates the Tkinter UI for the GitHub Contribution Tracker widget."""
    global root, streak_label, max_streak_label, total_contributions_label, update_label, progress_bar, progress_fill

    root = tk.Tk()
    root.title("GitHub Contribution Streak")
    root.configure(bg="#e0f7fa")

    main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
    main_frame.pack(padx=20, pady=20)

    tk.Label(main_frame, text="GitHub Contribution Tracker", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#00796b").pack(pady=10)

    streak_label = tk.Label(main_frame, text=f"Current Streak: {streak} days", font=("Helvetica", 12), bg="#ffffff")
    streak_label.pack()
    max_streak_label = tk.Label(main_frame, text=f"Max Streak: {max_streak} days", font=("Helvetica", 12), bg="#ffffff")
    max_streak_label.pack()
    total_contributions_label = tk.Label(main_frame, text=f"Total Contributions: {total_contributions} this year", font=("Helvetica", 12), bg="#ffffff")
    total_contributions_label.pack()

    progress_bar = tk.Canvas(main_frame, width=310, height=30, bg="white", bd=0, highlightthickness=0)
    progress_bar.pack(pady=5)
    progress_bar.create_rectangle(10, 10, 310, 40, outline="#00796b", width=2)
    progress_fill = progress_bar.create_rectangle(10, 10, 10 + (streak * 3), 40, fill="#4db6ac", outline="")

    create_heatmap_preview(main_frame)

    update_label = tk.Label(main_frame, text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", font=("Helvetica", 8), bg="#ffffff")
    update_label.pack()

    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Minimize", command=minimize_window, font=("Helvetica", 10), bg="#b0bec5", fg="black").pack(side="left", padx=5)
    tk.Button(button_frame, text="Refresh", command=update_contributions, font=("Helvetica", 10), bg="#00796b", fg="white").pack(side="left", padx=5)

    root.mainloop()

def create_heatmap_preview(frame):
    """Creates a mock heatmap preview for the contribution activity."""
    heatmap_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="flat")
    heatmap_frame.pack(pady=10)
    tk.Label(heatmap_frame, text="Contribution Heatmap", font=("Helvetica", 10), bg="#ffffff", fg="#00796b").pack()
    colors = ["#dcedc8", "#aed581", "#7cb342", "#388e3c"]
    for row in range(5):
        for col in range(7):
            color = colors[col % 4]
            tk.Frame(heatmap_frame, bg=color, width=10, height=10).grid(row=row, column=col, padx=2, pady=2)

if __name__ == "__main__":
    contributions_html = get_contributions_html()
    if contributions_html:
        current_streak, max_streak, total_contributions = parse_contributions(contributions_html)
        create_widget(current_streak, max_streak, total_contributions)
    else:
        print("Could not retrieve contributions.")
