# On Track — Train Timetable Finder

A command-line Python application developed as a university programming project. It loads a sample train timetable from CSV and provides timetable lookup, editing, visualisation and scheduled alerts.

## Features

- Browse train arrival times and search by date and train.
- Find upcoming services based on a selected date and time.
- Edit timetable entries using a demonstration admin access code.
- Visualise train times using Matplotlib.
- Set in-session train reminders using a background thread.

## Requirements

- Python 3
- Matplotlib (`pip install -r requirements.txt`)

## Run locally

1. Download the repository files into the same directory.
2. Run `pip install -r requirements.txt`.
3. Run `python Main.py` (or `python3 Main.py`).
4. Follow the terminal menu.

For the demonstration admin-editing feature, the example code in `admin_codes.csv` is `DEMO2025`. **This is not secure authentication and is provided only for coursework demonstration.**

## Data and limitations

`Timetable.csv` is a static sample dataset covering 1 January through 31 December 2025, with five services per day. It is **not** a real-time railway schedule. Searches outside 2025 will not return matching dates. Reminder alerts run only while the application remains open; the existing code is a coursework implementation and has not been comprehensively tested across all edge cases.

## Project structure

- `Main.py` — original application source code.
- `Timetable.csv` — example train times for 2025.
- `admin_codes.csv` — non-sensitive demonstration code.
- `requirements.txt` — external Python dependency.

## Skills demonstrated

Python, CSV file processing, dictionaries, date/time handling, functions, sorting, Matplotlib and basic threading.

## Notes

This repository preserves the original coursework code, with the admin code replaced by a demonstration value. Future enhancements may include input validation, automated tests, and a revised upcoming-train search algorithm.
