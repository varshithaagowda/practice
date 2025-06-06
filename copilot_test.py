import os
import time
import platform

def get_uptime():
    if platform.system() == "Windows":
        # For Windows, uptime can be calculated using 'net stats srv'
        try:
            import subprocess
            output = subprocess.check_output("net stats srv", shell=True, text=True)
            for line in output.splitlines():
                if line.lower().startswith("statistics since"):
                    # Parse the uptime start time
                    from datetime import datetime
                    start_time = line.split("since", 1)[1].strip()
                    # Convert to datetime object
                    boot_time = datetime.strptime(start_time, "%m/%d/%Y %I:%M:%S %p")
                    # Calculate uptime
                    uptime_seconds = (datetime.now() - boot_time).total_seconds()
                    return int(uptime_seconds)
        except Exception as e:
            return f"Error retrieving uptime on Windows: {e}"
    elif platform.system() == "Linux":
        # On Linux, read from /proc/uptime
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return int(uptime_seconds)
        except Exception as e:
            return f"Error retrieving uptime on Linux: {e}"
    elif platform.system() == "Darwin":
        # For macOS, use sysctl kern.boottime
        try:
            import subprocess
            output = subprocess.check_output(['sysctl', '-n', 'kern.boottime'], text=True)
            import re
            m = re.search(r'{ sec = (\d+),', output)
            if m:
                boot_time = int(m.group(1))
                uptime_seconds = int(time.time()) - boot_time
                return uptime_seconds
            else:
                return "Could not parse kern.boottime"
        except Exception as e:
            return f"Error retrieving uptime on macOS: {e}"
    else:
        return "Unsupported OS"

def main():
    uptime = get_uptime()
    if isinstance(uptime, int):
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"System uptime: {hours} hours, {minutes} minutes, {seconds} seconds")
    else:
        print(uptime)

if __name__ == "__main__":
    main()
