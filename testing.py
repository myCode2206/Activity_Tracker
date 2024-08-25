import psutil
import win32gui
import win32process
import time

def get_active_window_name():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def get_active_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def track_active_applications(interval=5):
    print("Tracking active applications... Press Ctrl+C to stop.\n")
    try:
        while True:
            active_window_name = get_active_window_name()
            active_process_name = get_active_process_name()
            if active_window_name and active_process_name:
                print(f"Active Window: {active_window_name} | Process: {active_process_name}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nTracking stopped.")

if __name__ == "__main__":
    track_active_applications()