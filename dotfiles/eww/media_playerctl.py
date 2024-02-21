from subprocess import run

# Get status
cmd = "playerctl status"
data = run(cmd, capture_output=True, shell=True)
status = data.stdout.decode('utf-8').strip()

output = ''

if 'Playing' == status:
    # Get metadata
    output += ''
    
    cmd = "playerctl metadata --format '{{ artist }};{{ title }};{{ duration(position) }};{{ duration(mpris:length) }}'"
    data = run(cmd, capture_output=True, shell=True)
    metadata = data.stdout.decode('utf-8').strip()
    metadataSplit = metadata.split(';')
    artist = metadataSplit[0]
    title = metadataSplit[1]
    position = metadataSplit[2]
    length = metadataSplit[3]

    if len(artist) > 0:
        newOutput = f'{artist} - {title} {position}|{length}'
    else:
        newOutput = f'{title} {position}|{length}'

    if len(newOutput) > 50:
        newOutput = f'{title} {position}|{length}'

    if len(newOutput) > 50:
        title = title[:40] + '..'
        newOutput = f'{title} {position}|{length}'

    output = f'{output} {newOutput}'
else:
    output += ' Not playing'

print(output)
