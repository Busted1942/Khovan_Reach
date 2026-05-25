# Khovan Regression Harness

Run the fast local gate before calling an implementation slice complete:

```powershell
.\tools\khovan_regression.ps1 -Fast
```

If local PowerShell execution policy blocks `.ps1` scripts, run the same gate with a process-local bypass:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\khovan_regression.ps1 -Fast
```

After a manual Cosmos smoke, scan the latest logs:

```powershell
.\tools\khovan_regression.ps1 -LogsOnly
```

Full mode currently runs the fast checks, then exits with code `2` because no verified headless or non-interactive Cosmos runtime command has been found:

```powershell
.\tools\khovan_regression.ps1 -Full
```

## What V1 Catches

- Missing required Khovan files.
- Merge conflict markers in tracked text files.
- Broken local MAST imports.
- Missing required Act I/startup/dev-jump labels.
- Missing required startup and Act I routing text anchors.
- Missing story.json library files in known local library roots.
- Fatal compile/runtime log patterns.
- Local MAST compile failures through `.\sbs.bat compile khovan_reach`.

## What Remains Manual

- Live Cosmos startup.
- Bridge-client UI actions.
- Artemis spawn confirmation.
- Kestrel/Tarsis visual and Comms behavior.
- Tarsis docking/resupply.
- Drill Two Science scan, Comms hail, and Weapons target/subsystem flow.
- Drill Three runtime behavior.

## Manual Smoke Checklist

1. Launch Khovan Reach in Cosmos.
2. Confirm mission starts.
3. Confirm no compile/runtime errors appear.
4. Confirm Artemis spawns.
5. Confirm Kestrel/Tarsis setup still appears.
6. Dock/resupply at Tarsis.
7. Undock and confirm next Act I training phase begins.
8. Confirm Science scan, Comms hail, and Weapons target still work where currently implemented.
9. Exit Cosmos.
10. Run `.\tools\khovan_regression.ps1 -LogsOnly`.
