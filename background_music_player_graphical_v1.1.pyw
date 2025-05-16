import time
import threading
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
import pythoncom
import pygame
import os


##### IM NOT GOOD AT PYTHON
##### THIS IS ONE OF MY FIRST PYTHON PROJECTS

##### IF YOU ENCOUNTER CPU USAGE PROBLEMS THERE ARE SLEEP TIMERS IN HERE, WHICH ARE COMMENTED OUT
##### USING THESE WILL FREE UP CPU BUT ALSO SLOW DOWN THE SYSTEM, CAN CAUSE LATE TO NO DETECTIONS
##### ESPECIALLY WITH SHORT SOUNDS

##### WHEN HAVING ISSUES OF IT DETECTING SOUNDS IT SHOULDN'T DETECT, OR YOU SIMPLY WANT EXCLUSISIONS
##### TWEAK  > excluded_process_names <  IN  > is_sound_playing(threshold=0.01) <  FIRST FUNCTION BTW

##### IF YOU NEED A SILENCE DELAY HIGHER THAN PROVIDED BY THE SCALE, EITHER EDIT THE DEFAULT HERE,
##### OR THE CONFIG
##### EITHER WAY MAKE SURE TO CHANGE THE  > to= <  IN  > silence_delay_scale  <
##### CAN BE FOUND IN  > gui_loop() <  
##### OTHERWISE YOUR SAVE FILE WILL RESET (except the folder_path)

##### IF YOU NEED MORE EXTENSIONS (other than .mp3 and .wav) EDIT
#####   > AUDIO_EXTENSIONS <  UNDERNEATH THE SECOND FUNCTION

##### tweak this code to your liking



##### VARIABLES #####
silence_delay = 5  # seconds to wait before playing music on silence
folder_path = None # the folder containing your .mp3s (note: .wav is enabled but not tested)


script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.txt")


# Shared variables
is_playing = False
player = None

def is_sound_playing(threshold=0.01):
    sessions = AudioUtilities.GetAllSessions()
    excluded_process_names = {"python.exe", "pythonw.exe", "audiodg.exe", "rainmeter.exe"}  # Add any you want to exclude
    
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
    while running:
        if monitoring:
            is_playing = not is_sound_playing()
#        time.sleep(0.1)

