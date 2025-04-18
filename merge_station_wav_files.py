import os
from pydub import AudioSegment
from datetime import datetime
from tqdm import tqdm  # For progress bar
from colorama import Fore, Style, init  # For colored terminal output

# Initialize colorama
init(autoreset=True)

# Base directory containing the temporary folders
base_dir = r"C:\Users\ubema\OneDrive\Documents\0_ART_COMMISIONS\Julian_Charriere\2025_BLACK_SMOKER\BLACK_SMOKER_SCRIPTS\hydrodownwav\hydrophone_downloader\hydrodownwav_sonifications"

# Output directory for merged files
output_dir = os.path.join(base_dir, "merged")
os.makedirs(output_dir, exist_ok=True)

# Summary dictionary to track processing details
summary = {
    "total_folders": 0,
    "total_files": 0,
    "skipped_files": [],
}

# Iterate through all station folders in the base directory
for station_folder in os.listdir(base_dir):
    station_path = os.path.join(base_dir, station_folder)
    if not os.path.isdir(station_path) or station_folder == "merged":
        continue  # Skip if not a directory or if it's the merged folder

    print(f"{Fore.CYAN}Processing station folder: {station_folder}")

    # Update summary for folders processed
    summary["total_folders"] += 1

    # Get all .wav files in the station folder
    wav_files = sorted([f for f in os.listdir(station_path) if f.endswith(".wav")])

    if not wav_files:
        print(f"{Fore.YELLOW}No .wav files found in folder: {station_folder}")
        continue  # Skip if no .wav files in the folder

    # Update summary for total files found
    summary["total_files"] += len(wav_files)

    # Extract the hydrophone name and timestamps from the filenames
    first_file = wav_files[0]
    last_file = wav_files[-1]

    print(f"{Fore.GREEN}First file: {first_file}, Last file: {last_file}")

    try:
        # Extract hydrophone name from the first file
        hydrophone_name = first_file.split("_")[0]

        # Extract timestamps from filenames
        first_timestamp = first_file.split("_")[1].split(".")[0]
        last_timestamp = last_file.split("_")[1].split(".")[0]

        # Convert timestamps to date format (YYYYMMDD)
        start_date = datetime.strptime(first_timestamp[:8], "%Y%m%d").strftime("%Y%m%d")
        end_date = datetime.strptime(last_timestamp[:8], "%Y%m%d").strftime("%Y%m%d")
    except (IndexError, ValueError) as e:
        print(f"{Fore.RED}Error extracting hydrophone name or timestamps from filenames in folder: {station_folder}")
        print(f"{Fore.RED}Error details: {e}")
        continue

    # Create a new filename for the merged file
    merged_filename = f"{hydrophone_name}_{start_date}T{end_date}.wav"
    merged_filepath = os.path.join(output_dir, merged_filename)

    # Check if the merged file already exists (commented out for testing)
    # if os.path.exists(merged_filepath):
    #     print(f"{Fore.YELLOW}Merged file already exists: {merged_filepath}. Skipping folder: {station_folder}")
    #     continue

    print(f"{Fore.CYAN}Merging files for hydrophone {hydrophone_name} from {start_date} to {end_date}...")

    # Merge all .wav files in the current folder
    merged_audio = AudioSegment.empty()
    total_files = len(wav_files)

    # Use tqdm for the progress bar
    for wav_file in tqdm(wav_files, desc=f"Merging {station_folder}", unit="file"):
        file_path = os.path.join(station_path, wav_file)
        try:
            audio = AudioSegment.from_wav(file_path)
            merged_audio += audio
        except Exception as e:
            print(f"{Fore.RED}Error processing file: {file_path}")
            print(f"{Fore.RED}Error details: {e}")
            summary["skipped_files"].append(file_path)
            continue

    # Export the merged audio file
    try:
        merged_audio.export(merged_filepath, format="wav")
        print(f"{Fore.GREEN}Merged file saved as: {merged_filepath}")

        # Validate the output file
        if os.path.exists(merged_filepath) and os.path.getsize(merged_filepath) > 0:
            print(f"{Fore.GREEN}Validation successful: {merged_filepath}")
        else:
            print(f"{Fore.RED}Validation failed: {merged_filepath}. File may be corrupted or empty.")
    except Exception as e:
        print(f"{Fore.RED}Error exporting merged file for hydrophone {hydrophone_name}")
        print(f"{Fore.RED}Error details: {e}")

# Print summary report at the end
print(f"{Style.BRIGHT}{Fore.BLUE}Summary Report:")
print(f"{Fore.CYAN}Total Folders Processed: {summary['total_folders']}")
print(f"{Fore.CYAN}Total Files Merged: {summary['total_files']}")
print(f"{Fore.YELLOW}Skipped Files: {len(summary['skipped_files'])}")