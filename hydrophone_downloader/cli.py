"""
cli.py
"""


import hydra
from omegaconf import DictConfig
from dotenv import load_dotenv, set_key
import os
from .downloader import download_data

# Load .env file to get API token
load_dotenv()

@hydra.main(config_path="../configs", config_name="config")
def main(cfg: DictConfig):
    token = os.getenv("ONC_TOKEN")
    
    if not token:
        print("Error: ONC API token not set. Use 'mycli-tool set_token --ONC-token=XXXXXXXX' to set it.")
        return
    
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
        token=token
    )

# Command to set the API token and store it in .env file
def set_token(onc_token: str):
    dotenv_file = ".env"
    set_key(dotenv_file, "ONC_TOKEN", onc_token)
    print(f"ONC API token set successfully.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CLI for setting ONC API token or running the downloader")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for setting the API token
    token_parser = subparsers.add_parser("set_token", help="Set the ONC API token")
    token_parser.add_argument("--ONC-token", required=True, help="Your ONC API token")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "set_token":
        set_token(args.ONC_token)
    else:
        main()

