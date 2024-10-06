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
    def __init__(self, delay, command):
        self.command = command
        self.delay = delay
        self.last_modified = time.time()
        self.timer = None
        print(f"Handler initialized with delay={delay} and command={command}")

    def on_any_event(self, event):
        print(f"Detected change in: {event.src_path}")
        # Cập nhật thời gian khi có sự kiện thay đổi
        self.last_modified = time.time()

        if self.timer is not None:
            self.timer.cancel()

        # Tạo và bắt đầu timer
        self.timer = threading.Timer(1, self.countdown, args=[self.delay])
        self.timer.start()

    def countdown(self, countdown_time):
        print(f"Countdown started: {countdown_time} seconds")
        for i in range(countdown_time, 0, -1):
            print(f"Command will be executed in {i} seconds...", end='\r')
            time.sleep(1)

        self.execute_command()

    def execute_command(self):
        # Kiểm tra nếu không có thay đổi nào thêm trong khoảng delay
        if time.time() - self.last_modified >= self.delay:
            print(f"\nExecuting command: {self.command}")
            subprocess.call(self.command, shell=True)

"""
Example usage:
    python monitor.py /path/to/folder "echo 'Folder has changed'" --delay 5
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor folder changes and execute a command after a delay.")
    parser.add_argument("folder", type=str, help="Folder to monitor")
    parser.add_argument("command", type=str, help="Command to execute when files change")
    parser.add_argument("--delay", type=int, default=5, help="Delay in seconds before executing the command (default: 5 seconds)")

    args = parser.parse_args()

    path_to_watch = args.folder  # Thư mục giám sát
    command_to_run = args.command  # Lệnh thực thi
    delay_in_seconds = args.delay  # Khoảng thời gian chờ

    print(f"Monitoring folder: {path_to_watch}")
    print(f"Command to run: {command_to_run}")
    print(f"Delay set to: {delay_in_seconds} seconds")

    event_handler = ChangeHandler(delay=delay_in_seconds, command=command_to_run)
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
