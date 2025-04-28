import subprocess
import time

while True:
    print("✅ Bot starting...")
    process = subprocess.Popen(["python3", "main.py"])
    process.wait()

    print("❌ Bot crashed or exited. Restarting in 5 seconds...")
    time.sleep(5)


