# GH-CRIZ OMNI TOOL

A professional workspace manager for GitHub with integrated system monitoring and automation features.

## Features

- Pulse Heartbeat: Automated health logging to pulse.log.
- Network Sync: Automatic following based on keywords and unfollowing non-followers.
- Tech Scout: Real-time search for trending repositories in Laravel and JavaScript.
- System Monitor: Live display of CPU, RAM, and disk usage for PISCES Laptop.

## Technical Stack

- Python 3.10+
- PyGithub
- rich
- psutil

## Installation

1. Install dependencies:
   pip install -r requirements.txt

2. Set the GitHub Token environment variable:
   set GH_TOKEN=your_personal_access_token

3. Run the application:
   python main.py

## Usage Flags

- --auto: Executes the Pulse Heartbeat and exits immediately.
