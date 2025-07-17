# AI MultiMedia Transcriber

AI MultiMedia Transcriber helps you generate srt subtitles from multimedia files like mp4, mkv, wav or mp3, or even from a YouTube video URL.

## Note:

- Python 3.10 must be installed for this script! You can get python-3.10.11-amd64.exe from this [link](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe) if you have Windows.
- The `AI_MultiMedia_Transcriber.py` Python script can use CUDA GPU processing so it can run faster, or it will use CPU if CUDA is not available. This uses the medium size voice recognition model for GPU and if it falls to CPU it uses the small sized model.
- It needs `FFmpeg` to be present in the operating system and registered in PATH in Environment Variables for Windows users.
- For GPU CUDA processing, it needs the latest supported NVIDIA GPU Computing Toolkit to be installed with cuDNN version 8.9.7.29.
- The `AI_MultiMedia_Transcriber-Forced-EN-LargeV3.py` and `AI_MultiMedia_Transcriber-Forced-EN-LargestV2.py` versions are to be used in case the first script fails to recognize the source language correctly.
  Both scripts can use CUDA GPU processing so it can run faster, or it will use CPU if CUDA is not available. If your GPU has less than 12GB VRAM, like 4GB, 6GB, 8GB VRAM you can use `AI_MultiMedia_Transcriber-Forced-EN-LargeV3.py` since it's smaller than the v2.
- The voice recognition model is available in the `small` size, `medium` size, `large(v3)`, and `largest size(v2)`. The scripts use their indicated size voice recognition model for GPU and if it falls to CPU it uses the small sized model.
- The script has a `requirements.txt` that contains required dependencies as listed bellow.



## Requirements:

- `faster-whisper`
- `ffmpeg-python`
- `pytubefix`
- `tk`
- `torch==2.4.1+cu124`


## Therefore AI MultiMedia Transcriber performs the following actions:

1. It starts by prompting the user to select a Source multimedia file.
2. It extracts a wav audio file from the source file or URL link.
3. It starts the transcribe process and generates a text file (.txt) named as the input file in the current working directory.
4. You can then click the `Convert_Subtitle_TimeFrame.exe` OR run the `Convert_Subtitle_TimeFrame.py` script to convert the timeframe from the respective text file and it generates an srt subtitle file also named after the input file in the current working directory.
5. It is meant to use the GPU device with CUDA but if it's not available, it falls back to using CPU.

## Full Description:

AI MultiMedia Transcriber is a Python script that helps you create subtitles for your videos and audio files. It utilizes the power of Whisper, an OpenAI voice recognition model, to convert the audio track into text that can be converted into srt timeframe type subtitle format.

- It supports various formats of multimedia files like MP4, MKV, WAV, MP3, or simply a YouTube video URL provided by the user.
- It does Automatic Audio Extraction so there's no need to extract audio separately, the script handles it for you.
- The Text to Subtitle Conversion script generates a subtitle file (.srt) compatible with all video players.
- GPU Acceleration is Optional so it uses NVIDIA GPUs for faster processing but it seamlessly switches to CPU if a compatible GPU isn't available.





<br><br>


<br><br>





**Script Developer:** Gabriel Mihai Sandu  
**GitHub Profile:** [https://github.com/Gabrieliam42](https://github.com/Gabrieliam42)
