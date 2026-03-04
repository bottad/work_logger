import csv
import json
from datetime import datetime, timedelta
import os
import platform
from collections import defaultdict
from pathlib import Path

# CHANGE TO YOUR NEEDS
TOTAL_HOLIDAYS = 19  # Total number of holiday days allowed
PENSUM = 42 * 0.9  # Weekly pensum in hours
WORKDAYS = 5  # Monday to Friday (5 workdays)

#######################################
# DO NOT CHANGE ANITHING BEYOND HERE! #
#######################################

BASE_DIR = Path(__file__).resolve().parent

# Filepaths
FILE_NAME = BASE_DIR / "data" / "work_hours.csv"
STATE_FILE = BASE_DIR / "data" / "work_state.json"
HOLIDAY_FILE = BASE_DIR / "data" / "holiday_state.json"

# Global variables to store times
start_time = None
break_start_time = None
total_break_duration = timedelta()
used_holidays = 0

# Function that clears the console for cleaner seperation of the main menu and the log display
def clear_console():
    # Check the OS type and clear the console accordingly
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Function to save current state to a file
def save_state():
    global start_time, break_start_time, total_break_duration
    state = {
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else None,
        "break_start_time": break_start_time.strftime('%Y-%m-%d %H:%M:%S') if break_start_time else None,
        "total_break_duration": total_break_duration.total_seconds()
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

# Function to load the saved state from a file
def load_state():
    global start_time, break_start_time, total_break_duration
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            if state["start_time"]:
                start_time = datetime.strptime(state["start_time"], '%Y-%m-%d %H:%M:%S')
            if state["break_start_time"]:
                break_start_time = datetime.strptime(state["break_start_time"], '%Y-%m-%d %H:%M:%S')
            total_break_duration = timedelta(seconds=state["total_break_duration"])

# Function to delete the saved state file (after work day ends)
def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

# Function to start working (logs the start time)
def start_work():
    global start_time
    if start_time is None:
        start_time = datetime.now()
        print(f"Started working at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        save_state()
    else:
        print("You have already started work!")

# Function to stop working and calculate time worked
def stop_work():
    global start_time, total_break_duration
    if start_time is None:
        print("You haven't started work yet!")
        return

    end_time = datetime.now()
    total_time = end_time - start_time - total_break_duration
    hours_worked = total_time.total_seconds() / 3600
    print(f"Stopped working at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time worked (excluding breaks): {hours_worked:.2f} hours")
    
    log_work(start_time, end_time, hours_worked)
    
    clear_state()

# Function to start a break
def start_break():
    global break_start_time
    if break_start_time is None:
        break_start_time = datetime.now()
        print(f"Started break at {break_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        save_state()
    else:
        print("You are already on a break!")

# Function to end a break
def end_break():
    global break_start_time, total_break_duration
    if break_start_time is not None:
        break_end_time = datetime.now()
        break_duration = break_end_time - break_start_time
        total_break_duration += break_duration
        print(f"Ended break at {break_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total break time: {break_duration.total_seconds() / 60:.2f} minutes")
        break_start_time = None
        save_state()
    else:
        print("You haven't started a break yet!")

# Function to log the working hours to a CSV file
def log_work(start_time, end_time, hours_worked, description=None):
    if description == "Holiday":
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([start_time.strftime('%Y-%m-%d'), "Holiday", "Holiday", f"{hours_worked:.2f}"])
    else:
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([start_time.strftime('%Y-%m-%d'), start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S'), f"{hours_worked:.2f}"])
    print(f"Work logged for {start_time.strftime('%Y-%m-%d')}")

# Function to manually start work
def manual_start_work():
    global start_time

    clear_console()

    today = datetime.now().date()
    start_time_str = input("Enter the start time (HH:MM): ")
    start_time = datetime.combine(today, datetime.strptime(start_time_str, '%H:%M').time())
    save_state()
    print(f"Manual work started on {today} at {start_time.time()}.")

# Function to manually end work
def manual_end_work():
    global start_time, total_break_duration

    clear_console()

    if start_time is None:
        print("No work start entry found!")
        return

    end_time_str = input("Enter the end time (HH:MM): ")
    end_time = datetime.combine(datetime.now().date(), datetime.strptime(end_time_str, '%H:%M').time())

    total_time = (end_time - start_time) - total_break_duration
    hours_worked = total_time.total_seconds() / 3600

    log_work(start_time, end_time, hours_worked)
    clear_state()

    print(f"Manual work ended at {end_time.time()}. Total hours worked: {hours_worked:.2f}.")

# Function to manually start break
def manual_start_break():
    global break_start_time

    clear_console()

    today = datetime.now().date()
    start_time_str = input("Enter the start time for break (HH:MM): ")
    break_start_time = datetime.combine(today, datetime.strptime(start_time_str, '%H:%M').time())
    
    save_state()
    print(f"Manual break started on {today} at {break_start_time.time()}.")

# Function to manually end break
def manual_end_break():
    global break_start_time, total_break_duration

    clear_console()

    today = datetime.now().date()
    end_time_str = input("Enter the end time for break (HH:MM): ")
    end_time = datetime.combine(today, datetime.strptime(end_time_str, '%H:%M').time())

    if break_start_time:
        hours = (end_time - break_start_time).total_seconds() / 3600  # Calculate break duration
        total_break_duration += timedelta(hours=hours)
        break_start_time = None
        
        save_state()
        print(f"Manual break ended on {today} at {end_time.time()}. Total break duration: {hours:.2f} hours.")
    else:
        print("No break start entry found for today.")

# Function to manually log work for a past day
def manual_log():
    clear_console()
    try:
        date_str = input("Enter the date for the work log (YYYY-MM-DD): ")
        start_time_str = input("Enter start time (HH:MM): ")
        end_time_str = input("Enter end time (HH:MM): ")

        work_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_time = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')

        break_time_minutes = input("Enter total break time in minutes (optional, press Enter to skip): ")
        break_time = timedelta(minutes=int(break_time_minutes)) if break_time_minutes else timedelta()

        total_time = end_time - start_time - break_time
        hours_worked = total_time.total_seconds() / 3600

        log_work(start_time, end_time, hours_worked)
        print(f"Manually logged {hours_worked:.2f} hours for {work_date.strftime('%Y-%m-%d')}")

    except ValueError as e:
        print(f"Error: {e}. Please enter the date and times in the correct format.")

# Function to save holiday state to a file
def save_holiday_state():
    global used_holidays
    with open(HOLIDAY_FILE, 'w') as f:
        json.dump({"used_holidays": used_holidays}, f)

# Function to load the holiday state from a file
def load_holiday_state():
    global used_holidays
    if os.path.exists(HOLIDAY_FILE):
        with open(HOLIDAY_FILE, 'r') as f:
            state = json.load(f)
            used_holidays = state.get("used_holidays", 0)
    else:
        used_holidays = 0

# Function to manually log a holiday
def manual_log_holiday():
    global used_holidays

    clear_console()

    if used_holidays >= TOTAL_HOLIDAYS:
        print("You have used all your available holiday days.")
        return

    date_str = input("Enter the date for the holiday (YYYY-MM-DD): ")

    try:
        holiday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        hours_worked = PENSUM / WORKDAYS

        log_work(holiday_date, holiday_date, hours_worked, description="Holiday")

        used_holidays += 1
        save_holiday_state()

        print(f"Holiday logged for {holiday_date.strftime('%Y-%m-%d')}. You have {TOTAL_HOLIDAYS - used_holidays} holidays remaining.")

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# Function to view the work logs with weekly aggregation and pensum comparison
def view_work_log():
    clear_console()
    try:
        daily_hours = defaultdict(list)
        daily_breaks = defaultdict(list)  # To track daily break times in minutes
        weekly_hours = defaultdict(float)
        holidays = set()  # To keep track of holiday dates
        ill_days = set() # To keep track of ill dates

        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                date_str, start, end, hours = row[:4]
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

                # Check if the day is logged as a holiday
                if "Holiday" in row:
                    daily_hours[date].append(8.4)  # 8.4 hours for a holiday
                    holidays.add(date)  # Add the date to the holidays set
                elif "ill" in row:
                    daily_hours[date].append(8.4)  # 8.4 hours for a holiday
                    ill_days.add(date)  # Add the date to the holidays set
                else:
                    # Parse start and end times to calculate break
                    start_time = datetime.strptime(start, '%H:%M:%S')
                    end_time = datetime.strptime(end, '%H:%M:%S')
                    total_worked_time = (end_time - start_time).total_seconds() / 3600
                    break_time_minutes = (total_worked_time - float(hours)) * 60

                    daily_hours[date].append(float(hours))
                    daily_breaks[date].append(break_time_minutes)

                week_start = date - timedelta(days=date.weekday())  # Get the Monday of that week
                weekly_hours[week_start] += float(hours)

        # Print daily hours block-wise by week
        current_week = None
        total_hours_all_weeks = 0
        total_diff_all_weeks = 0 
        today = datetime.now().date()
        print("\nWeekly Work Log")
        print("-" * 50)

        for date in sorted(daily_hours.keys()):
            week_start = date - timedelta(days=date.weekday())  # Monday of the current week
            if current_week != week_start:
                if current_week is not None:
                    # Calculate the pensum for the week
                    if current_week == today - timedelta(days=today.weekday()):  # If it's the current week
                        # Determine how many weekdays (Mon-Fri) have passed, excluding today if not complete
                        days_worked = today.weekday()  # Monday = 0, Friday = 4
                        
                        # Check if today's work hours have been fully logged
                        if today in daily_hours:
                            today_hours = sum(daily_hours[today])
                            if today_hours > 0:
                                days_worked = today.weekday() + 1
                                
                        current_pensum = PENSUM * (days_worked / WORKDAYS)  # Adjust pensum for workdays
                    else:
                        current_pensum = PENSUM
                    
                    week_diff = weekly_hours[current_week] - current_pensum
                    total_diff_all_weeks += week_diff
                    sign = "+" if week_diff > 0 else ""
                    print(f"Total for week starting {current_week.strftime('%Y-%m-%d')}: "
                          f"{weekly_hours[current_week]:.2f} hours ({sign}{week_diff:.2f} hours)")
                    print("-" * 50)
                current_week = week_start

            if date in holidays:
                print(f"{date.strftime('%a, %Y-%m-%d')}: (free)")
            elif date in ill_days:
                print(f"{date.strftime('%a, %Y-%m-%d')}: (ill)")
            else:
                total_for_day = sum(daily_hours[date])
                total_break_for_day = sum(daily_breaks[date])
                print(f"{date.strftime('%a, %Y-%m-%d')}: {total_for_day:.2f} hours (Break: {total_break_for_day:.0f} minutes)")
            total_hours_all_weeks += total_for_day

        if current_week is not None:
            if current_week == today - timedelta(days=today.weekday()):
                days_worked = today.weekday()  # Monday = 0, Friday = 4

                if today in daily_hours:  # If today's hours are logged
                    today_hours = sum(daily_hours[today])
                    if today_hours > 0:
                        days_worked = today.weekday() + 1

                current_pensum = PENSUM * (days_worked / WORKDAYS)
            else:
                current_pensum = PENSUM

            week_diff = weekly_hours[current_week] - current_pensum
            total_diff_all_weeks += week_diff
            sign = "+" if week_diff > 0 else ""
            print(f"Total for week starting {current_week.strftime('%Y-%m-%d')}: "
                  f"{weekly_hours[current_week]:.2f} hours ({sign}{week_diff:.2f} hours)")

        # Summary
        print("-" * 50)
        overall_sign = "+" if total_diff_all_weeks > 0 else ""
        print(f"Total hours worked: {total_hours_all_weeks:.2f} hours")
        print(f"Overall difference from pensum: {overall_sign}{total_diff_all_weeks:.2f} hours")

        remaining_holidays = TOTAL_HOLIDAYS - used_holidays
        print(f"Remaining holidays: {remaining_holidays}")

    except FileNotFoundError:
        print("No work log found. Start logging your hours first.")

    input("\nPress Enter to return to the main menu...")
    clear_console()

# Main menu to navigate the program
def main_menu():
    clear_console()
    load_state()
    load_holiday_state()

    while True:
        print("\n--- Live Commands ---")
        print("1.  Start Work")
        print("2.  Stop Work")
        print("3.  Start Break")
        print("4.  End Break")

        print("\n--- Manual Commands ---")
        print("5.  Manually Start Work")
        print("6.  Manually Stop Work")
        print("7.  Manually Start Break")
        print("8.  Manually End Break")
        print("9.  Manual Log for a Past Day")
        print("10. Log a Holiday")

        print("\n--- View and Exit ---")
        print("11. View Work Log")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            start_work()
        elif choice == '2':
            stop_work()
        elif choice == '3':
            start_break()
        elif choice == '4':
            end_break()
        elif choice == '5':
            manual_start_work()
        elif choice == '6':
            manual_end_work()
        elif choice == '7':
            manual_start_break()
        elif choice == '8':
            manual_end_break()
        elif choice == '9':
            manual_log()
        elif choice == '10':
            manual_log_holiday()
        elif choice == '11':
            view_work_log()
        elif choice == '12':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

# Main call
if __name__ == "__main__":
    main_menu()