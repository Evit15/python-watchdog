import time
import threading
import argparse
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    """
    A handler class that responds to file system events with a delay and executes a command.
    Attributes:
        command (str): The command to be executed after the delay.
        delay (int): The delay in seconds before executing the command.
        last_modified (float): The timestamp of the last detected change.
        timer (threading.Timer): The timer object used to manage the delay.
    Methods:
        on_any_event(event):
            Responds to any file system event by resetting the timer and updating the last modified time.
        countdown(countdown_time):
            Starts a countdown and executes the command if no further changes are detected during the delay.
        execute_command():
            Executes the specified command if no changes have been detected within the delay period.
    """
    def __init__(self, delay, commands):
        self.commands = commands  # List of commands
        self.delay = delay
        self.last_modified = time.time()
        self.timer = None
        print(f"Handler initialized with delay={delay} and commands={commands}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            self.trigger_event()

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.trigger_event()

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            self.trigger_event()

    def trigger_event(self):
        # Update the last modified time when an event occurs
        self.last_modified = time.time()

        if self.timer is not None:
            self.timer.cancel()

        # Create and start the timer
        self.timer = threading.Timer(1, self.countdown, args=[self.delay])
        self.timer.start()

    def countdown(self, countdown_time):
        print(f"Countdown started: {countdown_time} seconds")
        for i in range(countdown_time, 0, -1):
            print(f"Commands will be executed in {i} seconds...", end='\r')
            time.sleep(1)

        self.execute_commands()

    def execute_commands(self):
        # Check if no changes occurred during the delay
        if time.time() - self.last_modified >= self.delay:
            for command in self.commands:
                print(f"\nExecuting command: {command}")
                subprocess.call(command, shell=True)

"""
Example usage:
    python monitor.py --folder /path/to/folder --commands "echo 'First command'" "echo 'Second command'" --delay 5
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor folder changes and execute commands after a delay.")
    parser.add_argument("--folder", type=str, help="Folder to monitor")
    parser.add_argument("--commands", type=str, nargs='+', help="Commands to execute when files change")
    parser.add_argument("--delay", type=int, default=5, help="Delay in seconds before executing the commands (default: 5 seconds)")

    args = parser.parse_args()

    path_to_watch = args.folder  # Thư mục giám sát
    commands_to_run = args.commands  # Danh sách lệnh thực thi
    delay_in_seconds = args.delay  # Khoảng thời gian chờ

    print(f"Monitoring folder: {path_to_watch}")
    print(f"Commands to run: {commands_to_run}")
    print(f"Delay set to: {delay_in_seconds} seconds")

    event_handler = ChangeHandler(delay=delay_in_seconds, commands=commands_to_run)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    
    print(f"Starting observer...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
        observer.stop()

    observer.join()
