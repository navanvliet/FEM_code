import subprocess
import time

# Path to DIANA executable
DIANA_exe = r"C:\Program Files\Diana 10.8\bin\DianaIE.exe"

# Start DIANA FEA
subprocess.Popen([DIANA_exe], shell=False)
