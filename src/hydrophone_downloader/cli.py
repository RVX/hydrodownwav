"""
cli.py
"""


import hydra
from omegaconf import DictConfig
from dotenv import load_dotenv, set_key
import os


from hydrophone_downloader.downloader import download_data



# # Load .env file to get API token
# load_dotenv()
# token = os.getenv("ONC_TOKEN")


@hydra.main(config_path="../configs", config_name="config", version_base="1.3")
def main(cfg: DictConfig):
    
    
    download_data(
        min_lat=cfg.min_latitude, 
        max_lat=cfg.max_latitude,
        min_lon=cfg.min_longitude, 
        max_lon=cfg.max_longitude, 
        min_depth=cfg.min_depth,
        max_depth=cfg.max_depth,
        license=cfg.license,
        start_time=cfg.start_time,
        end_time=cfg.end_time,
        save_dir=cfg.save_dir,
    )

# Command to set the API token and store it in .env file
@hydra.main(config_path="../configs", config_name="token_config")
def set_token(cfg: DictConfig):
    # get project root directory
    dotenv_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), '.env')

    set_key(dotenv_file, "ONC_TOKEN", cfg.ONC_token)
    print(f"ONC API token set successfully.")

if __name__ == "__main__":
    main()

