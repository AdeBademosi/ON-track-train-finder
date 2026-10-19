# importing necessary libraries
import csv
import os 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta 
import time
import threading

# defining necessary functions
# Load CSV file into a dictionary
def load_csv_dict():
    # Automatically get path to CSV in the same folder as this script
    base_dir = os.path.dirname(__file__)
    filename = os.path.join(base_dir, "Timetable.csv")

    # Read the CSV
    timetable_data = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row["Date"].strip()
            timetable_data[date] = {}
            for train_label, time in row.items():
                if train_label != "Date":
                    timetable_data[date][train_label] = time
    return timetable_data

#run the program
def run_program():
    train_dict = load_csv_dict()
    main_menu(train_dict)
train_dict = load_csv_dict()

#admin codes 
def verify_admin_code(input_code):
    with open("admin_codes.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["code"].strip() == input_code.strip():
                return True
    return False

#get greeting 
now = datetime.now()
hour = datetime.now().hour 
def get_greeting(hour):
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Hello"
    return greeting

greeting = get_greeting(hour)

# Get today's date
today = datetime.now().strftime("%d/%m/%Y")
print("Today's date:", today)
print("All timetable dates:", list(train_dict.keys())[:5])

# pree enter to continue function
def press_enter_to_continue():
    input("\nPress Enter to return to menu...")

#Choice 1
def print_arrival_times(data):
                while True:
                    print("\n--- Arrival Times Menu ---")
                    print("1. View Today's Train Times")
                    print("2. View Full Train Schedule")
                    print("3. View Timetable for a Specific Train")
                    print("4. Back to Main Menu")


                    choice_1 = input("Enter your choice (1–4): ")

#choice 1_1
                    if choice_1 == "1":
                        if today in train_dict:
                            print("Today's train times:")
                            for train, time in train_dict[today].items():
                                print(f"{train}: {time}")
                        else:
                            print("No trains scheduled for today.")
                        press_enter_to_continue()


#choice 1_2
                    elif choice_1 == "2":
                        for date, trains in train_dict.items():
                            print(f"{date}: {trains}")
                        press_enter_to_continue()

#choice 1_3
                    elif choice_1 == "3":
                        print("\n--- Search Train Schedule ---")
                        train_number = input("Enter train number (1–5): ").strip()
                        train_key = f"Train {train_number}"

                        date_input = input("Enter date (dd/mm/yyyy) or press Enter to view full schedule: ").strip()

                        if date_input:
                            if date_input in data and train_key in data[date_input]:
                                time = data[date_input][train_key]
                                print(f"{train_key} arrives at {time} on {date_input}")
                            else:
                                print(f"No schedule found for {train_key} on {date_input}")
                        else:
                            print(f"\nFull schedule for {train_key}:")
                            found = False
                            for date, trains in data.items():
                                if train_key in trains:
                                    print(f"{date} - {trains[train_key]}")
                                    found = True
                            if not found:
                                print(f"No records found for {train_key}")

                        press_enter_to_continue()

#choice 1_4
                    elif choice_1 == "4":
                        break 
                    else:
                        print("Invalid choice. Please enter 1,2,3 or 4.")


#Choice 2
def manage_timetable(data):
                while True:
                    print("\n--- Manage Timetable Menu ---")
                    print("1. Search for Specific Train by Date and Time")
                    print("2. Update Arrival Times")
                    print("3. Back to Main Menu")

                    choice_2 = input("Enter your choice (1–3): ")
                    if choice_2 == "1":
                        specific_train(data)
                        press_enter_to_continue()
                    elif choice_2 == "2":
                        update_arrival_time(data)
                        press_enter_to_continue()
                    elif choice_2 == "3":
                        break 
                    else:
                        print("Invalid choice. Please enter 1, 2 or 3.")


#choice 2_1

def specific_train(data):
    print("\n--- Search Available Trains from a Fixed Time ---")
    date_input = input("Enter start date (dd/mm/yyyy): ").strip()
    time_input = input("Enter the time to search from (HH:MM, 24-hour): ").strip()

    try:
        current_date = datetime.strptime(date_input, "%d/%m/%Y")
        fixed_time = datetime.strptime(time_input, "%H:%M").time()
    except ValueError:
        print("Invalid date or time format. Please try again.")
    else:
        while True:
            date_key = current_date.strftime("%d/%m/%Y")
            print(f"\nTrains available on {date_key} from {fixed_time.strftime('%H:%M')}:\n")

            if date_key in train_dict:
                found = False
                for train, arrival_time in train_dict[date_key].items():
                    try:
                        train_time = datetime.strptime(arrival_time, "%H:%M").time()
                        if train_time >= fixed_time:
                            print(f"{train} - {arrival_time}")
                            found = True
                    except:
                        continue
                if not found:
                    print("No trains available at or after that time on this day.")
            else:
                print("No trains scheduled for this date.")

            next_day = input("\nPress Enter to check the next day or type 'q' to return to the menu: ").strip().lower()
            if next_day == "q":
                break
            current_date += timedelta(days=1)

#choice 2_2                 
def update_arrival_time(data):
    code = input("Enter admin access code: ").strip()
    if verify_admin_code(code):
        print("Access granted.")
        date = input("Enter the date (dd/mm/yyyy): ").strip()
        if date not in data:
            print("Date not found in timetable.")
            return

        train_key = input("Enter train number (1–5): ").strip()
        train_key = f"Train {train_key}"

        if train_key not in data[date]:
            print(f"{train_key} not found on {date}.")
            return

        new_time = input(f"Enter new arrival time for {train_key} on {date} (HH:MM): ").strip()
        data[date][train_key] = new_time
        print(f"Updated: {train_key} now arrives at {new_time} on {date}")
        save_dict_to_csv(data)
    else:
        print("Access denied.")
        return

def save_dict_to_csv(data, filename="Timetable.csv"):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, filename)

        # Safely get fieldnames based on a sample date entry
        fieldnames = ["Date"]
        if data:
            sample_day = next(iter(data.values()))
            fieldnames += list(sample_day.keys())

        with open(file_path, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for date, train_times in data.items():
                row = {"Date": date}
                row.update(train_times)
                writer.writerow(row)
    

#choice 3
def setup_graph(title):
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=14, weight="bold", color="white")
    ax.set_xlabel("Date", fontsize=12, color="white")
    ax.set_ylabel("Arrival Time", fontsize=12, color="white")
    ax.tick_params(colors='white', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    return ax
                            
def analyse_timetable(data):
    while True:
        print("\n--- Analyse Timetable Menu ---")
        print("1. View Monthly Arrival Times Graph ")
        print("2. View Arrival Times of Specific Train")
        print("3. Back to Main Menu")
        choice_3 = input("Enter your choice (1–4): ")
        if choice_3 == "1":
                monthly_arrival_times(data)
                press_enter_to_continue()
        elif choice_3 == "2":
                specific_train_arrival_times(data)
                press_enter_to_continue()
        elif choice_3 == "3":
                break
        else:
                print("Invalid choice. Please enter 1, 2, or 3")

#choice 3_1
def monthly_arrival_times(data):
    month_input = input("Enter the month number (e.g. 01 for January, 05 for May): ").strip()

    try:
        selected_month = int(month_input)
        if selected_month < 1 or selected_month > 12:
            print("Invalid month. Please enter a number between 01 and 12.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric month.")
        return

    dates = []
    times = []

    for date, trains in data.items():
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y")
            if date_obj.month == selected_month:
                for time_str in trains.values():
                    try:
                        dt_obj = datetime.strptime(f"{date} {time_str}", "%d/%m/%Y %H:%M")
                        dates.append(dt_obj)
                        times.append(datetime.combine(datetime.today(), dt_obj.time()))
                    except:
                        continue
        except:
            continue

    if not dates:
        print(f"No train records found for month {month_input}.")
        return

    # Sort dates
    sorted_data = sorted(zip(dates, times), key=lambda x: x[0])
    sorted_dates = [d for d, _ in sorted_data]
    sorted_times = [t for _, t in sorted_data]
    month_name = datetime(1900, selected_month, 1).strftime("%B")
    ax = setup_graph(f"Train Arrivals for Month {month_name}")
    ax.plot(sorted_dates, sorted_times, color='deepskyblue', linewidth=2)
    ax.scatter(sorted_dates, sorted_times, color='yellow', s=50, zorder=5)

    plt.tight_layout()
    plt.show()

#choice 3_2
def specific_train_arrival_times(data):
    train_input = input("Enter train number (1–5): ").strip()

    if not train_input.isdigit():
        print("Invalid input. Please enter a number like 1, 2, 3, etc.")
        return

    train_key = f"Train {train_input}"
    dates, times = [], []

    for date, trains in data.items():
        if train_key in trains:
            try:
                time_str = trains[train_key]
                dt_obj = datetime.strptime(f"{date} {time_str}", "%d/%m/%Y %H:%M")
                dates.append(dt_obj)
                times.append(datetime.combine(datetime.today(), dt_obj.time()))
            except:
                continue

    if not dates:
        print(f"No arrival times found for {train_key}.")
        return

    ax = setup_graph(f"Arrival Times for {train_key}")
    ax.plot(dates, times, color='deepskyblue', linewidth=2)

    plt.tight_layout()
    plt.show()


#Choice 4
def set_schedules(data):
    def run_alert(date_str, train_label, train_time_str):
        alerts_sent = set()
        print(f"\nAlert active for {train_label} on {date_str} at {train_time_str}")
        print("Press Ctrl+C in terminal to stop manually.\n")

        try:
            while True:
                now = datetime.now()
                current_date_str = now.strftime("%d/%m/%Y")

                if current_date_str != date_str:
                    break  # Stop if the date has passed

                try:
                    arrival_time = datetime.strptime(f"{date_str} {train_time_str}", "%d/%m/%Y %H:%M")
                    minutes_to_arrival = int((arrival_time - now).total_seconds() // 60)

                    if minutes_to_arrival in [10, 5, 1] and minutes_to_arrival >= 0:
                        if minutes_to_arrival not in alerts_sent:
                            if minutes_to_arrival == 10:
                                print("\nYour train is here in 10 mins")
                            elif minutes_to_arrival == 5:
                                print("\nGet ready! Your train is here in 5 mins")
                            elif minutes_to_arrival == 1:
                                print("\nHurry! Your train has arrived. Prepare to depart.")
                            alerts_sent.add(minutes_to_arrival)
                except Exception as e:
                    print(f"Error checking train time: {e}")

                time.sleep(30)
        except KeyboardInterrupt:
            print("\nAlert stopped manually.")

    # === User Input ===
    date_input = input("Enter date (dd/mm/yyyy): ").strip()
    time_input = input("Start checking from what time? (HH:MM, 24-hour): ").strip()

    try:
        start_datetime = datetime.strptime(f"{date_input} {time_input}", "%d/%m/%Y %H:%M")
    except ValueError:
        print("Invalid date or time format.")
        return

    # === Build list of next 5 train options ===
    upcoming_trains = []

    sorted_dates = sorted(data.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
    for date in sorted_dates:
        for train_label, time_str in data[date].items():
            try:
                train_dt = datetime.strptime(f"{date} {time_str}", "%d/%m/%Y %H:%M")
                if train_dt >= start_datetime:
                    upcoming_trains.append((date, train_label, time_str, train_dt))
            except:
                continue
        if len(upcoming_trains) >= 5:
            break

    if not upcoming_trains:
        print("No upcoming trains found.")
        return

    # Sort and pick the first 5
    upcoming_trains.sort(key=lambda x: x[3])
    options = upcoming_trains[:5]

    print("\nNext available trains:")
    letter_map = {}
    for idx, (d, label, time_str, _) in enumerate(options):
        letter = chr(ord('A') + idx)
        letter_map[letter] = (d, label, time_str)
        print(f"{letter}. {d} {label} at {time_str}")

    # User selects train
    choice = input("\nWhich train do you want to set an alert for? (A–E): ").strip().upper()
    if choice not in letter_map:
        print("Invalid selection.")
        return

    chosen_date, chosen_label, chosen_time = letter_map[choice]
    thread = threading.Thread(target=run_alert, args=(chosen_date, chosen_label, chosen_time), daemon=True)
    thread.start()
    press_enter_to_continue()




#Building Main Menu
#main menu
def main_menu(data):
    train_dict = load_csv_dict()
    while True:
        print(f"{greeting}, Let's get you moving.")
        print("\n--- OnTrack Main Menu ---")
        print("1. Print Arrival Times")
        print("2. Manage Timetable")
        print("3. Analyse Timetable")
        print("4. Set Schedules")
        print("5. Quit Application")
        
        choice = input("Enter your choice (1–5): ")
#choice 1
        if choice == "1": 
            print_arrival_times(train_dict)
            

#choice 2
        elif choice == "2":
            manage_timetable(train_dict)
            
            
#choice 3
        elif choice == "3":
            analyse_timetable(train_dict)
            
#choice 4
        elif choice == "4":
            print("---Set Schedules---")
            set_schedules(train_dict)
            
#choice 5
        elif choice == "5":
            print("See you soon!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    run_program()

