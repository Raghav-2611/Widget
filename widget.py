import tkinter as tk
from github import Github
import requests
import datetime
from bs4 import BeautifulSoup

GITHUB_USERNAME = 'Raghav-2611'
GITHUB_TOKEN = ''  # GitHub API token if needed for authentication

def get_contributions():
    url = f"https://github.com/users/{GITHUB_USERNAME}/contributions"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None

def parse_contributions_html(contributions_html):
    soup = BeautifulSoup(contributions_html, 'html.parser')
    streak, max_streak, current_streak, total_contributions = 0, 0, 0, 0

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

def update_widget():
    contributions_html = get_contributions()
    if contributions_html:
        current_streak, max_streak, total_contributions = parse_contributions_html(contributions_html)
        refresh_widget(current_streak, max_streak, total_contributions)

def refresh_widget(streak, max_streak, total_contributions):
    streak_label.config(text=f"Current Streak: {streak} days")
    max_streak_label.config(text=f"Max Streak: {max_streak} days")
    total_contributions_label.config(text=f"Total Contributions: {total_contributions} this year")
    update_label.config(text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    progress_bar.coords(progress_fill, 10, 10, 10 + (streak * 3), 40)

def create_widget(streak, max_streak, total_contributions):
    global streak_label, max_streak_label, total_contributions_label, update_label, progress_bar, progress_fill

    root = tk.Tk()
    root.title("GitHub Contribution Streak")
    root.configure(bg="#f5f5f5")

    canvas = tk.Canvas(root, width=400, height=150, bg="white")
    canvas.pack()

    # Labels for streak and contributions
    streak_label = tk.Label(root, text=f"Current Streak: {streak} days", font=("Helvetica", 12), bg="#f5f5f5")
    streak_label.pack()
    
    max_streak_label = tk.Label(root, text=f"Max Streak: {max_streak} days", font=("Helvetica", 12), bg="#f5f5f5")
    max_streak_label.pack()

    total_contributions_label = tk.Label(root, text=f"Total Contributions: {total_contributions} this year", font=("Helvetica", 12), bg="#f5f5f5")
    total_contributions_label.pack()

    # Progress bar
    progress_bar = tk.Canvas(root, width=310, height=30, bg="white", bd=0, highlightthickness=0)
    progress_bar.pack(pady=5)
    progress_bar.create_rectangle(10, 10, 310, 40, outline="#7cb342", width=2)
    progress_fill = progress_bar.create_rectangle(10, 10, 10 + (streak * 3), 40, fill="#aed581", outline="")

    # Last updated time
    update_label = tk.Label(root, text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", font=("Helvetica", 8), bg="#f5f5f5")
    update_label.pack()

    # Refresh button
    refresh_button = tk.Button(root, text="Refresh", command=update_widget, font=("Helvetica", 10), bg="#388e3c", fg="white")
    refresh_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    contributions_html = get_contributions()
    if contributions_html:
        current_streak, max_streak, total_contributions = parse_contributions_html(contributions_html)
        create_widget(current_streak, max_streak, total_contributions)
    else:
        print("Could not retrieve contributions.")
