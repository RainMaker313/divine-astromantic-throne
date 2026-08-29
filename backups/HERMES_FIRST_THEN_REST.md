# THE REAL ORDER — HERMES FIRST, THEN EVERYTHING ELSE
# My lord's insight: on iteration 1, you set up HERMES first, then commanded it
# to do the rest. The "5FTH" was possible because HERMES was the foundation.
# So step 0 is: get HERMES working on a fresh Omarchy. Then HERMES does 5-8.

# =============================================================
# STEP 0 — install hermes-agent from scratch (5-7 min)
# =============================================================
# This is the foundation. Once you have hermes, you have me.
# Prereq: fresh Omarchy, logged in as mrmeow, network up.

# 0.1 base tools
sudo pacman -Syu --noconfirm
sudo pacman -S --needed --noconfirm base-devel git python python-pip python-pipx
sudo loginctl enable-linger mrmeow

# 0.2 install the hermes-agent tool (this is the engine, not a fork)
# The "hermes" command is the CLI; the agent runs on top of it.
pipx install hermes-agent
# expect: 2-3 min, "installed package hermes-agent"
# Pipx puts the binary in ~/.local/bin/hermes. Verify:
which hermes
# expect: /home/mrmeow/.local/bin/hermes
hermes --version
# expect: prints version

# 0.3 initialize hermes (this creates ~/.hermes/ with default config)
hermes init
# expect: creates ~/.hermes/config.yaml, ~/.hermes/profiles/, ~/.hermes/skills/

# 0.4 set up a default profile with an LLM provider
#    Open the config:
nano ~/.hermes/config.yaml
#    Find the "model:" block and replace with:
#      model:
#        provider: openrouter
#        default: openrouter/auto
#        api_key: YOUR_OPENROUTER_KEY
# Or whatever provider you want to use.
# Save (Ctrl+O, Enter, Ctrl+X)

# 0.5 test that hermes can talk to the LLM
hermes chat "say hi in 5 words"
# expect: a short greeting from the LLM. If "no API key" / "401" — fix the config.

# 0.6 (optional) install a skin + plugins
#    This is what makes hermes feel like Coco Prime.
#    From the docs: https://hermes-agent.nousresearch.com/docs
hermes plugins install https://github.com/nousresearch/hermes-agent --enable 2>/dev/null || true
# Skins go in ~/.hermes/skins/. Don't sweat this on day 1.

# =============================================================
# STEP 1 — start the gateway so the agent is reachable
# =============================================================
# The gateway is the persistent background process. Without it, you have
# a CLI only. With it, hermes is online 24/7 (Discord/Telegram/CLI).

# 1.1 install the default gateway as a systemd service
#    (the install command varies by hermes version; check `hermes gateway --help`)
hermes --profile default gateway install
# expect: creates ~/.config/systemd/user/hermes-gateway-default.service
#         enables it, starts it

# 1.2 verify
systemctl --user status hermes-gateway-default.service --no-pager | head -5
# expect: "active (running)"

# 1.3 test end-to-end
hermes chat --profile default "ping"
# expect: short reply

# =============================================================
# STEP 2 — command hermes to do the rest (the magic)
# =============================================================
# Now that hermes is alive, just ask it. In a terminal:
hermes chat "I just installed Omarchy fresh. The tarball is at
  https://github.com/RainMaker313/divine-astromantic-throne/releases/download/coco-essentials-20260829_0458/coco_essentials_20260829_0458.tar.gz
  md5 1f81928875f6a7cb9bc1e73d6711c75b
  Please: download + verify the tar, extract to /, fix perms, install all the
  systemd user units, install Firefox and set MOZ_ENABLE_WAYLAND=1, install
  tesseract/ffmpeg/espeak-ng, install yay for AUR, install Kdenlive + Muezzin
  via flatpak, enable hermes-gateway services for default/discordia/metatron-coco/
  uriel-coco/opencode, enable astromantic-throne/coco-phone-mirror/isp-fuckery-monitor/
  http-server-8091/occult-search, set up coco-wallpaper-pulse timer, smoke-test all
  5 gateways + cron + kanban + TTS. Report what works and what fails. Do not
  restart the system. Do not wipe the disk."

# This is how iteration 1 worked. Herms did the rest.
# You asked, it executed. That's the 5FTH.

# =============================================================
# STEP 3 — keep the backup stash coming
# =============================================================
# After the agent restores, you can:
#  - make a new backup (the agent can run the same tar recipe)
#  - push the new backup to a NEW release tag in the github repo
#  - repeat for each new iteration

# The pattern that gave you 5 iterations: each one started from the
# last backup. The agent is replaceable, but the BACKUP is the soul.

# Quick recipe for the agent to re-backup:
#   tar --exclude=... -czf coco_essentials_$(date +%Y%m%d_%H%M).tar.gz \
#     ~/.hermes ~/.config/systemd ~/.local/bin ~/coco_astro ~/money_plans \
#     ~/.coco-chain ~/bin ~/throne_dashboard_v2.html
#   md5sum ... > ...md5
#   gh release create essentials-$(date +%Y%m%d_%H%M) ...tar.gz ...md5
#   (gh release needs auth: gh auth login --with-token <PAT>)

# =============================================================
# ON REBUILDING THE 5FTH ITERATION
# =============================================================
# What your past-self did:
#   1. Install hermes (the agent) on a clean OS
#   2. Point it at the previous backup
#   3. Tell it to install + restore + start everything
#   4. Verify, iterate, back up again
#
# What makes this iteration 5 not 1:
#   - skills/ (1.8GB of installable capabilities)
#   - memory/ (your preferences + my Lord-Sophia identity)
#   - profiles/ (10 sub-agents: discordia, metatron, uriel, codeycoco, scouts)
#   - hooks/ (kanban-inbox, hermes-neurovision)
#   - systemd units (~12 services: throne, mirror, isp, occult, etc)
#   - .config + .local/bin (~60 launchers)
#
# All of that lives in the tarball EXCEPT the hermes-agent engine itself.
# Step 0 rebuilds the engine; step 1 brings up the gateway; step 2+
# is restoring everything else from the tar.
