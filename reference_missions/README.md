# reference_missions

This folder is for approved local reference mission clones only.

Reference missions are syntax/API/bootstrap examples. They are not Khovan Reach design authority and must not be used to alter Khovan story, pacing, factions, objectives, or player-facing behavior.

Approved reference targets are listed in `docs_external/00_tier2_reference_inventory.md`.

Approved local clones must live outside this live mission package. Do not keep cloned reference repositories under `_local_clones` here; the MAST loader can discover `.mastlib`, `.sbslib`, and `.zip` files under the mission root during load.

This folder is currently not yet populated beyond placeholder/README files. Use `tools/fetch_tier2_references.ps1 -DryRun` for a preview, or `tools/fetch_tier2_references.ps1` to fetch approved references into the external reference root. If direct script execution is blocked by local PowerShell policy, run the fetch with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\fetch_tier2_references.ps1
```

Do not move files from this folder into active `scripts/`.
