# storm-damage-detection

Requirements:

- conda

Cloning in an environment without your GitHub credentials (e.g., Google Colab, Paperspace, etc.)

```bash
$ git clone https://<personal-access-token>@github.com/hongjiaherng/storm-damage-detection.git
```

Cloning (as a collaborator)

```bash
$ git clone https://github.com/hongjiaherng/storm-damage-detection.git
```

Create a new venv

```bash
$ conda env create -f env-cuda.yml # If you have a CUDA-compatible GPU
$ conda env create -f env-cpu.yml # If you don't have a CUDA-compatible GPU
$ conda activate <venv-name>
```

Update dependencies based on the env file

```bash
$ conda env update -f env-cuda.yml # If you have a CUDA-compatible GPU
$ conda env update -f env-cpu.yml # If you don't have a CUDA-compatible GPU
```

Download data

```bash
$ python -m scripts.download_data # python ./scripts/download_data.py
```

Add a new jupyter kernel

```bash
$ jupyter kernelspec list # List all kernels, but you won't see your new venv yet
$ python -m ipykernel install --name <venv-name> --display-name <display-name> # <venv-name> can be the same as <display-name>
$ jupyter kernelspec list # Now you should see your new venv
```

Remove a jupyter kernel (if you ever need to)

```bash
$ jupyter kernelspec list # List all kernels, including your new venv
$ jupyter kernelspec uninstall <venv-name> # <venv-name> is the name of your venv
$ jupyter kernelspec list # Now you shouldn't see your new venv
```

Supplying a Planetary Computer API key to avoid rate limiting (optional). Refer [here](https://pypi.org/project/planetary-computer/) for more info.

```bash
$ planetarycomputer configure <api-key> # request one from planetary computer hub's token section
```
