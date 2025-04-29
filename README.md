# hydrophone_downloader

A command-line tool to query data from various hydrophone sources and merge `.wav` files from hydrophone stations into a single `.wav` file for each station. Each folder will also download a BibTeX entry for dataset citation and a `metadata.json` file so that the download query is fully reproducible. Data is automatically converted to FLAC format for lossless compression.

---

## Features

### Hydrophone Downloader
- Query data from supported hydrophone sources.
- Automatically download metadata and citation information.
- Convert downloaded data to FLAC format for lossless compression.

### WAV File Merger
- Merges `.wav` files in chronological order.
- Automatically generates filenames based on the hydrophone name and timestamps.
- Displays progress bars and colored terminal output for better visibility.
- Validates the output files to ensure successful merging.

---

## Installation

nstallation
Install the hydrophone downloader package:
pip install git+https://github.com/bnestor/hydrophone_downloader.git

git clone https://github.com/bnestor/hydrophone_downloader.git
cd hydrophone_downloader
pip install -e .



### Requirements
- **Python**: Version 3.7 or higher.
- **FFmpeg**: Required for audio processing with `pydub`.
- **Python Libraries**:
  - `pydub`
  - `tqdm`
  - `colorama`

Install the required Python libraries using:
```bash
pip install -r [requirements.txt](http://_vscodecontentref_/1)
```
WAV File Merger
Usage
Place the folders containing .wav files in the input directory:

C:/path/to/input_directory/
├── station1/
│   ├── file1.wav
│   ├── file2.wav
│   └── ...
├── station2/
│   ├── file1.wav
│   ├── file2.wav
│   └── ...

# Run the script:
python merge_station_wav_files.py

# The merged files will be saved in the merged folder inside the input directory:
C:/path/to/input_directory/merged/
├── station1_YYYYMMDDTYYYYMMDD.wav
├── station2_YYYYMMDDTYYYYMMDD.wav
└── ...

# Example Output
Processing station folder: station1
First file: file1.wav, Last file: file10.wav
Merging files for hydrophone station1 from 20220101 to 20220102...
Merging station1: 100%|█████████████████████████████████████████████| 10/10 [00:05<00:00, 2.00file/s]
Merged file saved as: C:/path/to/input_directory/merged/station1_20220101T20220102.wav
Validation successful: C:/path/to/input_directory/merged/station1_20220101T20220102.wav

Summary Report:
Total Folders Processed: 2
Total Files Merged: 20
Skipped Files: 0

# Understanding the Naming Convention
ICLISTENHF1251_20150104T235858.270Z likely represents:

A recording made by the ICLISTEN HF1251 hydrophone.
The recording was captured on January 4, 2015, at 23:58:58.270 UTC.