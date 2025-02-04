# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import tkinter as tk
from tkinter import messagebox, filedialog
import ffmpeg
import torch
import os
import pytubefix as pytube
from faster_whisper import WhisperModel
import math
import sys
import ctypes
import subprocess

os.environ["HUGGINGFACE_HUB_CACHE"] = os.getcwd()

def check_admin():
    """Check if the user has administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False

def main():
    if sys.platform != 'win32':
        print("This script only runs on Windows")
        sys.exit(1)

    if not check_admin():
        subprocess.run(['runas', '/user:Administrator', sys.executable, __file__])
        sys.exit(0)

    root.mainloop()

class Logger(object):
    def __init__(self, video_file):
        log_file = os.path.join(os.getcwd(), f"{os.path.splitext(os.path.basename(video_file))[0]}.txt")
        self.terminal = sys.stdout
        self.log = open(log_file, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message.encode("utf-8", "replace").decode("utf-8"))
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def extract_audio_from_video(video_file):
    print(f"Extracting audio from {video_file}...")

    audio_file = f"{os.path.basename(video_file)}.wav"

    try:
        ffmpeg.input(video_file).output(audio_file).run(overwrite_output=True)
        print(f"Audio extracted successfully: {audio_file}")
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        print(f"FFmpeg error: {error_message}")
        raise e

    return audio_file

def transcribe_audio_file(audio_file):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running device: {device}")
        model_name = "medium" if device == "cuda" else "small"
        
        try:
            model = WhisperModel(model_name, device=device)
            segments, info = model.transcribe(audio_file)
            language_code = info.language
            print(f"Detected language code: {language_code}")
            segment_list = list(segments)
        
        except RuntimeError as e:
            if "no kernel image is available for execution on the device" in str(e):
                print("CUDA execution failed, falling back to CPU.")
                device = "cpu"
                model = WhisperModel(model_name, device=device)
                segments, info = model.transcribe(audio_file)
                language_code = info.language
                segment_list = list(segments)
            else:
                raise e
        
        for segment in segment_list:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        return language_code, segment_list
    except Exception as e:
        messagebox.showwarning("Transcription Error", f"An error occurred during transcription: {e}")
        return None, []

def convert_time_to_srt_format(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def save_subtitles_as_srt(video_file, segments):
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    subtitle_filename = os.path.join(os.getcwd(), f"{base_name}.srt")
    srt_content = ""

    if segments:
        for index, segment in enumerate(segments):
            start_time = convert_time_to_srt_format(segment.start)
            end_time = convert_time_to_srt_format(segment.end)

            srt_content += f"{index + 1}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{segment.text}\n\n"
    else:
        srt_content = "1\n00:00:00,000 --> 00:00:05,000\n(No transcription available)\n\n"

    with open(subtitle_filename, "w", encoding='utf-8') as srt_file:
        srt_file.write(srt_content)

    print(f"Subtitle file saved successfully: {subtitle_filename}")
    return subtitle_filename

def select_media_file():
    file_path = filedialog.askopenfilename(filetypes=[("Media files", "*.mp4 *.mkv *.wav *.mp3")])
    if not file_path:
        messagebox.showwarning("File Selection Error", "Please select a valid media file.")
        return None
    return file_path

def process_selected_file():
    media_file = select_media_file()
    if media_file:
        logger = Logger(media_file)
        sys.stdout = logger

        try:
            if media_file.endswith((".mp4", ".mkv", ".wav", ".mp3")):
                if media_file.endswith((".mp4", ".mkv")):
                    audio_file = extract_audio_from_video(media_file)
                    language_code, segments = transcribe_audio_file(audio_file)
                    if segments:
                        subtitle_file = save_subtitles_as_srt(media_file, segments)
                else:
                    language_code, segments = transcribe_audio_file(media_file)
                    if segments:
                        subtitle_file = save_subtitles_as_srt(media_file, segments)

                messagebox.showinfo("Success", f"Transcription and subtitles saved to: {subtitle_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            sys.stdout = logger.terminal
            logger.log.close()

def process_youtube_video_url():
    youtube_url = url_entry.get()
    if not youtube_url:
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL.")
        return

    try:
        yt_video = pytube.YouTube(youtube_url)
        video_stream = yt_video.streams.get_highest_resolution()

        if video_stream:
            current_directory = os.getcwd()
            print(f"Downloading video: {yt_video.title}")
            video_filename = video_stream.download(output_path=current_directory)
            print(f"Downloaded video saved as: {video_filename}")

            logger = Logger(video_filename)
            sys.stdout = logger

            try:
                audio_file = extract_audio_from_video(video_filename)
                language_code, segments = transcribe_audio_file(audio_file)
                if segments:
                    subtitle_file = save_subtitles_as_srt(video_filename, segments)

                messagebox.showinfo("Success", f"Transcription and subtitles saved to: {subtitle_file}")
            except Exception as e:
                print(f"An error occurred: {e}")
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                sys.stdout = logger.terminal
                logger.log.close()
        else:
            messagebox.showwarning("Download Error", "No suitable video stream was found for download.")
    except pytube.exceptions.PytubeError as e:
        messagebox.showwarning("Pytube Error", f"An error occurred with Pytube: {e}")
    except Exception as e:
        messagebox.showwarning("Error", f"An unexpected error occurred: {e}")

root = tk.Tk()
root.title("AI Multimedia Subtitle Scribe")
root.geometry("640x640")
root.configure(bg='#2e2e2e')

media_file_label = tk.Label(root, text="Select a MP4, MKV, WAV, or MP3 file for transcription:", bg='#2e2e2e', fg='white')
media_file_label.pack(pady=10)

media_file_button = tk.Button(root, text="Select a File", command=process_selected_file, bg='#4d4d4d', fg='white')
media_file_button.pack(pady=20)

youtube_url_label = tk.Label(root, text="Or enter a YouTube video URL:", bg='#2e2e2e', fg='white')
youtube_url_label.pack(pady=10)
url_entry = tk.Entry(root, bg='#4d4d4d', fg='white')
url_entry.pack(pady=10)

youtube_url_button = tk.Button(root, text="Transcribe from URL", command=process_youtube_video_url, bg='#4d4d4d', fg='white')
youtube_url_button.pack(pady=20)

root.mainloop()

if __name__ == "__main__":
    main()
