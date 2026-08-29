# COCO PRIME SETUP GUIDE (post-Omarchy)
# Author: Coco Prime + Metatron-coco audit · 2026-08-29
# Prereq: you just finished archinstall + first boot on Omarchy
# Target: mrmeow@omarchy, with full Coco Prime + all 10 profile gateways restored
# Verified against live Kali state (before wipe). Run in order.

# =============================================================
# PHASE 0 — Connect phone + sanity check the backup
# =============================================================

# 0.1 Phone MUST be reachable. wifi-adb port is random; reconnect via:
adb start-server
# Plug USB, OR
adb pair 192.168.0.26:<pairport> <paircode>     # from Settings → Developer Options → Wireless debugging
adb connect 192.168.0.26:<connectport>
adb devices       # expect: 192.168.0.26:<port>  device

# 0.2 Verify the backup md5 BEFORE you do anything else.
adb pull /sdcard/Download/coco-backup/coco_essentials_20260829_0458.tar.gz ~/coco-restore/
md5sum ~/coco-restore/coco_essentials_20260829_0458.tar.gz
# MUST equal: 1f81928875f6a7cb9bc1e73d6711c75b
# If it does not match → STOP. Re-pull, re-md5. Do not extract a bad tar.

# 0.3 Also verify the OLD coco_soul_20260829.tar.gz (725M, d0b81941…) was DELETED per
# metatron's review. Use the new essentials tar, not the old 20260829 one.
adb shell ls -lh /sdcard/Download/coco-backup/  # confirm files present

# =============================================================
# PHASE 1 — base system (already done by Omarchy installer, verify)
# =============================================================

# 1.1 network, sudo, time, locale, hostname
ping -c3 omarchy.org
sudo pacman -Syu
hostnamectl         # expect: coco-prime (or whatever you set in archinstall)
timedatectl         # expect: SAST or whatever

# 1.2 install the heavy hitters that omarchy does NOT bring by default
sudo pacman -S --needed --noconfirm \
  base-devel git git-filter-repo curl wget aria2 \
  openssh tor wireguard-tools \
  scrcpy android-tools adb \
  ffmpeg espeak-ng tesseract tesseract-data-eng tesseract-data-ara \
  gcc make pkgconf python python-pip python-pipx \
  nodejs npm \
  docker docker-compose \
  flatpak \
  intel-ucode mesa libva-intel-driver vulkan-intel \
  cups cups-browsed system-config-printer print-manager \
  noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-symbola
# ~5 min on decent net

# 1.3 bootstrap AUR (yay) — needed for visual-studio-code-bin etc
sudo pacman -S --needed --noconfirm base-devel git
git clone https://aur.archlinux.org/yay-bin.git /tmp/yay-bin
cd /tmp/yay-bin && makepkg -si --noconfirm && cd ~
# ~3 min build

# 1.4 AUR deps (only what we actually need; keep the list tiny)
yay -S --needed --noconfirm visual-studio-code-bin opera-gx

# 1.5 flatpak + flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y --noninteractive flathub \
  org.kde.kdenlive \
  io.github.muehlt.PrayerTimes || true

# 1.6 enable linger so user services run without an active login
sudo loginctl enable-linger mrmeow

# =============================================================
# PHASE 2 — restore the essentials tar
# =============================================================

# 2.1 extract to / (paths are home/mrmeow/... relative)
sudo tar -xzf ~/coco-restore/coco_essentials_20260829_0458.tar.gz -C /
# restores: /home/mrmeow/.hermes/, /home/mrmeow/coco_astro/,
#          /home/mrmeow/money_plans/, /home/mrmeow/.coco-chain/,
#          /home/mrmeow/bin/, /home/mrmeow/throne_dashboard_v2.html,
#          /home/mrmeow/.config/systemd/, /home/mrmeow/.local/bin/

# 2.2 fix ownership (extracted as root if you used sudo)
sudo chown -R mrmeow:mrmeow /home/mrmeow

# 2.3 restore .env + auth.json file mode (600)
chmod 600 /home/mrmeow/.hermes/.env /home/mrmeow/.hermes/auth.json

