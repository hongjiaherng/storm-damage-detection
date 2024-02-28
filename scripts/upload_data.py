# Usage: python .\scripts\upload_data.py --folder_path ./data/building_footprint_roi --path_in_repo building_footprint_roi
import os
import argparse
from huggingface_hub import HfApi
from dotenv import load_dotenv


if __name__ == "__main__":
    # accept cli arguments
    parser = argparse.ArgumentParser(description="Upload data to the Hugging Face Hub")
    parser.add_argument("--folder_path", type=str, required=True, help="Path to the folder with data to upload")
    parser.add_argument("--path_in_repo", type=str, required=True, help="Path in the repository to upload the data to")
    args = parser.parse_args()

    # unpack cli arguments
    folder_path = args.folder_path
    path_in_repo = args.path_in_repo

    # ask for double confirmation
    print(f"You'll upload data from '{folder_path}' to '{path_in_repo}' in the repository. Are you sure? (y/n)", end=" ")
    confirmation = input()
    if confirmation.lower() != "y":
        print("Aborting...")
        exit(1)

    # load environment variables from .env file
    load_dotenv()

    # init hf api
    api = HfApi(token=os.getenv("HF_HUB_TOKEN"))

    # upload folder
    api.upload_folder(
        folder_path=folder_path,
        path_in_repo=path_in_repo,
        repo_id="jherng/storm-damage-detection",
        repo_type="dataset",
    )

    print("Data uploaded successfully!")
