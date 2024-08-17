from flask import Blueprint, request, session
from datetime import datetime
import csv
import os

user_log_bp = Blueprint('user_log_bp', __name__)

# Define the path for the log file
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
excel_file = os.path.join(desktop_path, 'chatlogfile', 'user_logs.xlsx')
fieldnames = ['IP Address', 'Username', 'Login Time', 'Logout Time', 'Duration']

def log_user(username, ip_address, login_time, logout_time):
    os.makedirs(os.path.dirname(excel_file), exist_ok=True)
    with open(excel_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()

        if isinstance(login_time, datetime):
            login_time_str = login_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            login_time_str = ''

        if isinstance(logout_time, datetime):
            logout_time_str = logout_time.strftime('%Y-%m-%d %H:%M:%S')
            duration = str(logout_time - login_time)
        elif logout_time == 'Active':
            logout_time_str = 'Active'
            duration = 'Active'
        else:
            logout_time_str = ''
            duration = ''

        writer.writerow({
            'IP Address': ip_address,
            'Username': username,
            'Login Time': login_time_str,
            'Logout Time': logout_time_str,
            'Duration': duration
        })
