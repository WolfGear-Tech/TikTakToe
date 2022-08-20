## Installation Guide

Please use this guide on how to install this project.

### Project Requirements

* [Python3.10](https://www.python.org)
* [Poetry](https://python-poetry.org/)

### Firs Steps

```shell
# Install project dependencies
$ poetry install

# Initi Repository
$ git init

# Make First Commit
$ git add .
$ git commit -m "first commit"

# Create your Repository and Configure
$ git remote add <name> <url>

# Push your Commit
$ git push <name>
```

### Configure

If you are using PyQt5 Designer, don't forget to build your .ui file.

```shell
$ pyuic5 -x "autoClicker.ui" -o auto_clicker_UI.py
```

This project organizes own configuration in this way:

* Project **settings** (all non-sensible information) is stored in
  `pyproject.toml`
  

### Build

Use the following commands to install or reinstall Project.

```shell
$ pyinstaller --clean -F -n 'TikTakToe' main.pyw
```