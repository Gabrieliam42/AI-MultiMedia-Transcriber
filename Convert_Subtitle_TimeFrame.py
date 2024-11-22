# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import os
import glob

def convert_to_srt(input_file, output_file):
    try:
        # Attempt to open the file with utf-8 encoding
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            content = infile.readlines()
            process_content(content, outfile)

    except UnicodeDecodeError:
        try:
            # Read the file as raw bytes for fallback decoding
            with open(input_file, 'rb') as infile:
                content_bytes = infile.read()

            # Attempt to decode using Latin-1 as a fallback
            content = content_bytes.decode('latin-1').splitlines()
        except UnicodeDecodeError:
            try:
                # Fallback to Latin-2 if both UTF-8 and Latin-1 fail
                content = content_bytes.decode('latin-2').splitlines()
            except UnicodeDecodeError:
                raise ValueError("Failed to decode the file with UTF-8, Latin-1, and Latin-2 encodings.")

        print("UTF-8 encoding failed, retrying with 'latin-1' or 'latin-2' encoding...")
        try:
            # Process the decoded content and write to the output file
            with open(output_file, 'w', encoding='utf-8') as outfile:
                process_content(content, outfile)
        except Exception as e:
            print(f"Failed to process content: {e}")

def process_content(content, outfile):
    srt_content = []
    index = 1

    # To track repeating lines
    repeat_count = 0
    last_text = None

    for line in content:
        if 's -> ' in line:
            parts = line.split('s -> ')
            start_time = float(parts[0].strip('[').strip('s'))
            end_time, text = parts[1].split('s]')
            end_time = float(end_time.strip())
            text = text.strip()

            # Check for repeated text
            if text == last_text:
                repeat_count += 1
            else:
                repeat_count = 1
                last_text = text

            # If repeated more than three times, clear the text
            if repeat_count > 3:
                text = ""

            # Format SRT times
            start_time_str = format_time(start_time)
            end_time_str = format_time(end_time)

            # Append to SRT content with cleared or original text
            srt_content.append(f"{index}\n{start_time_str} --> {end_time_str}\n{text}\n")
            index += 1

    outfile.write('\n'.join(srt_content))

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

if __name__ == "__main__":
    # Detect and delete WAV files
    wav_files = glob.glob(os.path.join(os.getcwd(), "*.wav"))
    for wav_file in wav_files:
        print(f"Found WAV file: {wav_file}")
        try:
            os.remove(wav_file)
            print(f"Deleted WAV file: {wav_file}")
        except Exception as e:
            print(f"Failed to delete WAV file: {e}")

    # Detect all .txt files in the current working directory, excluding requirements.txt
    txt_files = [
        file for file in glob.glob(os.path.join(os.getcwd(), '*.txt'))
        if os.path.basename(file).lower() != 'requirements.txt'
    ]

    if not txt_files:
        print("No valid .txt file found in the current directory!")
    else:
        # Use the first detected .txt file
        input_file = txt_files[0]
        output_file = os.path.splitext(input_file)[0] + '.srt'
        
        print(f"Detected input file: {input_file}")
        print(f"Generating output file: {output_file}")

        # Convert the detected .txt file to SRT format
        convert_to_srt(input_file, output_file)
        print(f"The subtitle file '{output_file}' has been generated!")

        # Delete the input .txt file after the SRT file has been generated
        try:
            os.remove(input_file)
            print(f"Deleted the input file: {input_file}")
        except Exception as e:
            print(f"Failed to delete the input file: {e}")
