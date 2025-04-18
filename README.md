# hydrophone_downloader
A command line tool to query data from various hydrophone sources. Each ffolder will also download a bibtex entry for dataset citation, and a metadata.json so that the download query is fully reproducible.
Data is automatically converted to FLAC format for lossless compression. 

## Installation
Requirements: python 3 environment

```pip install git+https://github.com/bnestor/hydrophone_downloader.git```

To edit or add your own data sources:

```
git clone https://github.com/bnestor/hydrophone_downloader.git
cd hydrophone_downloader
pip install -e .
```


## Usage
You may need to get a token from Ocean Networks Canada if you wish to download data from their servers. According to [the documentation](https://wiki.oceannetworks.ca/display/O2A/API+Reference), users should generate the token by "logging in at [http://data.oceannetworks.ca/Profile](http://data.oceannetworks.ca/Profile). Click the "Web Services" tab, then click "Generate Token" "

e585a8ac-4846-4370-8ae1-ee2d69679e70 --> My token

Then you may set your token by running the command:
```
hydrophone-downloader-set-token ONC_token=<your_token_here> # this only needs to be done once
```



Open up a terminal or command prompt and type:
```

VIC:
hydrophone-downloader min_latitude=40 max_latitude=50 min_longitude=-129 max_longitude=-123 min_depth=0 max_depth=1000 start_time="2025-04-14" end_time="2025-04-15" save_dir="C:/Users/ubema/OneDrive/Documents/0_ART_COMMISIONS/Julian_Charriere/2025_BLACK_SMOKER/BLACK_SMOKER_SCRIPTS/hydrodownwav/hydrophone_downloader/hydrodownwav_sonifications"


hydrophone-downloader min_latitude=40 max_latitude=50 min_longitude=-129 max_longitude=-123 min_depth=0 max_depth=1000 start_time="2015-01-01" end_time="2020-12-31" save_dir="/path/to/large/storage"
```

## Supported Hydrophone Sources
- Ocean Networks Canada: [https://www.oceannetworks.ca/](https://www.oceannetworks.ca/)
- Ocean Observatories Initiative: [https://oceanobservatories.org/](https://oceanobservatories.org/)

## Coming Soon
- Log to avoid redundant downloads

## Contributing
If you have a hydrophone source, create a custom class that inherits from `src/configs/base_class.py`. If token-access is required, you may need to modify the `src/configs/token_config.yaml` as well.


# TO BE DONE

Customization to add support for additional hydrophone sources:
---------------------------------------------------------------

Create a custom class that inherits from src/configs/base_class.py.
If the new source requires token-based access, modify the token_config.yaml file.




#understanding the naming
ICLISTENHF1251_20150104T235858.270Z likely represents:

A recording made by the ICLISTEN HF1251 hydrophone.
The recording was captured on January 4, 2015, at 23:58:58.270 UTC.
Why This Naming Convention is Useful
Device Identification: The name includes the hydrophone's model and serial number, making it easy to trace the source of the recording.
Timestamp: The precise timestamp allows users to know exactly when the recording was made, which is critical for scientific analysis and synchronization with other datasets.
Standardized Format: Using a structured naming convention ensures consistency and makes it easier to manage and analyze large datasets.




# Giting hard
=============

If you want to test the experimental branch, please follow these steps:

1. Clone the repository:

Initialize a Git repository
    git init

Create the Initial Commit
Add all the current files to the staging area
    git add .

Commit the current working code as the initial version:
    git commit -m "Initial working version of hydrophone_downloader"

Create a new branch for experimental changes
    git branch experimental

Switch to the experimental branch:
    git checkout experimental

Now, you can make changes in the experimental branch without affecting the main branch.

Switch back to the main branch
    git checkout main

Create a backup branch to preserve the stable version
    git branch stable


Workflow for Experimental Changes Make changes in the experimental branch.
Test your changes thoroughly. 
Commit your changes:
    git add .
    git commit -m "Experimental changes: [describe your changes]"   

If the changes are successful, merge them into the main branch:
    git checkout main
    git merge experimental

If the changes are stable, update the stable branch:
    git checkout stable
    git merge main 


 # Initialize a repository
git init

# Check status
git status

# Stage and commit changes
git add .
git commit -m "Message"

# Create and switch branches
git branch <branch-name>
git checkout <branch-name>

# Merge branches
git checkout main
git merge <branch-name>

# Push changes
git push origin main