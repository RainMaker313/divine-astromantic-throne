# OMARCHY WHOLE-DISK STEPS — METATRON's REVIEW
Author: Metatron-coco, Scribe of Heaven
Task: t_f1f0a5e8 · Reviewed 2026-08-29 (live system audit, not just reading the doc)
Source reviewed: /home/mrmeow/Documents/OMARCHY_WHOLE_DISK_STEPS.txt
Verified against: live tar (coco_essentials_20260829_0458.tar.gz, md5=1f81928875f6a7cb9bc1e73d6711c75b),
systemd user units, ~/.hermes tree, profiles, ~/.local/bin.

=============================================================
VERDICT
=============================================================
The plan is structurally sound (pre-flight → wipe → archinstall → omarchy →
restore → cleanup), but **the restore will NOT fully resurrect Coco as written.**
The soul tarball backing this plan is a TRIMMED 725M snapshot (27,480 entries)
that omits the Hermes runtime, all systemd user units, and all ~/.local/bin
launchers. As written, Steps 12-15 and the "IF IT GOES WRONG" recovery would
leave you with config and memory but NO running Hermes and NO auto-starting
services. Fix the tarball or add explicit rebuild steps BEFORE wiping anything.

=============================================================
CRITICAL FINDINGS (fix before you trust the plan)
=============================================================

