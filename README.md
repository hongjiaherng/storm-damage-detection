# storm-damage-detection

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
$ conda create -n storm-damage-detection python=3.11
$ conda install -r requirements.txt
```

Download data
```bash
$ python -m scripts.download_data # python ./scripts/download_data.py
```