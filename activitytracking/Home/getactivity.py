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
    try:
        arr=[]
        while True:
            active_window_name = get_active_window_name()
            active_process_name = get_active_process_name()
            if active_window_name and active_process_name:
                if active_window_name!=arr[-1]:
                    arr.append(active_window_name)
            time.sleep(interval)
        return arr
    except KeyboardInterrupt:
        return []

# active_window_name
#active_process_name