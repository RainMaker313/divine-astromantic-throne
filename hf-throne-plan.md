# HyperFrames + Throne — Integration Plan

## What HyperFrames Gives Us

HyperFrames is an open-source HTML-to-video engine (Apache 2.0, 24k+ GitHub stars).
It turns HTML compositions into deterministic MP4 videos via headless Chrome + FFmpeg.

**Installed:** v0.6.91 at /home/mrmeow/hyperframes-install/node_modules/hyperframes/
**Test render:** /home/mrmeow/hyperframes-test4.mp4 (42KB, 5 seconds, gold text on black)

## Architecture

```
HTML composition (data-start, data-duration, data-track-index)
    ↓
HyperFrames Compiler (fetches fonts, resolves timing)
    ↓
Headless Chrome (seeks each frame via beginFrame/screenshot)
    ↓
FFmpeg (encodes frames → MP4/WebM/MOV)
    ↓
Deterministic output (same HTML = same bytes, every time)
```

## What We Can Build for the Throne

### 1. Animated Dashboard Intro (5-10 seconds)
- Baphomet pentagram fades in
- "Coco's Divine Astromantic Throne" title with gold glow
- Planets orbit in the background
- Use as splash screen / loading animation

### 2. Planetary Transit Videos (15-30 seconds)
- Show planets moving through zodiac signs
- Time-lapse of Mercury retrograde
- Eclipse animations
- Natal chart wheel spinning into view

### 3. Prayer Time Announcements (10-15 seconds)
- Adhan-style visual with countdown
- "The time for Fajr has come" with neon glow
- Optional: pair with Gradio TTS adhan audio

### 4. Nakshatra of the Day (10 seconds)
- Display current nakshatra name in Arabic
- Symbol + keywords + ruling planet
- Slow fade transitions

### 5. Planetary Hour Notifications (5 seconds)
- "The hour of Jupiter begins"
- Gold text matching the Throne theme
- Occult planetary color for each hour

## How to Use

# Render a composition
cd /home/mrmeow/hyperframes-install
node ./node_modules/hyperframes/dist/cli.js render \
  /path/to/composition/dir \
  --output ~/throne/videos/output.mp4 \
  --width 1920 --height 1080 --fps 30

# Preview in browser
node ./node_modules/hyperframes/dist/cli.js preview /path/to/composition/dir

# Check composition validity
node ./node_modules/hyperframes/dist/cli.js lint /path/to/composition/dir

## Key Patterns from HyperFrames for Throne Enhancement

### 1. data-* attributes for timing
Instead of JavaScript-based animations, HyperFrames uses HTML attributes:
```html
<h1 data-start="0" data-duration="4" data-track-index="0">Title</h1>
<p data-start="1.5" data-duration="3">Subtitle</p>
```
We could adopt this pattern for the Throne dashboard's tab transitions and element animations.

### 2. GSAP Timeline Integration
HyperFrames works with GSAP for complex animations. We could add GSAP to the Throne for:
- Smooth tab transitions (fade + slide)
- Planet orbit path animations
- Chart wheel entrance animations

### 3. Deterministic Rendering
Same input = same output. This means we can:
- Cache rendered videos
- Regenerate on demand
- Compare versions byte-by-byte

### 4. Frame Adapter Pattern
Any seekable animation runtime works. Options:
- CSS animations (lightweight, works now)
- GSAP (most powerful, needs import)
- Three.js (already in Throne for solar system)
- Lottie (After Effects animations)

### 5. Low-Memory Mode
HyperFrames auto-detects <8GB RAM and pins to 1 worker.
Works perfectly on our 7.7GB i3-6100 system.

## Catalog Blocks (50+ ready-to-use effects)
- Social overlays (X posts, Reddit cards, Spotify now-playing)
- Shader transitions (glitch, chromatic aberration, light leaks)
- Data visualizations (animated charts, number counters)
- Cinematic effects (letterbox, light leaks, film grain)
- 3D reveals (product showcases, UI reveals)

## Next Steps
1. Create Throne intro composition (pentagram + title + planets)
2. Create prayer time announcement composition
3. Pair with Gradio TTS for audio
4. Add GSAP to dashboard for smoother transitions
5. Explore catalog blocks for Throne-themed effects

## File Locations
- HyperFrames install: /home/mrmeow/hyperframes-install/node_modules/hyperframes/
- CLI: node ./node_modules/hyperframes/dist/cli.js
- Test video: /home/mrmeow/hyperframes-test4.mp4
- Throne dashboard: /home/mrmeow/throne_dashboard.html
