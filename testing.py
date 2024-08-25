import psutil
import time
import platform
import subprocess

def get_active_window_name():
    if platform.system() == 'Windows':
        import win32gui
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    elif platform.system() == 'Darwin':  # macOS
        from AppKit import NSWorkspace
        return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
    elif platform.system() == 'Linux':
        # Get the ID of the currently active window
        result = subprocess.run(['xprop', '-root', '_NET_ACTIVE_WINDOW'], capture_output=True, text=True)
        window_id = result.stdout.split()[-1]
        # Get the name of the window with the given ID
        result = subprocess.run(['xprop', '-id', window_id, 'WM_NAME'], capture_output=True, text=True)
        return result.stdout.split('=', 1)[-1].strip().strip('"')
    return None

def get_active_process_name():
    if platform.system() == 'Windows':
        import win32process
        import win32gui
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    elif platform.system() in ['Darwin', 'Linux']:
        try:
            # Get the PID of the current process
            pid = os.getpid()
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
