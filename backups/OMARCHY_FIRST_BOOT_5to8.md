# STEPS 5-8 (DEEP DIVE) — PULL BACKUP, EXTRACT, BUILD HERMES, START SERVICES
# Prereq: Steps 1-4 done. You are mrmeow@omarchy, Firefox open, network up.
# This is the meat. Take your time. ~10 min total.

##############################################################################
# STEP 5 — pull + verify the backup
##############################################################################
# 5.1 Make a workspace for the restore
mkdir -p ~/coco-restore
cd ~/coco-restore
# confirm: you are now in /home/mrmeow/coco-restore
pwd
# expect: /home/mrmeow/coco-restore

# 5.2 Download the 611M tarball from GitHub (the release we pushed earlier)
curl -L -o coco_essentials_20260829_0458.tar.gz \
  https://github.com/RainMaker313/divine-astromantic-throne/releases/download/coco-essentials-20260829_0458/coco_essentials_20260829_0458.tar.gz
# -L follows redirects (github -> CDN). Takes 1-2 min.
# expect: progress bar, ends with "100  611M  ..."

# 5.3 Inspect the file
ls -lh coco_essentials_20260829_0458.tar.gz
# expect: ~611M, dated 2026-08-29
file coco_essentials_20260829_0458.tar.gz
# expect: "gzip compressed data"

# 5.4 Verify the md5 (CRITICAL — do not skip)
echo "1f81928875f6a7cb9bc1e73d6711c75b  coco_essentials_20260829_0458.tar.gz" | md5sum -c -
# expect: "coco_essentials_20260829_0458.tar.gz: OK"
# If "FAILED" → the download is corrupt. STOP. Re-download (rm the bad file first):
#   rm coco_essentials_20260829_0458.tar.gz
#   curl -L -O https://github.com/RainMaker313/divine-astromantic-throne/releases/download/coco-essentials-20260829_0458/coco_essentials_20260829_0458.tar.gz
#   md5sum -c -

# 5.5 (Optional but smart) peek inside the tar
tar -tzf coco_essentials_20260829_0458.tar.gz | head -10
# expect: paths like home/mrmeow/.hermes/...
# Also count entries:
tar -tzf coco_essentials_20260829_0458.tar.gz | wc -l
# expect: 26907 (matches what we packed)

##############################################################################
# STEP 6 — extract + fix permissions
##############################################################################
# 6.1 The tar contains paths like home/mrmeow/... (relative to /).
#     Extract at the root so files land in their original locations.
cd /
# Why sudo? Some files in .hermes are owned root (state.db etc).
sudo tar -xzf /home/mrmeow/coco-restore/coco_essentials_20260829_0458.tar.gz -C /
# expect: ~30s of progress, no errors. If you see "Permission denied" mid-way,
# some files exist already — fix with --overwrite:
#   sudo tar -xzf /home/mrmeow/coco-restore/coco_essentials_20260829_0458.tar.gz -C / --overwrite

# 6.2 Fix ownership (the sudo above may have set root:root on some files)
sudo chown -R mrmeow:mrmeow /home/mrmeow
# expect: silent, instant

# 6.3 Lock down secrets (file mode 600 — owner read/write only)
chmod 600 /home/mrmeow/.hermes/.env /home/mrmeow/.hermes/auth.json
# expect: silent

# 6.4 Verify key directories are present
ls -la /home/mrmeow/.hermes/ | head -5
# expect: config.yaml, .env, auth.json, profiles/, skills/, memory/
ls -la /home/mrmeow/.config/systemd/user/ | head -5
# expect: hermes-gateway-*.service, astromantic-throne.service, etc
ls /home/mrmeow/.local/bin/ | head -5
# expect: hermes, metatron, discordia, uriel, codeycoco, edge-tts, etc

# 6.5 Confirm no hermes-agent venv (it's excluded from the tar)
ls /home/mrmeow/.hermes/hermes-agent/ 2>&1
# expect: "No such file or directory"  ← this is correct
ls /home/mrmeow/.hermes/hermes-agent/venv 2>&1
# expect: "No such file or directory"  ← venv will be built in step 7

##############################################################################
# STEP 7 — rebuild the Hermes venv (the only manual part)
##############################################################################
# BEFORE THIS STEP — get the real hermes-agent git URL.
# On Kali, before wiping, run:
#   cat /home/mrmeow/.hermes/hermes-agent/.git/config
# Look for the line under [remote "origin"]: url = https://...
# WRITE THAT URL DOWN. Examples (yours may differ):
#   https://github.com/nousresearch/hermes-agent.git
#   https://github.com/your-fork/hermes-agent.git
#   git@github.com:your-fork/hermes-agent.git

# 7.1 Set the URL (replace the placeholder)
HERMES_REPO="PASTE_THE_URL_HERE"
# Verify
echo "$HERMES_REPO"
# expect: the real https:// or git@ URL

# 7.2 Clone the repo
cd /home/mrmeow/.hermes
# If the dir exists empty (from a half-done step), remove it first:
rm -rf hermes-agent
git clone "$HERMES_REPO" hermes-agent
# expect: "Cloning into 'hermes-agent'..."
# 1-2 min depending on connection

# 7.3 Check out the same commit you had on Kali (else behavior may differ)
cd /home/mrmeow/.hermes/hermes-agent
# To find your current commit on Kali BEFORE wiping:
#   git -C /home/mrmeow/.hermes/hermes-agent rev-parse HEAD
# write that hash down too. Example: a1b2c3d4e5f6...
# On Omarchy:
git checkout <PASTE_COMMIT_HASH>
# If you didn't record the commit, skip this step — main/master will be close enough.

# 7.4 Create the venv
python -m venv venv
# expect: silent, instant. Creates venv/ directory.

