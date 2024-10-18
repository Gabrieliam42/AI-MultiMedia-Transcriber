# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import os

def convert_to_srt(input_file, output_file):
    try:
        # Attempt to open the file with utf-8 encoding
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            content = infile.readlines()
            process_content(content, outfile)
    
    except UnicodeDecodeError:
        try:
            # Attempt to decode using Latin-1 as a fallback
            content = content_bytes.decode('latin-1')
        except UnicodeDecodeError:
            try:
                # Fallback to Latin-2 if both UTF-8 and Latin-1 fail
                content = content_bytes.decode('latin-2')
            except UnicodeDecodeError:
                raise ValueError("Failed to decode the file with UTF-8, Latin-1, and Latin-2 encodings.")
    
        print("UTF-8 encoding failed, retrying with 'latin-1' encoding...")
        try:
            # Fallback to latin-1 encoding
            with open(input_file, 'r', encoding='latin-1') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
                content = infile.readlines()
                process_content(content, outfile)
        except Exception as e:
            print(f"Failed to open file: {e}")

def process_content(content, outfile):
    srt_content = []
    index = 1

    for line in content:
        if 's -> ' in line:
            parts = line.split('s -> ')
            start_time = float(parts[0].strip('[').strip('s'))
            end_time, text = parts[1].split('s]')
            end_time = float(end_time.strip())
            text = text.strip()

            start_time_str = format_time(start_time)
            end_time_str = format_time(end_time)

            srt_content.append(f"{index}\n{start_time_str} --> {end_time_str}\n{text}\n")
            index += 1

    outfile.write('\n'.join(srt_content))

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

if __name__ == "__main__":
    input_file = os.path.join(os.getcwd(), 'subtitle.txt')
    output_file = os.path.join(os.getcwd(), 'subtitle.srt')
    convert_to_srt(input_file, output_file)
    print("The subtitle file 'subtitle.srt' has been generated!")
