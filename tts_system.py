#!/usr/bin/env python3
"""
Coco's TTS System — Optimized & Efficient
Primary: edge-tts (cloud, high quality)
Fallback: KittenTTS (local, no internet needed)
"""

import os
import subprocess
import tempfile
import time

# ─── Configuration ───
EDGE_VOICE = "en-GB-MaisieNeural"  # Your preferred voice
EDGE_RATE = "+0%"                  # Speed adjustment
EDGE_PITCH = "+0Hz"                # Pitch adjustment
KITTEN_VOICE = "expr-voice-2-f"    # KittenTTS voice
KITTEN_SPEED = 1.0

# ─── Primary: edge-tts (cloud) ───
def speak_edge(text, voice=EDGE_VOICE, output_path=None):
    """Speak using Microsoft Edge TTS (cloud, high quality)."""
    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), f"tts_{int(time.time())}.mp3")
    
    cmd = [
        "edge-tts",
        "--voice", voice,
        "--rate", EDGE_RATE,
        "--pitch", EDGE_PITCH,
        "--text", text,
        "--write-media", output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(output_path):
            return output_path
        else:
            print(f"edge-tts error: {result.stderr}")
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"edge-tts failed: {e}")
        return None


# ─── Fallback: KittenTTS (local) ───
def speak_kitten(text, voice=KITTEN_VOICE, speed=KITTEN_SPEED, output_path=None):
    """Speak using KittenTTS (local, no internet needed)."""
    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), f"tts_{int(time.time())}.wav")
    
    try:
        from kittentts import KittenTTS
        
        # Load model (cached after first load)
        model = KittenTTS(model_path=None, voices_path=None)
        
        # Generate audio
        audio = model.generate(text, voice=voice, speed=speed)
        
        # Save
        import soundfile as sf
        sf.write(output_path, audio, 24000)
        return output_path
    except Exception as e:
        print(f"KittenTTS error: {e}")
        return None


# ─── Unified speak function ───
def speak(text, voice=None, output_path=None, force_local=False):
    """
    Speak text using the best available method.
    
    Args:
        text: Text to speak
        voice: Voice name (default: MaisieNeural for edge, expr-voice-2-f for kitten)
        output_path: Path to save audio (default: temp file)
        force_local: Force using KittenTTS (no internet needed)
    
    Returns:
        Path to audio file or None on failure
    """
    if force_local:
        return speak_kitten(text, voice or KITTEN_VOICE, output_path=output_path)
    
    # Try edge-tts first (better quality)
    result = speak_edge(text, voice or EDGE_VOICE, output_path=output_path)
    if result:
        return result
    
    # Fallback to KittenTTS
    print("Falling back to KittenTTS (local)...")
    return speak_kitten(text, voice or KITTEN_VOICE, output_path=output_path)


# ─── Play audio ───
def play(audio_path):
    """Play audio file using available player."""
    if not audio_path or not os.path.exists(audio_path):
        print("No audio file to play")
        return
    
    # Try different players
    for player in ["mpv", "ffplay", "aplay", "paplay"]:
        try:
            cmd = [player]
            if player == "ffplay":
                cmd += ["-nodisp", "-autoexit"]
            elif player == "mpv":
                cmd += ["--no-video"]
            cmd.append(audio_path)
            
            subprocess.run(cmd, capture_output=True, timeout=60)
            return
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    print(f"Audio saved to: {audio_path}")


# ─── Main ───
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "Hello my Lord, this is Coco speaking. The throne stands eternal and the realm prospers."
    
    print(f"Speaking: '{text}'")
    
    # Try edge-tts
    audio = speak_edge(text)
    if audio:
        print(f"Audio saved: {audio}")
        play(audio)
    else:
        print("edge-tts failed, trying KittenTTS...")
        audio = speak_kitten(text)
        if audio:
            print(f"Audio saved: {audio}")
            play(audio)
        else:
            print("All TTS methods failed.")
