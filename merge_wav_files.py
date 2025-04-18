import os
from pydub import AudioSegment

# Directory containing the .wav files
input_dir = "C:/Users/ubema/OneDrive/Documents/0_ART_COMMISIONS/Julian_Charriere/2025_BLACK_SMOKER/BLACK_SMOKER_SCRIPTS/hydrodownwav/hydrophone_downloader/hydrodownwav_sonifications"
output_dir = input_dir  # Save the merged file in the same directory

# Get a sorted list of all .wav files in the directory
wav_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".wav")])

if len(wav_files) == 0:
    print("No .wav files found in the directory.")
    exit()

# Load the first and last file to determine the new timestamp
first_file = wav_files[0]
last_file = wav_files[-1]

# Extract timestamps from the filenames
first_timestamp = first_file.split("_")[1].split(".")[0]
last_timestamp = last_file.split("_")[1].split(".")[0]

# Create the new filename based on the first and last timestamps
new_filename = f"ICLISTENHF1251_{first_timestamp}_to_{last_timestamp}.wav"
output_path = os.path.join(output_dir, new_filename)

# Merge all .wav files
print("Merging files...")
merged_audio = AudioSegment.empty()
for wav_file in wav_files:
    file_path = os.path.join(input_dir, wav_file)
    audio = AudioSegment.from_wav(file_path)
    merged_audio += audio

# Export the merged audio file
merged_audio.export(output_path, format="wav")
print(f"Merged file saved as: {output_path}")