"""
Utility Functions
"""

from datetime import datetime


def print_header(title):
    print("=" * 60)
    print(title.upper())
    print("=" * 60)


def print_success(message):
    print(f"{message}")


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")