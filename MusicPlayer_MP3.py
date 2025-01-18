import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        
        # Initialize player state
        self.is_playing = False
        self.is_paused = False
        self.playlist = []

        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Play button
        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

        # Pause button
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=1, padx=10, pady=10)

        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=10, pady=10)

        # Playlist box
        self.playlist_box = tk.Listbox(self.root, height=10, width=50)
        self.playlist_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Add song button
        self.add_button = tk.Button(self.root, text="Add Song", command=self.add_song)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        # Remove song button
        self.remove_button = tk.Button(self.root, text="Remove Song", command=self.remove_song)
        self.remove_button.grid(row=2, column=1, padx=10, pady=10)

    def play_music(self):
        if self.playlist_box.curselection():
            song_index = self.playlist_box.curselection()[0]
            song = self.playlist[song_index]
            
            # Load and play the selected song
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0, start=0.0)
            
            self.is_playing = True
            self.is_paused = False
            self.update_button_text()

    def pause_music(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.update_button_text()

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.update_button_text()

    def update_button_text(self):
        # Update the button text based on player state
        if self.is_playing:
            self.play_button.config(text="Pause")
        else:
            self.play_button.config(text="Play")
        
        if self.is_paused:
            self.play_button.config(text="Resume")

    def add_song(self):
        # Open a file dialog to select an MP3 file
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        
        if file_path:
            self.playlist.append(file_path)
            self.playlist_box.insert(tk.END, os.path.basename(file_path))

    def remove_song(self):
        # Remove selected song from the playlist
        selected_song = self.playlist_box.curselection()
        if selected_song:
            song_index = selected_song[0]
            self.playlist_box.delete(song_index)
            del self.playlist[song_index]

def main():
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()