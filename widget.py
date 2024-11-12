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
        response.raise_for_status()  # Raises an error for HTTP codes 4xx or 5xx
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None

def parse_contributions_html(contributions_html):
    soup = BeautifulSoup(contributions_html, 'html.parser')
    streak, max_streak, current_streak = 0, 0, 0

    for rect in soup.find_all('rect', {'data-count': True}):
        count = int(rect['data-count'])
        if count > 0:
            streak += 1
            current_streak = streak
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return current_streak, max_streak

def create_widget(streak, max_streak):
    root = tk.Tk()
    root.title("GitHub Contribution Streak")

    canvas = tk.Canvas(root, width=400, height=100, bg="white")
    canvas.pack()

    # Streak Display
    streak_label = tk.Label(root, text=f"Current Streak: {streak} days", font=("Helvetica", 12))
    streak_label.pack()
    
    max_streak_label = tk.Label(root, text=f"Max Streak: {max_streak} days", font=("Helvetica", 12))
    max_streak_label.pack()

    # Display bars with colors depending on streak
    colors = ["#d4e157", "#aed581", "#7cb342", "#388e3c"]
    for i in range(streak):
        color = colors[min(i // 10, len(colors) - 1)]
        canvas.create_rectangle(10 + (i * 15), 50, 25 + (i * 15), 70, fill=color, outline="")

    # Last updated time
    update_label = tk.Label(root, text=f"Last updated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", font=("Helvetica", 8))
    update_label.pack()

    root.mainloop()

if __name__ == "__main__":
    contributions_html = get_contributions()
    if contributions_html:
        current_streak, max_streak = parse_contributions_html(contributions_html)
        create_widget(current_streak, max_streak)
    else:
        print("Could not retrieve contributions.")
