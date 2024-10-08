import argparse
import logging
import subprocess
import os
import shutil
import warnings
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from huggingface_hub.repository import Repository, is_local_clone
from huggingface_hub import snapshot_download

ROOT_PATH = Path(__file__).parent.parent.resolve().as_posix()
HUB_PATH = Path(ROOT_PATH, "datasets/storm-damage-detection/hub").as_posix()
WORKING_PATH = Path(ROOT_PATH, "datasets/storm-damage-detection/working").as_posix()
REPO_ID = "jherng/storm-damage-detection"
REPO_URL = f"https://huggingface.co/datasets/{REPO_ID}"


# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

# Load env variables
load_dotenv()
HF_TOKEN = os.getenv("HF_HUB_TOKEN", None)
if HF_TOKEN is None:
    raise ValueError("Please set the HF_HUB_TOKEN environment variable in a .env file at the project root.")


def prepare_hub_dataset(includes: List[str]) -> bool:
    """Prepare the dataset for upload to the Hugging Face Hub."""

    try:
        if not is_local_clone(HUB_PATH, remote_url=REPO_URL):  # Check if the dataset is a git lfs clone
            logger.error(
                "The dataset in the hub directory is not a git cloned repository. Please clone the dataset first."
            )
            return False

        logger.info("Clearing any existing files in the hub directory.")
        for fname in includes:
            if Path(HUB_PATH, f"{fname}.zip").exists():
                os.remove(Path(HUB_PATH, f"{fname}.zip"))

        for folder in includes:
            logger.info(f"Zipping the {folder} directory.")
            shutil.make_archive(Path(HUB_PATH, folder), "zip", Path(WORKING_PATH, folder))

        return True

    except Exception as e:
        logger.error(f"Failed to prepare the dataset for upload: {e}")
        return False


def prepare_working_dataset(includes: List[str]) -> None:
    """Prepare the working directory for the dataset."""
    logger.info("Clearing any existing files in the working directory.")
    os.makedirs(WORKING_PATH, exist_ok=True)
    shutil.rmtree(WORKING_PATH)  # Remove any existing files in the working dir

    # Unzip the dataset to the working directory
    logger.info("Unzipping the dataset to the working directory.")
    for zip_file in includes:
        shutil.unpack_archive(Path(HUB_PATH, f"{zip_file}.zip"), extract_dir=Path(WORKING_PATH, zip_file))


def upload_to_hub() -> None:
    """Upload the dataset to the Hugging Face Hub."""
    logger.info("Uploading the dataset to the Hugging Face Hub.")
    repo = Repository(local_dir=HUB_PATH, repo_type="dataset", token=HF_TOKEN)
    repo.push_to_hub(auto_lfs_prune=True)


def download_from_hub(with_git_lfs: bool) -> bool:
    """Check if the dataset is already cloned, if not clone it, otherwise pull the latest changes"""
    logger.info("Checking the local dataset repository in the hub directory.")
    os.makedirs(HUB_PATH, exist_ok=True)

    try:
        if not with_git_lfs:
            # Ugly code to force remove the existing files in the hub directory (might contain .git folder which can't be removed by shutil.rmtree)
            if os.name == "nt":
                subprocess.check_output(["cmd", "/C", "rmdir", "/S", "/Q", HUB_PATH])  # windows
            else:
                subprocess.check_output(["rm", "-rf", HUB_PATH])  # unix based

            logger.info(f'Download the dataset repository without Git LFS from "{REPO_URL}".')

            snapshot_download(
                repo_id=REPO_ID,
                repo_type="dataset",
                local_dir=HUB_PATH,
                local_dir_use_symlinks=False,
                token=HF_TOKEN,
            )

        else:  # Download with Git LFS
            if is_local_clone(HUB_PATH, remote_url=REPO_URL):  # Check if the dataset is already cloned
                logger.info(f'Dataset already cloned, pulling any latest change from "{REPO_URL}".')
                repo = Repository(local_dir=HUB_PATH, repo_type="dataset", token=HF_TOKEN)
                repo.git_pull()

            else:
                if len(os.listdir(HUB_PATH)) > 0:  # Check if folder is empty
                    shutil.rmtree(HUB_PATH)

                logger.info(f'Cloning the dataset repository from "{REPO_URL}".')
                repo = Repository(local_dir=HUB_PATH, repo_type="dataset", clone_from=REPO_URL, token=HF_TOKEN)

        return True

    except Exception as e:
        logger.error(f"Failed to clone the dataset repository: {e}")
        return False


if __name__ == "__main__":
    tracked_files = ["sdd", "unprep/all_grids", "unprep/building_footprint_roi", "unprep/raw", "unprep/submission_data", "runs"]

    parser = argparse.ArgumentParser(description="Manage the dataset in the Hugging Face Hub.")

    subparsers = parser.add_subparsers(dest="command", required=True)
    download_parser = subparsers.add_parser("download", help="Download the dataset from the Hugging Face Hub.")
    download_parser.add_argument(
        "--disable_git_lfs",
        action="store_true",
        help="Download the dataset with Git LFS (you won't be able to manage the hub repo with git lfs if this is set to true).",
    )
    upload_parser = subparsers.add_parser("upload", help="Upload the dataset to the Hugging Face Hub.")
    upload_parser.add_argument(
        "--includes",
        nargs="*",
        help="List of zip files to include when uploading the dataset (unchanged file should be excluded for efficiency).",
        choices=tracked_files,
        required=True,
    )
    args = parser.parse_args()

    logger.info(f"Hub directory: {HUB_PATH}")
    logger.info(f"Working directory: {WORKING_PATH}")
    logger.info(f"Hugging Face Hub repository URL: {REPO_URL}")

    if args.command == "upload":
        tracked_files = args.includes
        status = prepare_hub_dataset(tracked_files)

        if status:
            upload_to_hub()
        else:
            logger.error("Failed to prepare the dataset for upload to the Hugging Face Hub.")

    else:
        status = download_from_hub(with_git_lfs=not args.disable_git_lfs)
        if status:
            prepare_working_dataset(tracked_files)
            logger.info("Dataset is ready for use at working directory.")
        else:
            logger.error("Failed to download the dataset from the Hugging Face Hub.")