# 7.5 Activate + install (this is the slow part — 2-5 min)
. venv/bin/activate
# Your prompt should now show (venv) prefix
which python
# expect: /home/mrmeow/.hermes/hermes-agent/venv/bin/python
which pip
# expect: /home/mrmeow/.hermes/hermes-agent/venv/bin/pip

# Upgrade pip first (the bundled one is often too old)
pip install --upgrade pip wheel setuptools

# Install hermes-agent in editable mode WITH all optional deps
pip install -e ".[all]"
# expect: 2-5 min, lots of "Collecting..." then "Successfully installed..."
# If it errors on a missing dep, read the error — usually a system library
# (apt equivalent: `sudo pacman -S <pkg>` then re-run)

# 7.6 Smoke-test the venv
which hermes
# expect: /home/mrmeow/.hermes/hermes-agent/venv/bin/hermes
hermes --version
# expect: prints the version (e.g. "0.x.y")

# 7.7 Deactivate the venv (the systemd units will re-activate it when they start)
deactivate
# prompt prefix should disappear

# 7.8 Sanity: the unit file points to this exact path
grep ExecStart /home/mrmeow/.config/systemd/user/hermes-gateway-default.service | head -1
# expect: ExecStart=/home/mrmeow/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main
# If the path doesn't match, the service WILL fail to start. Check your git checkout.

##############################################################################
# STEP 8 — bring up all services
##############################################################################
# 8.1 Reload systemd to pick up the restored unit files
systemctl --user daemon-reload
# expect: silent

# 8.2 Re-enable lingering (in case pacman wiped it on first boot)
sudo loginctl enable-linger mrmeow
# expect: silent

# 8.3 Enable + start the gateway services
# (each one spins up an LLM-backed agent; takes 5-10s per service)
for s in hermes-gateway-default \
         hermes-gateway-discordia \
         hermes-gateway-metatron-coco \
         hermes-gateway-uriel-coco \
         hermes-gateway-opencode; do
  systemctl --user enable --now "$s.service"
  echo "--- $s ---"
  systemctl --user is-active "$s.service" 2>&1
done
# expect: 5 lines of "active"
# If any say "inactive" or "failed":
#   journalctl --user -u hermes-gateway-<name>.service -n 30 --no-pager

# 8.4 Enable the rest of the services
for s in astromantic-throne astromantic-throne-v9 \
         coco-phone-mirror isp-fuckery-monitor \
         http-server-8091 occult-search; do
  systemctl --user enable --now "$s.service" 2>/dev/null \
    && echo "$s: OK" \
    || echo "$s: SKIPPED (unit file missing or dep missing)"
done
# expect: 6 lines, all OK or 1-2 SKIPPED
# If astromantic-throne is SKIPPED, the throne Python module is not in the tar
# (it's a custom code, not in the essentials snapshot). See the section
# "throne backend source" at the end.

# 8.5 Enable the wallpaper pulse timer (paired with .service)
systemctl --user enable --now coco-wallpaper-pulse.timer
systemctl --user list-timers --all | grep -i wallpaper
# expect: "coco-wallpaper-pulse.timer ... n/a ..."

# 8.6 Smoke-test all 5 gateways in one shot
echo "=== gateway status ==="
for p in default discordia metatron-coco uriel-coco opencode; do
  state=$(systemctl --user is-active "hermes-gateway-$p.service" 2>&1)
  echo "  $p: $state"
done
# expect 5x "active"

# 8.7 Open the dashboard in Firefox
firefox http://127.0.0.1:8091/dashboard-v2 &
# expect: dashboard loads, shows the astro wheel
# If 502/503, the http-server-8091 service is not up; re-check step 8.4

# 8.8 Verify the cron ticker is alive
hermes cron status | head -3
# expect: "✓ Gateway is running — cron jobs will fire automatically"

# 8.9 Verify the kanban bridge
hermes kanban list | head -3
# expect: header + any prior tasks (or empty if first boot)

# 8.10 TTS test (edge provider needs internet)
hermes tts "Coco Prime online" --output /tmp/coco-hello.mp3
ls -lh /tmp/coco-hello.mp3
# expect: ~50KB MP3 file
# Play it: mpv /tmp/coco-hello.mp3

##############################################################################
# DONE. If all 10 sub-checks pass, you have a working Coco Prime.
##############################################################################

# === TROUBLESHOOTING (if something's red) ===

# Gateway service failed?
journalctl --user -u hermes-gateway-discordia -n 50 --no-pager
# Common: "No such file or directory" → venv path mismatch (re-do step 7.8)
# Common: "API key invalid" → provider config wrong; edit
#   ~/.hermes/profiles/discordia/config.yaml and check the model block

# Throne backend not starting?
ls /home/mrmeow/.hermes/hermes-agent/venv/lib/python*/site-packages/hermes_cli/ | head
# If the astromantic_throne_v8.py file is missing, the source repo
# (the one you git-cloned in step 7) does not contain it. Throne is a
# CUSTOM module, not the standard hermes-agent. It lives in:
#   /home/mrmeow/astromantic_throne_v8.py
# on Kali. That file is in the tar (under coco_astro/) but not at the
# expected location. Restore it:
sudo cp /home/mrmeow/coco_astro/astromantic_throne_v8.py \
        /home/mrmeow/.hermes/hermes-agent/
# (Adjust the path to wherever the source actually was on Kali — the tar
# preserved whatever you had at ~/coco_astro/.)

# Phone bridge dead?
adb kill-server; adb start-server
adb devices
# If empty, plug the phone in via USB and run /home/mrmeow/bin/coco-otg-auth.sh
# Or re-pair via wifi: Settings → Developer Options → Wireless debugging
