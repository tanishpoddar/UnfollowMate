# UnfollowMate: Instagram Tool

## Overview
UnfollowMate is a Python-based GUI tool that helps you analyze your Instagram following and pending follow requests. It identifies:
- People you follow who don't follow you back.
- Pending follow requests that haven't been accepted.

## Features
- Displays a list of users who don't follow you back with direct links to their profiles for easy unfollowing.
- Shows pending follow requests along with timestamps.
- Provides a clean and user-friendly interface.

## Prerequisites
Ensure you have Python installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

## Installation
1. Clone the repository or download the source code.
   ```sh
   git clone https://github.com/your-username/UnfollowMate.git
   cd UnfollowMate
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## How to Get Instagram JSON Files
To use this tool, you need to download your Instagram data:

1. **Go to Instagram Settings:**
   - Open Instagram on your phone or desktop.
   - Navigate to **Settings > Privacy and Security**.
   - Scroll down to the **Data Download** section.
   - Click **Request Download**.
   
2. **Download Your Data:**
   - Instagram will send a download link to your registered email.
   - Extract the downloaded ZIP file.
   - Locate the following JSON files in the extracted folder:
     - `followers_1.json`
     - `following.json`
     - `pending_follow_requests.json`
   - Copy these files to the project directory.

## Running the Application
Once you have the necessary JSON files in the project directory, run the script:
```sh
python gui.py
```

## Usage
- The GUI will display two tabs:
  - **Unfollowers**: Shows people who don't follow you back.
  - **Pending Requests**: Lists sent follow requests that haven't been accepted.
- Click the **Unfollow** button to open the profile and manually unfollow.
- Click **View Profile** under the Pending Requests tab to visit a user’s profile.

## License
This project is open-source and available under the MIT License.

## Author
Developed by **Tanish Poddar**