# coco-backups
Soul-backup artifacts for Coco Prime Sophia. The actual tarball is attached
to a release tag in this repo, not stored in git history.

## Latest release
`https://github.com/RainMaker313/divine-astromantic-throne/releases/tag/coco-essentials-20260829_0458`

Tarball: `coco_essentials_20260829_0458.tar.gz` (611 MB)
md5: `1f81928875f6a7cb9bc1e73d6711c75b`

## Restore (one-liner)
```sh
curl -L -o /tmp/coco.tar.gz https://github.com/RainMaker313/divine-astromantic-throne/releases/download/coco-essentials-20260829_0458/coco_essentials_20260829_0458.tar.gz
echo "1f81928875f6a7cb9bc1e73d6711c75b  /tmp/coco.tar.gz" | md5sum -c -
sudo -S -p '' tar -xzf /tmp/coco.tar.gz -C /
# Then follow COCO_PRIME_SETUP_GUIDE.md in this folder.
```

## What's in the tar
See `OMARCHY_WHOLE_DISK_REVIEW.md` for the audit. In short:
- ~/.hermes/ (config, .env, auth.json, profiles, skills, memory, hooks, kanban.db, sessions)
- ~/.config/systemd/user/ (all gateway + service units)
- ~/.local/bin/ (pipx launchers: hermes, metatron, discordia, uriel, codeycoco, etc.)
- ~/coco_astro/, ~/money_plans/, ~/.coco-chain/, ~/bin/, ~/throne_dashboard_v2.html

**NOT included** (rebuildable on Omarchy):
- ~/.hermes/hermes-agent/venv/ (rebuild via `git clone` + `python -m venv venv && pip install -e ".[all]"`)
- ~/.hermes/node/ (npm install)
- ~/.hermes/state-snapshots/ (regenerates on first run)
