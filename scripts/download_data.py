# remember about maximum downloaded elements from folder is 50 (https://stackoverflow.com/questions/65001496/how-to-download-a-google-drive-folder-using-link-in-linux)
from pathlib import Path
import os
import gdown
import zipfile


ROOT = Path(__file__).parent.parent.as_posix()
URL = "https://drive.google.com/file/d/1NnBNppQI_6jJ-gAOYA-EcPFEvg5rtPAB/view?usp=drive_link"
ZIP_PATH = os.path.join(ROOT, "data.zip")

if __name__ == "__main__":
    print("Downloading data...")
    gdown.download(URL, output=ZIP_PATH, quiet=False, fuzzy=True)

    print("Extracting data...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(path=ROOT)

    print("Data downloaded and extracted successfully! Cleaning up...")
    os.remove(ZIP_PATH)
