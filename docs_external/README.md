# docs_external

This folder is for local Tier 2 implementation references only.

It is not Khovan Reach design authority. Do not use files here to change story, pacing, factions, objectives, or player-facing behavior.

Local reference clones and downloaded docs should be fetched only after explicit approval. Use `tools/fetch_tier2_references.ps1 -DryRun` for a preview, or `tools/fetch_tier2_references.ps1` to fetch approved references. If direct script execution is blocked by local PowerShell policy, run the fetch with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\fetch_tier2_references.ps1
```

Expected subfolders:

- `_local_clones`: ignored by Git; approved local external reference clones go here.
- `cosmos`: not yet populated; reserved for approved Cosmos documentation snapshots or notes.
- `mast`: not yet populated; reserved for approved MAST documentation snapshots or notes.
- `sbs_utils`: not yet populated; reserved for curated notes or snapshots, not repo clones.

External reference material should remain ignored by Git unless Matt explicitly asks to vendor a specific file.
