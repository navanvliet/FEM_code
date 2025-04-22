import subprocess

# Path to the Plaxis 2D executable
plaxis_exe = r"C:\Program Files\Seequent\PLAXIS 2D 2024\Plaxis2DXInput.exe"

# Start PLAXIS 2D with the remote server enabled
subprocess.Popen([plaxis_exe], shell=False)