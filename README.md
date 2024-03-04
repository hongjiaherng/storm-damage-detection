# storm-damage-detection

## Getting Started

### Requirements

- conda >= 24.1.0

If you don't have conda installed, you can download it [here](https://docs.anaconda.com/free/miniconda/miniconda-install/). If you already have conda installed, update it to the latest version with the following:

```bash
conda --version
conda update -n base conda # Update conda to the latest version
```

### Setting Up the Environment

<details>
<summary><b>Local Machine</b></summary>

Follow these steps to set up the environment on your local machine:

1. Prerequisites: Clone the repository

   ```bash
   # Cloning as a collaborator
   git clone https://github.com/hongjiaherng/storm-damage-detection.git

   # Or if you are running on a machine without your GitHub credentials
   git clone https://<personal-access-token>@github.com/hongjiaherng/storm-damage-detection.git

   cd <path-to-repo>
   ```

2. Create a new venv: Use either `env-cuda.yml` or `env-cpu.yml` file based on your hardware

   ```bash
   # For CUDA-compatible GPU:
   conda env create -f env-cuda.yml
   conda activate storm-damage-detection

   # For CPU (Some actions needed on `env-cpu.yml` if you have a Mac with >= M1 chip):
   conda env create -f env-cpu.yml
   conda activate storm-damage-detection
   ```

3. Add a jupyter kernel (optional)

   If you intend to use Jupyter Notebook/Lab, follow these steps:

   ```bash
   python -m ipykernel install --name storm-damage-detection --display-name storm-damage-detection
   jupyter kernelspec list # Now you should see your new venv
   ```

   _Note: If you are using editors like VSCode for opening the notebook, the editor will automatically set up the kernel for you._

</details>

<details>
<summary><b>Microsoft Planetary Computer</b></summary>

Follow these steps to set up the environment on Microsoft Planetary Computer:

1. Prerequisites: Clone the repository

   ```bash
   git clone https://<personal-access-token>@github.com/hongjiaherng/storm-damage-detection.git
   cd <path-to-repo>
   ```

2. Update conda to the latest version (24.1.2 as of writing)

   <details open>
   <summary>Image: <b>GPU - PyTorch</b></summary>

   ```bash
   # Remove mamba if present, newer conda doesn't need mamba anymore. Currently, it causes conflict when trying to update conda to the latest version
   conda remove -n base -y mamba
   conda update -n base -y conda # Update conda to the latest version
   ```

   </details>

   <details open>
   <summary>Image: <b>CPU - Python</b></summary>

   ```bash
   # Reset the default solver to classic
   conda config --show solver # It should show "libmamba" but it's unusable for running conda install
   conda config --set solver classic

   # Force remove mamba (the conflicting package for upgrading to conda >= 24.1)
   conda remove -n base -y --force mamba # Remove mamba if present, newer conda doesn't need mamba anymore

   # Update conda to the latest version
   conda update -n base -y conda # Update conda to the latest version

   # Set the solver back to libmamba
   conda config --set solver libmamba
   conda config --show solver # It should show "libmamba"
   ```

   _Note: The version of conda on this image is broken (version 23.1.0): It doesn't support `libmamba` as the solver but it's still being set as the default solver._
   </details>

3. Create a new venv using `env-cuda.yml` or `env-cpu.yml` file based on your hardware. Also, check the file for any changes in the dependencies based on your environment _(Some actions needed if you're on Linux)_.

   ```bash
   conda deactivate # Deactivate the current venv

   conda env create -f env-cuda.yml # For GPU - PyTorch image
   conda env create -f env-cpu.yml # Or for CPU - Python image

   conda activate storm-damage-detection # Activate the new venv
   ```

4. Add a jupyter kernel for the new venv

   ```bash
   python -m ipykernel install --name storm-damage-detection --display-name storm-damage-detection --user
   jupyter kernelspec list # Now you should see your new venv
   ```

5. Now you can open up a notebook and select the newly created kernel (`storm-damage-detection`) to run the notebook.

</details>

## Miscellaneous

- Managing dataset

  - Download locally

    ```bash
    # Clone the dataset locally as a git-lfs repo, this is mandatory if you'd like to perform uploading to HF Hub
    # - git-lfs is required, download it from https://git-lfs.com/
    python -m scripts.manage_dataset download

    # Download the dataset locally without treating it as a git-lfs repo, thus you can't perform uploading with this setting
    # - useful for cloud VM that doesn't have git-lfs install (or you don't have the permission)
    python -m scripts.manage_dataset download --disable_git_lfs
    ```

  - Upload to HF Hub
    ```bash
    # After making changes to the datasets/storm-damage-detection/working directory, you can now run this script to push the latest changes to HF Hub
    # Supported --includes choices:
    # - sdd
    # - unprep/all_grids
    # - unprep/building_footprint_roi
    # - unprep/raw
    # - unprep/submission_data
    python -m scripts.manage_dataset upload --includes <folder-to-upload-1> <folder-to-upload-2> ... <folder-to-upload-n>
    ```
  - Structure

    Currently, the dataset is structured as described below:

    ```bash
    - datasets/
      - storm-damage-detection/
        - hub/    # hf hub's copy of the dataset, don't make change to this manually
          - unprep/
            - all_grids.zip
            - building_footprint_roi.zip
            - raw.zip
            - submission_data.zip
          - .gitattributes
          - sdd.zip
          - README.md
        - working/    # working copy of the dataset, make changes here
          - sdd/
            - train/
              - images/*.jpg
              - labels/*.txt
            - val/
              - images/*.jpg
              - labels/*.txt
            - test/
              - images/*.jpg
              - labels/*.txt
            - sdd.yaml
            - train.txt
            - val.txt
            - test.txt
          - unprep/    # this is where you'll find the unprocessed data
            - all_grids/
              - post_event/...
              - pre_event/...
            - building_footprint_roi/...
            - raw/...
            - submission_data/...
    ```

    You are expected to only make changes to the dataset within the 5 main folders `["sdd", "unprep/all_grids", "unprep/building_footprint_roi", "unprep/raw", "unprep/submission_data"]`. After you update the contents in the folder, you can then run the upload script as shown above to upload the latest changes to HF Hub. Under the hood, it'll zip each of the folders, and override them in the `datasets/storm-damage-detection/hub` directory.

- Remove a jupyter kernel (if you ever need to)

  ```bash
  jupyter kernelspec list # List all kernels, including the venv you want to remove
  jupyter kernelspec uninstall <venv-name> # <venv-name> is the name of your venv
  jupyter kernelspec list # Now you shouldn't see your new venv
  ```

- Supply a Planetary Computer API key to avoid rate limiting (optional, also not needed on Microsoft Planetary Computer). Refer [here](https://pypi.org/project/planetary-computer/) for more info.

  ```bash
  planetarycomputer configure <api-key> # request one from planetary computer hub's token section
  ```
