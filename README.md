
 AI MultiMedia Transcriber helps you generate srt subtitles from multimedia files like mp4, mkv, wav or mp3 or even from a YouTube video URL.


  Note:

	This AI_MultiMedia_Transcriber.py Python script can use CUDA GPU processing so it can run faster,
 	or it can use CPU if CUDA is not available.

	It needs FFmpeg to be present in the operating system and registered.

	The script has a requirements.txt that contains the list of dependencies so those need
 	to be installed.

	For GPU CUDA processing it needs the latest supported NVIDIA GPU Computing Toolkit to be installed
 	with cuDNN version 8.9.7.29.


	Therefore AI MultiMedia Transcriber performs the following actions:

	1. It starts by prompting the user to select a Source multimedia file.

	2. It extracts a wav audio file from the source file.

	3. It starts the transcribe process and it generates a text file named subtitle.txt
 	   in the current working directory.

	4. You can then run the Convert_Subtitle_TimeFrame.py script to convert the timeframe
 	   from subtitle.txt and it generates a srt subtitle file named subtitle.srt in the
	   current working directory.

	5. It tries to use the GPU device with CUDA but if it's not available
 	   it falls back to using CPU.

  Full Description:

	AI MultiMedia Transcriber is a Python script that helps you easily create subtitles
 	for your videos and audio files. It utilizes the power of Whisper, an OpenAI voice recognition model,
  	to convert the audio track into text that can be converted into srt timeframe type subtitle format.

	It supports various formats of multimedia files like MP4, MKV, WAV, MP3, or simply a YouTube video URL
	provided by the user.
	It does Automatic Audio Extraction so there's no need to extract audio separately, the script handles it
	for you.
	The Text to Subtitle Conversion script generates a subtitle file (.srt) compatible with all video players.
	GPU Acceleration is Optional so it uses NVIDIA GPUs for faster processing but it seamlessly switches
	to CPU if a compatible GPU isn't available.
