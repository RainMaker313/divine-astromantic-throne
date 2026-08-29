#!/bin/sh
# coco-prime-on-omarchy.sh
# One-shot script: pull backup, extract, rebuild hermes, start services.
# Prereq: archinstall done, logged in as mrmeow, Firefox up, network up.
# Run as: bash <(curl -sL https://raw.githubusercontent.com/RainMaker313/divine-astromantic-throne/releases/coco-essentials-20260829_0458/backups/coco-prime-on-omarchy.sh)
# OR copy-paste the body into a terminal.

set -e
URL="https://github.com/RainMaker313/divine-astromantic-throne/releases/download/coco-essentials-20260829_0458/coco_essentials_20260829_0458.tar.gz"
MD5="1f81928875f6a7cb9bc1e73d6711c75b"
HERMES_REPO="https://github.com/NousResearch/hermes-agent.git"

echo "=== STEP 1: base tools (5 min) ==="
sudo pacman -Syu --noconfirm
sudo pacman -S --needed --noconfirm \
  base-devel git curl wget \
  python python-pip python-pipx \
  nodejs npm \
  flatpak \
  firefox tesseract tesseract-data-eng ffmpeg espeak-ng
sudo loginctl enable-linger mrmeow
sudo mkdir -p /etc/flatpak && flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Firefox env so it doesn't crash your i915 GPU
mkdir -p ~/.config/environment.d
cat > ~/.config/environment.d/firefox.conf <<EOF
MOZ_ENABLE_WAYLAND=1
MOZ_USE_XINPUT2=1
EOF

echo "=== STEP 2: pull + verify backup ==="
mkdir -p ~/coco-restore && cd ~/coco-restore
curl -L -o coco.tar.gz "$URL"
echo "$MD5  coco.tar.gz" | md5sum -c -
# expect: "OK". if FAILED: rm coco.tar.gz; re-curl.

echo "=== STEP 3: extract + perms ==="
cd /
sudo tar -xzf /home/mrmeow/coco-restore/coco.tar.gz -C /
sudo chown -R mrmeow:mrmeow /home/mrmeow
chmod 600 /home/mrmeow/.hermes/.env /home/mrmeow/.hermes/auth.json

echo "=== STEP 4: rebuild hermes venv ==="
rm -rf /home/mrmeow/.hermes/hermes-agent
git clone "$HERMES_REPO" /home/mrmeow/.hermes/hermes-agent
cd /home/mrmeow/.hermes/hermes-agent
python -m venv venv
. venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -e ".[all]"
deactivate
hermes --version

echo "=== STEP 5: enable services ==="
systemctl --user daemon-reload
for s in hermes-gateway-default hermes-gateway-discordia hermes-gateway-metatron-coco \
         hermes-gateway-uriel-coco hermes-gateway-opencode \
         astromantic-throne astromantic-throne-v9 \
         coco-phone-mirror isp-fuckery-monitor \
         http-server-8091 occult-search; do
  systemctl --user enable --now "$s.service" 2>/dev/null && echo "$s: ok" || echo "$s: skipped"
done
systemctl --user enable --now coco-wallpaper-pulse.timer

echo "=== STEP 6: verify ==="
for p in default discordia metatron-coco uriel-coco opencode; do
  echo "  $p: $(systemctl --user is-active hermes-gateway-$p.service 2>&1)"
done
hermes cron status | head -1

echo "=== DONE. Open the dashboard: ==="
echo "firefox http://127.0.0.1:8091/dashboard-v2"
