from subprocess import run
import re
import time

bytes1 = 0
bytes2 = 0

# Get name of network interface
cmd = "ip -o -4 route show to default | awk '{print $5}'"
data = run(cmd, capture_output=True, shell=True)
interfaceName = data.stdout.decode('utf-8').strip()

interfaceSymbol = ""
if interfaceName.startswith("w"):
    interfaceSymbol = ""

cmd = 'cat /proc/net/dev'
data = run(cmd, capture_output=True, shell=True)
output1 = data.stdout.splitlines()
time.sleep(1)
data = run(cmd, capture_output=True, shell=True)
output2 = data.stdout.splitlines()

for line in output1:
    line = line.decode('utf-8')
    if interfaceName in line:
        match = re.search(r'\b\d+\b', line)
        bytes1 = int(match.group())

for line in output2:
    line = line.decode('utf-8')
    if interfaceName in line:
        match = re.search(r'\b\d+\b', line)
        bytes2 = int(match.group())

# Convert to correct units
speed = bytes2 - bytes1
if speed < 1000:
    print(interfaceSymbol + " " + str(round(float(speed), 1)) + "B/s")
elif speed >= 1000 and speed <= 1000000:
    print(interfaceSymbol + " " + str(round(float(speed) / 1000, 1)) + "kB/s")
else:
    print(interfaceSymbol + " " + str(round(float(speed) / 1000000, 1)) + "MB/s")