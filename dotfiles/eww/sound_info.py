from subprocess import run

# Get output volume
cmd = "wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{print $2*100}'"
data = run(cmd, capture_output=True, shell=True)
outputVolume = data.stdout.decode('utf-8').strip()

# Get microphone volume
cmd = "wpctl get-volume @DEFAULT_AUDIO_SOURCE@ | awk '{print $2*100}'"
data = run(cmd, capture_output=True, shell=True)
inputVolume = data.stdout.decode('utf-8').strip()

# Get output type
outputType = ""
cmd = 'grep -A4 -ri "Headphone Playback Switch" /proc/asound/card*/* | grep "Amp-Out vals.*0x00 0x00"'
data = run(cmd, capture_output=True, shell=True)
if data.stdout.decode('utf-8').strip():
    outputType = ""

print(outputType + " " + outputVolume + "%  " + inputVolume + "%")
