from subprocess import run
import re
import sys

def generateWorkspaceButton(workspaceId, activeWorkspaceId):
    if workspaceId == activeWorkspaceId:
        return f'(button :class "active-workspace" {workspaceId})'
    else:
        return f'(button {workspaceId})'

windowId = sys.argv[1]

# Get active workspace id
cmd = 'hyprctl activeworkspace'
data = run(cmd, capture_output=True, shell=True)
activeWorkspaceLines = data.stdout.splitlines()
match = re.search(r'ID (\d+)', activeWorkspaceLines[0].decode('utf-8').strip())
activeWorkspaceId = match.group(1)

# Get all workspaces for monitor id
cmd = 'hyprctl workspaces'
data = run(cmd, capture_output=True, shell=True)
workspacesLines = data.stdout.splitlines()

workspacesIds = []
workspaceButtons = ''

previousLine = ''
for line in workspacesLines:
    decodedLine = line.decode('utf-8').strip()
    if f'monitorID: {windowId}' in decodedLine:
        # Add id to generated ids for monitor
        match = re.search(r'ID (\d+)', previousLine)
        workspacesId = match.group(1)
        workspacesIds.append(workspacesId)        

    previousLine = decodedLine

workspacesIds.sort()
for id in workspacesIds:
    workspaceButtons += generateWorkspaceButton(id, activeWorkspaceId)

print(f'(box :vexpand true {workspaceButtons})')