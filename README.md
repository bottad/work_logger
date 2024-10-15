# Work Logger

This Python program is designed to track working hours, breaks, and holidays. It provides both real-time tracking and manual entry options, making it flexible for various workflows.

## Features

- **Start/Stop Work Sessions**: Automatically track your work hours and breaks.
- **Manual Logging**: Manually log work hours or breaks for current or past days.
- **Holiday Tracking**: Log holidays and track how many holiday days you have used.
- **View Work Log**: View work hours with weekly aggregation and compare with a weekly pensum (default 42 hours).
- **Save and Load State**: Work sessions are saved in case of program exit, so you can resume where you left off.

## Prerequisites

- Python 3.x

### Installation

1. Clone this repository:
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2. Make sure the `data` folder exists:
    ```
    data/
    ├── holiday_state.json (holiday counter created by the program)
    ├── work_hours.csv (work log created by the program)
    └── work_state.json (temporary file created by the program)
    ```

### Usage

Run the program with:
```bash
python work_logger.py
```

### Main Menu

Once the program is running, you can use the following options from the main menu:

#### Live Commands

1. **Start Work**: Begin a new work session.
2. **Stop Work**: End the current work session and calculate total hours worked (excluding breaks).
3. **Start Break**: Begin a break.
4. **End Break**: End the break and track the break duration.

#### Manual Commands

5. **Manually Start Work**: Log the start time manually.
6. **Manually Stop Work**: Log the end time manually.
7. **Manually Start Break**: Log a break start time manually.
8. **Manually End Break**: Log a break end time manually.
9. **Manual Log for a Past Day**: Enter work logs for a previous date.
10. **Log a Holiday**: Log a holiday (counts as 8.4 hours worked).

#### View and Exit

11. **View Work Log**: Display your work hours, grouped weekly, and compare against the pensum.
12. **Exit**: Exit the program.

### File Structure

The program uses the following files to store data:

- `data/work_hours.csv`: Stores the work logs in CSV format.
- `data/work_state.json`: Saves the current work session's state until this work day is finished (start time, break time).
- `data/holiday_state.json`: Tracks the number of holidays used.

### Example Workflow

#### Real Time:

1. Start your workday by selecting **Start Work**.
2. Take a break using **Start Break** and **End Break**.
3. End your workday by selecting **Stop Work**. Your hours will be logged automatically.
4. View your work logs and compare against the weekly pensum using **View Work Log**.

#### Manual:

Imagine you forgot to log your working hours or breaks for an entire day because you were working on-site without access to your computer. The next day, you want to ensure your times are accurately logged.

In this case, you can use the manual functions to retrospectively log the missing data. Here's how it would work:

1. **Manual Start Work**:
   You remember you started working at 09:00 AM yesterday. Instead of starting work in real-time, you can use the manual start function to log the start time for the previous day.
   
   **Command**: `Manually Start Work`

   **Input**: 
   ```
   Enter the start time (HH:MM): 09:00
   ```

2. **Manual Start Break**:
   You also recall taking a lunch break at 12:30 PM. You can log this using the manual start break function.

   **Command**: `Manually Start Break`

   **Input**:
   ```
   Enter the start time for break (HH:MM): 12:30
   ```

3. **Manual End Break**:
   After lunch, you ended your break at 1:15 PM. Use the manual end break function to log the end of your break.

   **Command**: `Manually End Break`

   **Input**:
   ```
   Enter the end time for break (HH:MM): 13:15
   ```

4. **Manual End Work**:
   Finally, you remember finishing your work day at 5:30 PM. You can use the manual end work function to log the end of your working hours.

   **Command**: `Manually End Work`

   **Input**:
   ```
   Enter the end time (HH:MM): 17:30
   ```

### Customization

- The default pensum is 42 hours per week, and holidays are logged as 8.4 hours per day.
- You can change the pensum and holiday values by modifying the respective variables inside the program (`PENSUM` and `TOTAL_HOLIDAYS`).

### Data Backup

Make sure to back up the `data/work_hours.csv` file regularly to avoid losing your work log history.

### License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software, provided that the original license and copyright notice are included in all copies or substantial portions of the software.