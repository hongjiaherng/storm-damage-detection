# storm-damage-detection

## Getting Started

### Requirements

- conda >= 24.1.0

If you don't have conda installed, you can download it [here](https://docs.anaconda.com/free/miniconda/miniconda-install/). If you already have conda installed, update it to the latest version with the following:

```bash
$ conda --version
$ conda update -n base conda # update conda to the latest version
```

### Setting Up the Environment

#### Local Machine

Follow these steps to set up the environment on your local machine:

1. Prerequisites: Clone the repository

   - Cloning as a collaborator

   ```bash
   $ git clone https://github.com/hongjiaherng/storm-damage-detection.git
   $ cd <path-to-repo>
   ```

   - Cloning on a machine without your GitHub credentials

   ```bash
   $ git clone https://<personal-access-token>@github.com/hongjiaherng/storm-damage-detection.git # If you are running on a machine without your GitHub credentials
   $ cd <path-to-repo>
   ```

2. Create a new venv: Use either `env-cuda.yml` or `env-cpu.yml` file based on your hardware

   - For CUDA-compatible GPU:

   ```bash
   $ conda env create -f env-cuda.yml
   $ conda activate storm-damage-detection
   ```

   - For CPU (check `env-cpu.yml` if you have a Mac with >= M1 chip):

   ```bash
   $ conda env create -f env-cpu.yml
   $ conda activate storm-damage-detection
   ```

3. Add a jupyter kernel (optional)

- If you intend to use Jupyter Notebook/Lab, follow these steps:

  ```bash
  $ python -m ipykernel install --name storm-damage-detection --display-name storm-damage-detection
  $ jupyter kernelspec list # Now you should see your new venv
  ```

  Note: If you are using editors like VSCode for opening the notebook, the editor will automatically set up the kernel for you.

#### Microsoft Planetary Computer

Assuming that PyTorch image is used for the Microsoft Planetary Computer, follow these steps:

1. Prerequisites: Clone the repository

   ```bash
   $ git clone https://<personal-access-token>@github.com/hongjiaherng/storm-damage-detection.git
   $ cd <path-to-repo>
   ```

2. Upgrade conda to the latest version (24.1.2 at the time of writing)

   ```bash
   $ conda remove -n base -y mamba # Remove mamba if present, new version of conda doesn't need mamba anymore, it causes issues when trying to update conda to the latest version
   $ conda update -n base -y conda # Update conda to the latest version
   ```

3. Create a new venv using `env-cuda.yml`

   ```bash
   $ conda deactivate # deactivate the current venv
   $ conda env create -f env-cuda.yml
   $ conda activate storm-damage-detection
   ```

4. Add a jupyter kernel for the new venv

   ```bash
   $ python -m ipykernel install --name storm-damage-detection --display-name storm-damage-detection --user
   $ jupyter kernelspec list # Now you should see your new venv
   ```

5. Now you can open up a notebook and select the newly created kernel (`storm-damage-detection`) to run the notebook with the new environment.

## Miscellaneous

- Remove a jupyter kernel (if you ever need to)

  ```bash
  $ jupyter kernelspec list # List all kernels, including the venv you want to remove
  $ jupyter kernelspec uninstall <venv-name> # <venv-name> is the name of your venv
  $ jupyter kernelspec list # Now you shouldn't see your new venv
  ```

- Supply a Planetary Computer API key to avoid rate limiting (optional). Refer [here](https://pypi.org/project/planetary-computer/) for more info.

  ```bash
  $ planetarycomputer configure <api-key> # request one from planetary computer hub's token section
  ```

- Download data

  ```bash
  $ python -m scripts.download_data # python ./scripts/download_data.py
  ```
