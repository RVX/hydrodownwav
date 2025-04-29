import os
from pydub import AudioSegment
from datetime import datetime
from tqdm import tqdm  # For progress bar
from colorama import Fore, Style, init  # For colored terminal output
from collections import defaultdict
import shutil  # For checking disk space

# Configuration: Set to True to delete original files after merging
delete_original_files = True  # Set to True to enable deletion

# Initialize colorama
init(autoreset=True)

# Base directory containing the temporary folders
base_dir = r"C:\Users\ubema\OneDrive\Documents\0_ART_COMMISIONS\Julian_Charriere\2025_BLACK_SMOKER\BLACK_SMOKER_SCRIPTS\hydrodownwav\hydrophone_downloader\hydrodownwav_sonifications"

# Output directory for merged files
output_dir = os.path.join(base_dir, "merged")
os.makedirs(output_dir, exist_ok=True)

# Update the summary dictionary to track skipped batches
summary = {
    "total_folders": 0,
    "total_files": 0,
    "skipped_files": [],
    "skipped_batches": [],
    "deleted_files": []  # New key to track deleted files
}

# Function to check available disk space
def check_disk_space(output_dir):
    total, used, free = shutil.disk_usage(output_dir)
    # Convert bytes to GB for readability
    free_gb = free / (1024 ** 3)
    return free_gb

