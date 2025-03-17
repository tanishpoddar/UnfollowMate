import json
import tkinter as tk
from tkinter import ttk
import webbrowser
from datetime import datetime
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load following and followers data
def load_json(filename):
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Extract usernames from JSON data
def extract_usernames(data, is_following=True):
    if is_following:
        return {user["string_list_data"][0]["value"].lower() for user in data["relationships_following"]}
    return {user["string_list_data"][0]["value"].lower() for user in data}

# Analyze followers and find non-followers
def analyze_followers(following_data, followers_data):
    following_set = extract_usernames(following_data, is_following=True)
    followers_set = extract_usernames(followers_data, is_following=False)
    non_followers = following_set - followers_set
    non_follower_links = []
    for user in following_data["relationships_following"]:
        username = user["string_list_data"][0]["value"].lower()
        if username in non_followers:
            non_follower_links.append((username, user["string_list_data"][0]["href"]))
    return sorted(non_follower_links)

# Load and analyze pending requests
def load_pending_requests(filename):
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['relationships_follow_requests_sent']

def format_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def analyze_pending_requests(requests):
    pending_list = []
    for req in requests:
        user_data = req['string_list_data'][0]
        pending_list.append((user_data['value'], user_data['href'], format_timestamp(user_data['timestamp'])))
    return sorted(pending_list, key=lambda x: x[2], reverse=True)

# Open profile link
def open_link(url):
    webbrowser.open(url)

# Create GUI
root = tk.Tk()
root.title("UnfollowMate : Instagram Tool")
root.configure(bg='#121212')
root.state('zoomed')

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background='#121212', borderwidth=2)
style.configure("TNotebook.Tab", background='#333333', foreground='white', padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#FF5733")])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

frame1 = tk.Frame(notebook, bg='#121212')
frame2 = tk.Frame(notebook, bg='#121212')
notebook.add(frame1, text='  Unfollowers  ')
notebook.add(frame2, text='  Pending Requests  ')

# Unfollowers List
unfollow_label = tk.Label(frame1, text="People who don't follow you back:", font=("Arial", 18, "bold"), fg='white', bg='#121212')
unfollow_label.pack(pady=10)

unfollow_canvas = tk.Canvas(frame1, bg='#121212')
unfollow_scroll = ttk.Scrollbar(frame1, orient='vertical', command=unfollow_canvas.yview)
unfollow_frame = tk.Frame(unfollow_canvas, bg='#121212')
unfollow_canvas.create_window((0, 0), window=unfollow_frame, anchor='nw')
unfollow_canvas.configure(yscrollcommand=unfollow_scroll.set)

unfollow_scroll.pack(side='right', fill='y')
unfollow_canvas.pack(side='left', fill='both', expand=True)

def populate_unfollowers():
    try:
        following_data = load_json('following.json')
        followers_data = load_json('followers_1.json')
        non_followers = analyze_followers(following_data, followers_data)
        for idx, (username, url) in enumerate(non_followers, 1):
            row = tk.Frame(unfollow_frame, bg='#121212')
            row.pack(fill='x', pady=5)
            label = tk.Label(row, text=f"{idx}. {username}", font=("Arial", 14), fg='white', bg='#121212')
            label.pack(side='left', padx=10)
            button = tk.Button(row, text="Unfollow", command=lambda u=url: open_link(u), bg='#FF5733', fg='white', font=("Arial", 12, "bold"), relief='flat')
            button.pack(side='right', padx=10)
    except Exception as e:
        print(f"Error loading unfollowers: {str(e)}")

# Pending Requests List
pending_label = tk.Label(frame2, text="Pending Follow Requests:", font=("Arial", 18, "bold"), fg='white', bg='#121212')
pending_label.pack(pady=10)

pending_canvas = tk.Canvas(frame2, bg='#121212')
pending_scroll = ttk.Scrollbar(frame2, orient='vertical', command=pending_canvas.yview)
pending_frame = tk.Frame(pending_canvas, bg='#121212')
pending_canvas.create_window((0, 0), window=pending_frame, anchor='nw')
pending_canvas.configure(yscrollcommand=pending_scroll.set)

pending_scroll.pack(side='right', fill='y')
pending_canvas.pack(side='left', fill='both', expand=True)

def populate_pending_requests():
    try:
        requests = load_pending_requests('pending_follow_requests.json')
        pending_list = analyze_pending_requests(requests)
        for idx, (username, url, date) in enumerate(pending_list, 1):
            row = tk.Frame(pending_frame, bg='#121212')
            row.pack(fill='x', pady=5)
            label = tk.Label(row, text=f"{idx}. {username} (Requested on {date})", font=("Arial", 14), fg='white', bg='#121212')
            label.pack(side='left', padx=10)
            button = tk.Button(row, text="View Profile", command=lambda u=url: open_link(u), bg='#FF5733', fg='white', font=("Arial", 12, "bold"), relief='flat')
            button.pack(side='right', padx=10)
    except Exception as e:
        print(f"Error loading pending requests: {str(e)}")

populate_unfollowers()
populate_pending_requests()

footer = tk.Label(root, text="Made with ❤ by Tanish Poddar", font=("Arial", 12), fg='red', bg='#121212')
footer.pack(side='bottom', pady=5)

root.mainloop()