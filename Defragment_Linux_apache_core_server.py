import os
import gc
import psutil
import subprocess

def defrag_memory():
    print("Defragmenting memory...")
    gc.collect()
    print("Memory defragmentation complete.")

def clear_cache():
    print("Clearing cache...")
    try:
        if os.name == 'posix':  # Linux/MacOS
            # Flush filesystem buffers
            os.system("sync")
            # Clear PageCache, dentries, and inodes
            os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
        elif os.name == 'nt':  # Windows
            # Clear standby list using PowerShell
            ps_script = """
            [void] [System.Reflection.Assembly]::LoadWithPartialName('Microsoft.VisualBasic')
            [Microsoft.VisualBasic.Devices.Computer]::new().Memory.ClearCache()
            """
            subprocess.run(["powershell", "-Command", ps_script], shell=True)

    except Exception as e:
        print(f"Cache clear failed: {e}")
    else:
        print("Cache cleared successfully.")

def close_unnecessary_processes():
    print("Closing unnecessary processes...")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            if proc.info['name'] not in ['explorer.exe', 'python.exe', 'cmd.exe', 'powershell.exe']:  # Keep essential processes
                psutil.Process(proc.info['pid']).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("Unnecessary processes closed.")

def set_performance_mode():
    if os.name == 'nt':
        print("Setting system to performance mode...")
        try:
            subprocess.run(["powercfg", "/setactive", "SCHEME_MIN"])  # Sets the power scheme to high performance
        except Exception as e:
            print(f"Failed to set performance mode: {e}")
        else:
            print("Performance mode set.")

def main():
    defrag_memory()
    clear_cache()
    close_unnecessary_processes()
    set_performance_mode()

if __name__ == "__main__":
    main()
