import tkinter as tk
from github import Github
import requests
import datetime

GITHUB_USERNAME = 'Raghav-2611'
GITHUB_TOKEN = '' 

def get_contributions():
    url = f"https://github.com/users/{GITHUB_USERNAME}/contributions"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve data.")
        return None

def get_streak():
    contributions_html = get_contributions()
    if not contributions_html:
        return 0

    streak = 0
    max_streak = 0
    for line in contributions_html.splitlines():
        if 'data-count="' in line:

            count = int(line.split('data-count="')[1].split('"')[0])
            if count > 0:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0 
    return max_streak

def create_widget(streak):
    root = tk.Tk()
    root.title("GitHub Contribution Streak")

    canvas = tk.Canvas(root, width=300, height=50, bg="white")
    canvas.pack()

    label = tk.Label(root, text=f"GitHub Streak: {streak} days", font=("Helvetica", 12))
    label.pack()

    for i in range(streak):
        canvas.create_rectangle(10 + (i * 15), 20, 25 + (i * 15), 35, fill="green")

    root.mainloop()

if __name__ == "__main__":
    streak = get_streak()
    create_widget(streak)