# Audio playback code
pygame.mixer.init()
AUDIO_EXTENSIONS = (".mp3", ".wav") # if your audio doesn't have these extensions they will be ignored (i hope)

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
        self.just_skipped = False

    def play_current(self):
        print("-> play current")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(self.files[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        print(f"Playing: {os.path.basename(self.files[self.current_index])} \n")
        global current_file
        update_window_title("Background Music Player - " + os.path.basename(self.files[self.current_index]))

    def play(self):
        if not self.is_playing:
            print("-> play ... not self.is_playing ")
            self.play_current()
        elif self.is_paused:
            print("-> play ... self.is_paused")
            pygame.mixer.music.unpause()
            self.is_paused = False

    def pause(self):
        if self.is_paused == False:
            print("-> pause")
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop(self):
        print("-> stop")
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def next_track(self):
        self.stop()
        print("-> next track")
        self.current_index = (self.current_index + 1) % len(self.files)
        self.play_current()


printed = False
def start_music_cycle():
    load_config()
    threading.Thread(target=save_loop, daemon=True).start()

    folder_printer()
    global printed

    while folder_path is None and running:
        time.sleep(0.2)

    printed = False
    folder_printer()
    try:
        audio_files = load_audio_files(folder_path)
    except Exception as e:
        print(f"Error: {e}")
        return

    global player
    player = AudioPlayer(audio_files)
    print("player assigned")

    silence_start_time = None
    last_folder_path = None

    while running:
        if not monitoring:
            time.sleep(0.5)
            continue

        if player.is_playing and not pygame.mixer.music.get_busy() and not player.is_paused:
            if player.just_skipped:
                # Reset the flag, skip auto-skip
                player.just_skipped = False
#                print("auto-proceed suppressed after manual proceed")
            else:
#                print("auto-proceed")
                player.next_track()


        if is_playing:
            if silence_start_time is None:
                silence_start_time = time.time()
            elif time.time() - silence_start_time >= silence_delay:
                player.play()
        else:
            silence_start_time = None
            player.pause()

        if folder_path != last_folder_path:
            last_folder_path = folder_path
            try:
                audio_files = load_audio_files(folder_path)
                player = AudioPlayer(audio_files)
                print("player reloaded with new folder.")
            except Exception as e:
                print(f"Error loading audio: {e}")
                player = None
                time.sleep(1)
                continue

#        time.sleep(0.1)
#        time.sleep(1)


def folder_printer():
    time.sleep(2)
    global printed
    global folder_path
    if printed == False:
        print("folder_path: \n" + str(folder_path) + "\n")
        if folder_path == None:
            print("no folder selected")
            printed = True
        else:
            print("folder selected")
            printed = True




import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import sys
import datetime
from tkinter.scrolledtext import ScrolledText

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.config(state='normal')
#        self.widget.insert(tk.END, text)
#        self.widget.see(tk.END)
#        self.widget.config(state='disabled')
        if text.strip() != '':
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.widget.insert(tk.END, f"[{timestamp}] {text} \n")
            self.widget.see(tk.END)  # Auto-scroll
        self.widget.config(state='disabled')

    def flush(self):
        pass





# Control flags
monitoring = True
running = True

def gui_pause():
    global monitoring
    if player is None:
        print("player not initialized yet.")
        return
    monitoring = False
    player.pause()
    print("System paused.")

def gui_stop():
    global running
    if player is None:
        print("player not initialized yet.")
        return
    running = False
    player.stop()
    print("System stopped.")
    save_config()
    root.quit()

def gui_start():
    global monitoring
    monitoring = True
    print("System resumed.")

def gui_next():
    if player is None:
        print("player not initialized yet.")
        return
    player.just_skipped = True
    print("proceding to next")
    player.next_track()



def gui_loop():
    global root
    root = tk.Tk()
    root.title("Background Music Player")

    start_btn = tk.Button(root, text="Start / Resume System", command=gui_start, width=20)
    pause_btn = tk.Button(root, text="Pause System", command=gui_pause, width=20)
    stop_btn = tk.Button(root, text="Stop & Exit System", command=gui_stop, width=20)

    start_btn.grid(pady=10)
    pause_btn.grid(pady=10)
    stop_btn.grid(pady=10)

    global folder_entry
    folder_entry = tk.Entry(root, width=40)
    folder_entry.grid(padx=(10,0))
    if folder_path:
        folder_entry.insert(0, folder_path)

    browse_btn = tk.Button(root, text="Browse", command=browse_folder)
    browse_btn.grid(padx=10)

    # Output display
    log_output = ScrolledText(root, height=15, width=70, state='normal')
    log_output.grid(padx=10, pady=10)

    sys.stdout = TextRedirector(log_output)
    sys.stderr = TextRedirector(log_output)

    global volume
    volume_scale = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Volume', command=set_volume)
    volume_scale.set(volume)  # default 50%
    volume_scale.grid()

    global silence_delay
    silence_delay_scale = tk.Scale(root, from_=0, to=300, orient='vertical', length=200, label='delay before playing in sec', command=set_silence_delay)
    silence_delay_scale.set(silence_delay) # default 5
    silence_delay_scale.grid(column=1, row=5)

    next_btn = tk.Button(root, text="Next file (not reliable)", command=gui_next, width=20)
    next_btn.grid(column=1, row=4)

    root.mainloop()

def update_window_title(title):
    if root and root.winfo_exists():
        root.after(0, lambda: root.title(title))



def browse_folder():
    global folder_entry
    global folder_path
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)
        folder_path = folder_selected
    save_config()


volume = 50
def set_volume(val):
    global volume
    if val != None:
        volume = float(val) / 100
    else:
        volume = float(volume) / 100
    if player:
        pygame.mixer.music.set_volume(volume)
    save_config()


def set_silence_delay(val):
    global silence_delay
    silence_delay = int(val)
    save_config()



def save_config():
    global volume
    global folder_path
    with open(config_path, "w") as f:
        f.write(f"volume={volume}\n")
        f.write(f"folder_path={folder_path}\n")
        f.write(f"silence_delay={silence_delay}\n")
#        print("written: ", volume, "   ", folder_path)

def load_config():
    print(config_path)
    global volume
    global folder_path
    global silence_delay
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("volume="):
                    volume = int(float(line.strip().split("=")[1]) * 100)
                elif line.startswith("folder_path="):
                    folder_path = line.strip().split("=", 1)[1]
                elif line.startswith("silence_delay="):
                    silence_delay = int(line.strip().split("=", 1)[1])
    return volume, folder_path


def save_loop():
    pass
#    while running:
#        time.sleep(5)
#        save_config()


if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    threading.Thread(target=start_music_cycle, daemon=True).start()
    gui_loop()
#    threading.Thread(target=update_loop, daemon=True).start()