# Iterate through all station folders in the base directory
for station_folder in os.listdir(base_dir):
    station_path = os.path.join(base_dir, station_folder)
    if not os.path.isdir(station_path) or station_folder == "merged":
        continue  # Skip if not a directory or if it's the merged folder

    # Informational Messages
    print(f"{Fore.BLUE}Processing station folder: {station_folder}")

    # Update summary for folders processed
    summary["total_folders"] += 1

    # Get all .wav and .flac files in the station folder
    wav_flac_files = sorted([f for f in os.listdir(station_path) if f.endswith((".wav", ".flac"))])

    if not wav_flac_files:
        # Warnings
        print(f"{Fore.LIGHTYELLOW_EX}No .wav or .flac files found in folder: {station_folder}")
        continue  # Skip if no .wav or .flac files in the folder

    # Update summary for total files found
    summary["total_files"] += len(wav_flac_files)

    # Group files by hydrophone name
    hydrophone_groups = defaultdict(list)
    for audio_file in wav_flac_files:
        hydrophone_name = audio_file.split("_")[0]  # Extract hydrophone name
        hydrophone_groups[hydrophone_name].append(audio_file)

    # Process each hydrophone group
    for hydrophone_name, files in hydrophone_groups.items():
        print(f"{Fore.GREEN}Merging files for hydrophone: {hydrophone_name}")

        # Sort files within the group
        files = sorted(files)

        # Process files in batches of 12 (1-hour batches)
        batch_size = 12
        total_batches = (len(files) + batch_size - 1) // batch_size  # Calculate total number of batches
        for batch_index in range(0, len(files), batch_size):
            batch_files = files[batch_index:batch_index + batch_size]

            # Extract timestamps for the batch
            first_file = batch_files[0]
            last_file = batch_files[-1]
            try:
                first_timestamp = first_file.split("_")[1].split(".")[0]
                last_timestamp = last_file.split("_")[1].split(".")[0]

                # Convert timestamps to date format (YYYYMMDD)
                start_date = datetime.strptime(first_timestamp[:8], "%Y%m%d").strftime("%Y%m%d")
                start_time = first_timestamp[9:15]  # Extract time (HHMMSS)
                end_time = last_timestamp[9:15]  # Extract time (HHMMSS)
            except (IndexError, ValueError) as e:
                print(f"{Fore.RED}Error extracting timestamps from filenames in batch: {hydrophone_name}")
                print(f"{Fore.RED}Error details: {e}")
                continue

            # Create a new filename for the merged batch
            merged_filename = f"{hydrophone_name}_{start_date}T{start_time}_to_{end_time}.wav"
            merged_filepath = os.path.join(output_dir, merged_filename)

            # Check if the merged file already exists
            if os.path.exists(merged_filepath):
                print(f"{Fore.LIGHTYELLOW_EX}Merged file already exists: {merged_filepath}. Skipping this batch.")
                
                # Delete original files if the option is enabled
                if delete_original_files:
                    print(f"{Fore.CYAN}Deleting original files for batch: {batch_files}")
                    for audio_file in batch_files:
                        file_path = os.path.join(station_path, audio_file)
                        try:
                            os.remove(file_path)
                            print(f"{Fore.YELLOW}Deleted original file: {file_path}")
                            summary["deleted_files"].append(file_path)  # Track deleted file
                        except Exception as e:
                            print(f"{Fore.RED}Error deleting file: {file_path}")
                            print(f"{Fore.RED}Error details: {e}")
                continue  # Skip this batch if the file already exists

            # Log the batch number and total batches
            current_batch_number = batch_index // batch_size + 1
            print(f"{Fore.BLUE}Merging batch {current_batch_number}/{total_batches} for hydrophone {hydrophone_name}...")

            # Merge the batch files
            merged_audio = AudioSegment.empty()
            for audio_file in tqdm(batch_files, desc=f"Merging batch {current_batch_number}/{total_batches}", unit="file"):
                file_path = os.path.join(station_path, audio_file)
                
                # Check if the file is too small (e.g., less than 1KB)
                if os.path.exists(file_path) and os.path.getsize(file_path) < 1024:  # 1KB = 1024 bytes
                    print(f"{Fore.LIGHTRED_EX}File too small: {file_path}. Deleting it.")
                    try:
                        os.remove(file_path)
                        print(f"{Fore.YELLOW}Deleted small file: {file_path}")
                        summary["deleted_files"].append(file_path)  # Track deleted file
                    except Exception as e:
                        print(f"{Fore.RED}Error deleting small file: {file_path}")
                        print(f"{Fore.RED}Error details: {e}")
                    continue  # Skip this file and move to the next one

                # Proceed with merging if the file is valid
                if not os.path.exists(file_path):
                    # Log missing file and skip
                    print(f"{Fore.LIGHTRED_EX}File not found: {file_path}")
                    summary["skipped_files"].append(file_path)
                    continue
                try:
                    audio = AudioSegment.from_file(file_path)  # Automatically handles .wav and .flac
                    merged_audio += audio
                except Exception as e:
                    # Log processing error and skip
                    print(f"{Fore.LIGHTRED_EX}Error processing file: {file_path}")
                    print(f"{Fore.LIGHTRED_EX}Error details: {e}")
                    summary["skipped_files"].append(file_path)
                    continue

            # Check disk space before exporting
            free_space_gb = check_disk_space(output_dir)
            if free_space_gb < 1:  # Set a threshold of 1 GB
                print(f"{Fore.RED}Insufficient disk space: {free_space_gb:.2f} GB remaining. Stopping processing.")
                break

            # Export the merged batch
            try:
                merged_audio.export(merged_filepath, format="wav")
                print(f"{Fore.LIGHTGREEN_EX}Merged batch {current_batch_number}/{total_batches} saved as: {merged_filepath}")

                # Validate the output file
                if os.path.exists(merged_filepath):
                    file_size = os.path.getsize(merged_filepath)  # Get file size in bytes
                    min_file_size = 1024 * 1024  # Set minimum file size to 1 MB (1 MB = 1024 * 1024 bytes)
                    if file_size > min_file_size:
                        print(f"{Fore.GREEN}Validation successful: {merged_filepath} ({file_size / (1024 * 1024):.2f} MB)")

                        # Delete original files if the option is enabled
                        if delete_original_files:
                            print(f"{Fore.CYAN}Deleting original files for batch: {batch_files}")
                            for audio_file in batch_files:
                                file_path = os.path.join(station_path, audio_file)
                                try:
                                    os.remove(file_path)
                                    print(f"{Fore.YELLOW}Deleted original file: {file_path}")
                                    summary["deleted_files"].append(file_path)  # Track deleted files
                                except Exception as e:
                                    print(f"{Fore.RED}Error deleting file: {file_path}")
                                    print(f"{Fore.RED}Error details: {e}")
                    else:
                        print(f"{Fore.LIGHTRED_EX}Validation failed: {merged_filepath}. File size is too small ({file_size / (1024 * 1024):.2f} MB).")
                        os.remove(merged_filepath)  # Delete the file
                        print(f"{Fore.YELLOW}Deleted file: {merged_filepath}")
                        summary["skipped_files"].append(merged_filepath)
                else:
                    print(f"{Fore.LIGHTRED_EX}Validation failed: {merged_filepath}. File does not exist.")
                    summary["skipped_files"].append(merged_filepath)
            except Exception as e:
                print(f"{Fore.RED}Error exporting merged batch for hydrophone {hydrophone_name}")
                print(f"{Fore.RED}Error details: {e}")

# Summary Report
print(f"{Style.BRIGHT}{Fore.BLUE}Summary Report:")
print(f"{Fore.LIGHTCYAN_EX}Total Folders Processed: {summary['total_folders']}")
print(f"{Fore.LIGHTCYAN_EX}Total Files Merged: {summary['total_files']}")
print(f"{Fore.LIGHTYELLOW_EX}Skipped Files: {len(summary['skipped_files'])}")
for skipped_file in summary["skipped_files"]:
    print(f"{Fore.LIGHTYELLOW_EX} - {skipped_file}")
print(f"{Fore.LIGHTYELLOW_EX}Skipped Batches: {len(summary['skipped_batches'])}")
for skipped_batch in summary["skipped_batches"]:
    print(f"{Fore.LIGHTYELLOW_EX} - {skipped_batch}")
print(f"{Fore.LIGHTGREEN_EX}Deleted Files: {len(summary['deleted_files'])}")
for deleted_file in summary["deleted_files"]:
    print(f"{Fore.LIGHTGREEN_EX} - {deleted_file}")