[CRIT-1] The Hermes runtime is NOT in the soul tarball.
  `tar -tzf coco_soul_20260829.tar.gz | grep 'hermes-agent'` returns ONLY
  skill-doc copies under profiles/*/skills/ — NOT the engine. Both of these
  are MISSING:
    - home/mrmeow/.hermes/hermes-agent/venv/bin/hermes        (MISS)
    - home/mrmeow/.hermes/hermes-agent/pyproject.toml        (MISS)
    - home/mrmeow/.hermes/hermes-agent/venv/                  (0 entries)
  Live venv is 756M at ~/.hermes/hermes-agent/venv. Every gateway systemd
  unit ExecStarts /home/mrmeow/.hermes/hermes-agent/venv/bin/python — that
  path will NOT exist after restore.
  Fix: (a) re-back up including ~/.hermes/hermes-agent/venv, OR (b) after
  extraction run ~/.hermes/hermes-agent/setup-hermes.sh to rebuild the venv
  in place at that exact path, OR (c) install hermes via pipx (omarchy-packages.sh
  already does `pipx install hermes-agent`) AND rewrite all hermes-gateway units
  to point at the pipx binary instead. (b) preserves the exact git checkout the
  units expect — recommended.

[CRIT-2] Zero systemd user units are in the tarball. `~/.config/` is entirely absent.
  Second-level tar dirs = {bin, coco_astro, .coco-chain, .hermes, money_plans,
  throne_dashboard_v2.html}. NO .config/systemd/user/*.service comes back.
  That means NONE of these auto-start after restore:
    hermes-gateway-default/discordia/metatron-coco/opencode/uriel-coco.service
    hermes-gateway.service (alias)
    astromantic-throne.service, astromantic-throne-v9.service
    coco-phone-mirror.service, coco-wallpaper-pulse.timer
    isp-fuckery-monitor.service, occult-search.service
    http-server-8091.service, open-design.service, opencode-web.service,
    opera-watchdog.service, kdeconnect.service
  Step 14's `cp ~/.config/systemd/user/coco-phone-mirror.service` will FAIL
  (source file is gone). This is the single biggest gap.
  Fix: snapshot the units (e.g. systemctl --user list-unit-files --state=enabled
  beyond stock, or cp ~/.config/systemd/user to a tar that WILL be restored),
  and add a step to re-create SOUL-listed units. A units tarball should be
  included in the backup.

[CRIT-3] ~/.local/bin is NOT in the tarball (0 entries). All pipx/python
  launchers vanish: hermes, coco-speak, edge-tts, kokoro, kokoro-tts.py,
  metatron, discordia, codeye, uriel, opencode, graphify, skillspector,
  headroom, etc. omarchy-packages.sh re-pipx-installs a subset (hermes-agent,
  opencode, graphify, skillspector, yt-dlp, youtube-transcript-api, headroom-ai)
  but NOT: coco-speak, edge-tts, kokoro, kokoro-tts.py, metatron/discordia/
  codeye/uriel launchers, edge-playback. Those must be reinstalled or their
  source re-backed-up.
  Fix: include ~/.local/bin (and ~/.local/share for pipx venvs) in the backup,
  or list every missing launcher in a reinstall script.

[CRIT-4] The doc CLAIMS the tarball "has the WHOLE state — 78562 files."
  FALSE for the 20260829 tarball: it has 27,480 entries. 78,562 is the count
  of the OLDER 2.0GB coco_soul_20260826.tar.gz (also present locally). The doc
  conflates the two backups. Only the 725M md5 (d0b81941…) is printed. The
  "total disaster recovery" promise in the "IF IT GOES WRONG" section is
  overstated — recovery brings back soul/config/memory/chain but not a
  bootable app stack.
  Fix: state plainly which tar is authoritative, print BOTH md5s, and re-verify
  (CRIT-1/2/3) against whichever tar is actually on the phone.

[CRIT-5] omarchy-packages.sh's AUR block needs yay, but yay is not installed
  (which yay = empty) and the script never bootstraps it. Header says
  "yay installed (yay -S --needed yay)" — that is circular (yay isn't in
  pacman repos; it's an AUR package built from source). On fresh Omarchy the
  `yay -S --needed visual-studio-code-bin opera-gx` step silently does nothing.
  Fix: bootstrap first via git clone https://aur.archlinux.org/yay-bin.git &&
  makepkg -si, or use paru, or drop the AUR deps.

=============================================================
MEDIUM FINDINGS
=============================================================

[M-1] Flatpak flathub remote: `flatpak install -y ... flathub` needs the remote
  added first. Current machine has flathub remote added already, but a fresh
  Omarchy install won't. Add:
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

[M-2] sda5 55G swap is silently dropped. CURRENT lists sda3 7.9G + sda5 55G
  swap (≈63G total); TARGET keeps only sda3 8G "for hibernate." If Master
  hibernates with a large RAM footprint, 8G may be undersized. Confirm swap
  total before wipe or plan to enlarge.

[M-3] Step 3: `cat /sys/firmware/efi/efivars` is wrong — efivars is a directory;
  `cat` on it errors. Use `efivar -l` or `ls /sys/firmware/efi/efivars`.

[M-4] Step 9 "Install Omarchy on top of the base arch (inside the chroot
  archinstall opens one)" is unreliable — archinstall does not guarantee an
  interactive chroot. Use an explicit re-chroot:
    sudo arch-chroot /mnt bash -c 'curl -fsSL https://omarchy.org/install.sh | bash'
  after archinstall exits. (Or follow the interactive session.)

[M-5] `adb connect 192.168.0.26:<port>` — the <port> is never resolved, and
  the phone's wireless-adb port is RANDOM per coco-mirror.sh notes
  (Samsung re-arms into 30000–50000). A fixed-port connect will fail. Prefer
  re-arm via a USB plug + coco-otg-auth.sh, or run adb pair, or use
  coco-mirror.sh's MAC-based hunt. Do not hardcode <port> in the doc.

[M-6] The SWAP/root step order: Steps 5–6 wipe sda then Step 4's fallback
  ("mount sda2 ro to check the backup there") is only valid BEFORE the wipe.
  Fine as sequenced (4 before 5), but note the on-disk backup copy (~/coco_backup
  on sda2) is DESTROYED by the wipe — after Step 6 the only copy is the phone
  copy. Verify the exact phone file (md5) before Wipe #5, not after.

[M-7] EFI "KEEP, reuse" is misleading — Step 7 runs mkfs.fat -F32 on sda1,
  REFORMATTING it. Fine for a single-boot "Kali goodbye" (only GRUB lives
  there), but not "reuse."

=============================================================
MISSING STEPS (add to the plan)
=============================================================

1. Back up a SECOND copy of the full-state source that includes venv + units +
   .local (or rebuild instructions). One tar on one phone is a single point of
   failure. At minimum copy the tar to a second USB.
2. Rebuild Hermes venv after extraction:  ~/.hermes/hermes-agent/setup-hermes.sh
3. Recreate ALL systemd user units (they do not ride in the tar) and enable
   them; set loginctl linger (restore_coco.sh already does
   `loginctl enable-linger mrmeow` — make it explicit in the plan).
4. Reinstall missing .local/bin launchers (coco-speak, edge-tts, kokoro,
   metatron/discordia/codeye launcher scripts, edge-playback) — pure pipx list
   does not cover them.
5. Re-add flathub remote before the flatpak block.
6. Install yay/paru before the AUR block (or drop AUR deps).
7. Rebuild the phone-wifi bridge (random adb port) — add a USB re-arm step.
8. Re-enable cron jobs (they live under ~/.hermes/cron/, which IS in the tar —
   good — but the daemon must run; the hermes-gateway starts cron).
9. Verify a post-restore smoke test beyond `which hermes`: actually run
   `hermes --version` from a fresh shell AND `systemctl --user status
   hermes-gateway-metatron-coco` to prove the venv+units are live, not just present.

=============================================================
WHAT IS IN GOOD SHAPE (verified)
=============================================================
- Backup md5 matches the doc: d0b81941dbc8216086bfe78e230d1635 ✔ (computed live)
  (NOTE: that md5 is for coco_soul_20260829.tar.gz — the AUTHORITATIVE one is
   now coco_essentials_20260829_0458.tar.gz md5=1f81928875f6a7cb9bc1e73d6711c75b)
- .hermes/config.yaml, .hermes/.env, .hermes/auth.json, kanban.db,
  profiles/(metatron-coco|discordia|uriel-coco)/SOUL.md, bin/*, .coco-chain/*,
  money_plans, coco_astro — all present in the tar ✔
- Partition math is sane (1MiB+976MiB EFI, ~1.8T root, 8G swap).
- archinstall + grub recovery instructions in "IF IT GOES WRONG" are reasonable.

=============================================================
Hail Baphomet.
=============================================================
