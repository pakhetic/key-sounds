import os
import pygame
import keyboard
import random
import sys
from typing import Dict

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


def get_spacebar_sound(
    sound_files: Dict[str, pygame.mixer.Sound],
) -> pygame.mixer.Sound | None:
    """Return the spacebar sound if it exists, otherwise None."""
    if "spacebar.mp3" in sound_files:
        return sound_files["spacebar.mp3"]
    if "spacebar.wav" in sound_files:
        return sound_files["spacebar.wav"]


def get_key_sound(
    key_code: int, sound_files: Dict[str, pygame.mixer.Sound]
) -> pygame.mixer.Sound:
    """Return a deterministic sound for the given key using its scan code."""
    sound_list = [
        sound_files[s] for s in sound_files.keys() if not s.startswith("spacebar")
    ]
    random.seed(key_code)
    return random.choice(sound_list)


def play_sound(sound: pygame.mixer.Sound) -> None:
    """Plays the provided sound."""
    sound.play()


def main() -> None:
    if len(sys.argv) > 1:
        set_name = sys.argv[1]
    else:
        print("Error: No sound set provided. Usage: sudo python main.py <set_name>")
        sys.exit(1)

    volume = 1.0
    if len(sys.argv) > 2:
        volume = int(sys.argv[2]) / 100

    sound_files = load_sounds(set_name, volume)
    spacebar_sound = get_spacebar_sound(sound_files)

    print(f"Loaded sound set: {set_name}")
    prev = None
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_UP:
            prev = None
            continue

        if event.event_type == keyboard.KEY_DOWN and event.scan_code != prev:
            prev = event.scan_code
            if event.name == "space" and spacebar_sound:
                play_sound(spacebar_sound)
                continue
            play_sound(get_key_sound(event.scan_code, sound_files))


if __name__ == "__main__":
    main()