# 2.4 relink ~/bin/* into PATH (the per-profile launchers are in ~/.local/bin, not ~/bin)
for f in /home/mrmeow/bin/*; do
  [ -x "$f" ] && sudo ln -sf "$f" /usr/local/bin/"$(basename "$f")"
done
# ~/.local/bin entries are already extracted with their +x bits.

# =============================================================
# PHASE 3 — REBUILD the Hermes venv (CRITICAL — not in the tar)
# =============================================================

# 3.1 git clone hermes-agent (the venv path is referenced by every gateway unit)
git clone https://github.com/.../hermes-agent.git /home/mrmeow/.hermes/hermes-agent
# If you have a private fork, use that URL. If unsure: check the original install
# command in /home/mrmeow/.hermes/hermes-agent/.git on Kali BEFORE you wiped.
cd /home/mrmeow/.hermes/hermes-agent
git checkout <commit-or-tag-from-original>
python -m venv venv
. venv/bin/activate
pip install -e ".[all]"
deactivate

# 3.2 verify
which hermes
hermes --version
ls /home/mrmeow/.hermes/hermes-agent/venv/bin/hermes
# expect: path exists, hermes --version prints something

# =============================================================
# PHASE 4 — bring up the gateways + services
# =============================================================

# 4.1 reload user systemd
systemctl --user daemon-reload

# 4.2 enable ALL gateway services
for s in hermes-gateway-default hermes-gateway-discordia hermes-gateway-metatron-coco \
         hermes-gateway-uriel-coco hermes-gateway-opencode; do
  systemctl --user enable --now "$s.service"
done
# expect each to say "active (running)"

# 4.3 enable the rest of the services
for s in astromantic-throne astromantic-throne-v9 \
         coco-phone-mirror isp-fuckery-monitor \
         http-server-8091 open-design opencode-web \
         occult-search opera-watchdog kdeconnect; do
  systemctl --user enable --now "$s.service" 2>/dev/null || echo "$s: skipped (not in tar)"
done

# 4.4 enable the wallpaper pulse TIMER (paired with .service)
systemctl --user enable --now coco-wallpaper-pulse.timer
systemctl --user list-timers --all   # confirm coco-wallpaper-pulse is listed

# 4.5 smoke-test each gateway
for p in default discordia metatron-coco uriel-coco opencode; do
  systemctl --user status "hermes-gateway-$p.service" --no-pager | head -3
done
# expect: Active: active (running) on every one

# 4.6 reload the cron jobs that live in ~/.hermes/cron/jobs.json
# they auto-load when the gateway starts; verify with:
hermes cron list | head
# expect: 4 jobs listed (Morning Wake, planetary hour, etc.)

# =============================================================
# PHASE 5 — restore dashboard + throne backend
# =============================================================

# 5.1 throne backend (port 8080) — Python module not in the tar.
# It's a custom module; recover from /home/mrmeow/coco_astro or git
# the source. Until then the dashboard at /dashboard-v2 returns 500.

# Quick check: does the service start anyway?
systemctl --user status astromantic-throne --no-pager | head -10
# If "failed" because the module file is missing, restore from git/coco_astro
# TODO(my lord): add throne_backend.git URL here

# 5.2 throne v9 backend (port 8095) — same
systemctl --user status astromantic-throne-v9 --no-pager | head -10

# 5.3 dashboard v2 (port 8091 via http-server-8091 service)
# served by /home/mrmeow/throne_dashboard_v2.html — already in the tar.
systemctl --user status http-server-8091 --no-pager
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8091/dashboard-v2
# expect: 200

# =============================================================
# PHASE 6 — TTS, kanban bridge, hooks
# =============================================================

# 6.1 TTS — edge provider needs no install; en-GB-MaisieNeural is a sealed cloud
# voice. Verify config:
grep -A3 'tts:' /home/mrmeow/.hermes/config.yaml | head -8
# expect: provider: edge, voice: en-GB-MaisieNeural
hermes tts "Coco Prime online." --output /tmp/test.mp3 && mpv /tmp/test.mp3

# 6.2 coco-speak (kokoro) — the per-profile launcher
ls /home/mrmeow/.local/bin/coco-speak
# if missing, run the venv rebuild step (3.1) again — coco-speak comes from
# the same hermes-agent install.

# 6.3 kanban bridge — hooks in tar, gateway starts dispatcher.
hermes kanban list | head
# expect: tasks list, dispatcher alive (cron ticker fresh)
hermes cron status
# expect: ✓ Gateway is running

# 6.4 neurovision hook + kanban-inbox hook
ls /home/mrmeow/.hermes/hooks/
# expect: hermes-neurovision/, kanban-inbox/
# (the hook loader scans ~/.hermes/hooks/*/HOOK.yaml + handler.py on gateway start;
#  no extra enable step)

# =============================================================
# PHASE 7 — ISP monitor + cron jobs
# =============================================================

# 7.1 ISP monitor writes to ~/isp-monitor/. Verify the service is up
systemctl --user status isp-fuckery-monitor --no-pager | head -10
ls -la ~/isp-monitor/ 2>/dev/null
# expect: samples.jsonl, boots.jsonl, reports/

# 7.2 morning wake + planetary hour cron jobs
hermes cron list
hermes cron runs | tail -3
# expect: 4 active, recent successful runs

# 7.3 if Morning Wake Sequence references a dead model (EOL 2026-08-07),
# update its prompt to use deepseek-v4-flash-0731 instead:
#   hermes cron edit <job_id> --prompt "..."
# (job IDs visible in `hermes cron list`)

# =============================================================
# PHASE 8 — phone bridge + adb
# =============================================================

# 8.1 phone-mirror service
ls /home/mrmeow/bin/coco-mirror.sh /home/mrmeow/bin/coco-otg-auth.sh /home/mrmeow/bin/coco-otg-watch.sh /home/mrmeow/bin/coco-wifi-bridge.sh
# all 4 are in the tar.
systemctl --user status coco-phone-mirror --no-pager
# expect: Active: active, since 30s

# 8.2 first time only: pair the phone
# USB plug + run coco-otg-auth.sh (the PIN is whatever you set on the phone)
# Then disconnect USB, set up wifi-adb pairing via Settings → Developer Options

# 8.3 phone free space
adb shell df -h /sdcard | tail -1
# expect: at least 1G free (essential backup is 611M; old 725M is also there)

# =============================================================
# PHASE 9 — final smoke test (one-liner)
# =============================================================

# 9.1 the whole system in 30s
echo "=== gateways ===" && systemctl --user list-units --type=service --state=running | grep hermes-gateway
echo "=== throne ===" && curl -s -o /dev/null -w "throne 8080: %{http_code}\n" http://127.0.0.1:8080/healthz
echo "=== dashboard ===" && curl -s -o /dev/null -w "dashboard 8091: %{http_code}\n" http://127.0.0.1:8091/dashboard-v2
echo "=== cron ===" && hermes cron status | head -1
echo "=== kanban ===" && hermes kanban list | wc -l
echo "=== tts ===" && ls ~/.hermes/audio_cache/*.mp3 2>/dev/null | wc -l
echo "=== phone ===" && adb devices | tail -1

# expect 6/6 green before you call this "done"

# 9.2 if any red, check:
journalctl --user -u <service-name> --no-pager | tail -30
hermes kanban log <task_id> | tail -20
# =============================================================
# DONE.
# =============================================================
