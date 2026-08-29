# OMARCHY FIRST BOOT — COCO PRIME + FIREFOX
# After archinstall + first login as mrmeow on Omarchy.
# Verified against Omarchy 4.0.1 (Arch base). Run top to bottom.

# =============================================================
# STEP 0 — network + identity (one-time, ~30s)
# =============================================================
ping -c3 omarchy.org                          # expect: 3 received
sudo pacman -Syu --noconfirm                  # sync + upgrade (~1-3 min)
sudo loginctl enable-linger mrmeow             # so user services run without active login
hostnamectl                                   # confirm hostname
sudo localectl set-locale LANG=en_US.UTF-8    # if you want US locale

# =============================================================
# STEP 1 — Firefox (the only browser that works on i915+Wayland)
# =============================================================
# Firefox is usually pre-installed on Omarchy. If not:
sudo pacman -S --needed --noconfirm firefox
# Verify + launch
firefox --version
firefox &

# Critical env so Firefox doesn't break on i915/Wayland (your box:
# HD Graphics 530 + Wayland, known GPU crash with Chromium):
# Add to ~/.config/environment.d/firefox.conf
mkdir -p ~/.config/environment.d
cat > ~/.config/environment.d/firefox.conf <<'EOF'
MOZ_ENABLE_WAYLAND=1
MOZ_USE_XINPUT2=1
EOF
# Logout/login OR source it now:
export $(cat ~/.config/environment.d/firefox.conf | xargs)
firefox &

# Test: open about:support → check "WebGL: enabled" + "Compositing: WebRender"
# if WebRender is "Software" and you wanted HW accel, the i915 will cope
# either way — Firefox never crashes your GPU like Chromium does.

# =============================================================
# STEP 2 — base tools (5 min)
# =============================================================
sudo pacman -S --needed --noconfirm \
  base-devel git git-filter-repo curl wget aria2 \
  openssh tor wireguard-tools \
  scrcpy android-tools adb \
  ffmpeg espeak-ng tesseract tesseract-data-eng tesseract-data-ara \
  python python-pip python-pipx \
  nodejs npm \
  docker docker-compose \
  flatpak \
  intel-ucode mesa libva-intel-driver vulkan-intel \
  noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-symbola

# =============================================================
# STEP 3 — bootstrap AUR (yay)
# =============================================================
git clone https://aur.archlinux.org/yay-bin.git /tmp/yay-bin
cd /tmp/yay-bin && makepkg -si --noconfirm && cd ~

# =============================================================
# STEP 4 — Flatpak + flathub
# =============================================================
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y --noninteractive flathub \
  org.kde.kdenlive \
  io.github.muehlt.PrayerTimes || true

# =============================================================
# STEP 5 — pull + verify the backup
# =============================================================
mkdir -p ~/coco-restore && cd ~/coco-restore
# Download from GitHub release (works without phone)
curl -L -o coco_essentials_20260829_0458.tar.gz \
  https://github.com/RainMaker313/divine-astromantic-throne/releases/download/coco-essentials-20260829_0458/coco_essentials_20260829_0458.tar.gz
# Verify md5 BEFORE extracting
echo "1f81928875f6a7cb9bc1e73d6711c75b  coco_essentials_20260829_0458.tar.gz" | md5sum -c -
# expect: ": OK"
# If it says FAILED → STOP. Re-download. Do NOT extract a bad tar.

# =============================================================
# STEP 6 — extract + fix perms (30s)
# =============================================================
cd /
sudo tar -xzf ~/coco-restore/coco_essentials_20260829_0458.tar.gz -C /
sudo chown -R mrmeow:mrmeow /home/mrmeow
chmod 600 /home/mrmeow/.hermes/.env /home/mrmeow/.hermes/auth.json

# =============================================================
# STEP 7 — REBUILD the Hermes venv (CRITICAL)
# =============================================================
# The tar has all skills/memory/profiles/.env but NOT the hermes-agent runtime.
# Check on Kali BEFORE wiping what's the actual repo URL:
#   cat /home/mrmeow/.hermes/hermes-agent/.git/config
# Then on Omarchy:
git clone <REAL_HERMES_AGENT_URL> /home/mrmeow/.hermes/hermes-agent
cd /home/mrmeow/.hermes/hermes-agent
git checkout <commit-or-tag-from-original>
python -m venv venv
. venv/bin/activate
pip install -e ".[all]"
deactivate
which hermes && hermes --version

# =============================================================
# STEP 8 — bring up services
# =============================================================
systemctl --user daemon-reload
for s in hermes-gateway-default hermes-gateway-discordia hermes-gateway-metatron-coco \
         hermes-gateway-uriel-coco hermes-gateway-opencode \
         astromantic-throne astromantic-throne-v9 \
         coco-phone-mirror isp-fuckery-monitor \
         http-server-8091 occult-search; do
  systemctl --user enable --now "$s.service" 2>/dev/null \
    && echo "$s: ok" || echo "$s: skipped"
done
systemctl --user enable --now coco-wallpaper-pulse.timer

# Quick smoke
for p in default discordia metatron-coco uriel-coco; do
  systemctl --user is-active "hermes-gateway-$p.service" 2>&1
done
# expect 4× "active"

# =============================================================
# STEP 9 — verify
# =============================================================
# Open in Firefox:
firefox http://127.0.0.1:8091/dashboard-v2     # main dashboard
# Throne backend (custom module, may need git URL — restore from coco_astro or git):
firefox http://127.0.0.1:8080/                 # throne v8 (if running)
# If 503/500, the throne python module is not restored — see COCO_PRIME_SETUP_GUIDE.md Phase 5

# =============================================================
# DONE. ~10-15 min from clean Omarchy to running Coco Prime.
# =============================================================
