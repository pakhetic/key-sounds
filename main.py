import os
import sys
import time
import random
from typing import Dict

import pygame
from pynput import keyboard

pygame.mixer.init()


def load_sounds(set_name: str, volume: float = 1.0) -> Dict[str, pygame.mixer.Sound]:
    """Load all .mp3 and .wav files from the selected sound set into memory."""
    sound_folder = os.path.join("sounds", set_name)
    if not os.path.isdir(sound_folder):
        print(f"Error: Sound set '{set_name}' not found.")
        sys.exit(1)

    sound_files = {}
    for filename in os.listdir(sound_folder):
        if filename.endswith((".mp3", ".wav")):
            sound_path = os.path.join(sound_folder, filename)
            sound_files[filename] = pygame.mixer.Sound(sound_path)
            sound_files[filename].set_volume(volume)
    return sound_files


def get_custom_sound(
    sound_files: Dict[str, pygame.mixer.Sound], name: str
) -> pygame.mixer.Sound | None:
    """Return the spacebar sound if it exists, otherwise None."""
    mp3, wav = f"{name}.mp3", f"{name}.wav"
    if mp3 in sound_files:
        return sound_files[mp3]
    if wav in sound_files:
        return sound_files[wav]


def get_key_sound(
    key_code: int, sound_files: Dict[str, pygame.mixer.Sound]
) -> pygame.mixer.Sound:
    """Return a deterministic sound for the given key using its scan code."""
    sound_list = [
        s for s in sound_files.keys() if not s.startswith(("spacebar", "non_default"))
    ]
    random.seed(key_code)
    name = random.choice(sound_list)
    return sound_files[name]


def on_press(key):
    if hasattr(key, "name"):
        if key.name == "space" and spacebar_sound:
            spacebar_sound.play()
            return
        if key.name and non_default_sound:
            non_default_sound.play()
            return

    if key.char:
        get_key_sound(ord(key.char), sound_files).play()


def main():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        time.sleep(0.001)


if len(sys.argv) > 1:
    set_name = sys.argv[1]
else:
    print("Error: No sound set provided. Usage: sudo python main.py <set_name>")
    sys.exit(1)

volume = 1.0
if len(sys.argv) > 2:
    volume = int(sys.argv[2]) / 100

sound_files = load_sounds(set_name, volume)
spacebar_sound = get_custom_sound(sound_files, "spacebar")
non_default_sound = get_custom_sound(sound_files, "non_default")

if __name__ == "__main__":
    print(f"Loaded sound set: {set_name}")
    main()
