import time
import threading
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
import pythoncom
import pygame
import os

# Shared flag
is_playing = False


def is_sound_playing(threshold=0.01):
    sessions = AudioUtilities.GetAllSessions()
    excluded_process_names = {"python.exe", "pythonw.exe", "audiodg.exe"}  # Add any you want to exclude
    
    for session in sessions:
        if session.Process and session.State == 1:
            try:
                process_name = session.Process.name()
#                print(process_name)
                if process_name.lower() in excluded_process_names:
                    continue  # Skip audio from these processes
            except Exception:
                continue
            volume = session._ctl.QueryInterface(IAudioMeterInformation)
            if volume.GetPeakValue() > threshold:
                return True
    return False

def main():
    pythoncom.CoInitialize()
    global is_playing
    print("Monitoring system audio...")
    while True:
        is_playing = not is_sound_playing()
        time.sleep(1)

# Audio playback code
pygame.mixer.init()
AUDIO_EXTENSIONS = (".mp3", ".wav")

def load_audio_files(folder):
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"Folder not found: {folder}")
    files = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(AUDIO_EXTENSIONS)
    ])
    if not files:
        raise FileNotFoundError("No audio files found.")
    return files

class AudioPlayer:
    def __init__(self, file_list):
        self.files = file_list
        self.current_index = 0
        self.is_paused = False
        self.is_playing = False

    def play_current(self):
        print("-> play current")
        pygame.mixer.music.load(self.files[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        print(f"Playing: {os.path.basename(self.files[self.current_index])}")

    def play(self):
        if not self.is_playing:
            print("not self.is_playing -> play")
            self.play_current()
        elif self.is_paused:
            print("self.is_paused -> play")
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("Resumed.")

    def pause(self):
        print("-> pause")
        pygame.mixer.music.pause()
        self.is_paused = True
        print("Paused.")

    def stop(self):
        print("-> stop")
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        print("Stopped.")

    def next_track(self):
        print("-> next track")
        self.stop()
        self.current_index = (self.current_index + 1) % len(self.files)
        self.play_current()

def start_music_cycle():
    folder_path = "C:/Users/glitc/Documents/Bodenlos/Python/background_music/files"
    try:
        audio_files = load_audio_files(folder_path)
    except Exception as e:
        print(f"Error: {e}")
        return

    player = AudioPlayer(audio_files)

    while True:
        if player.is_playing and not pygame.mixer.music.get_busy() and not player.is_paused:
            player.next_track()
        if is_playing:
            player.play()
        else:
            player.pause()
        time.sleep(1)

if __name__ == "__main__":
    sound_thread = threading.Thread(target=main, daemon=True)
    sound_thread.start()
    start_music_cycle()
