## mkprj

A basic CLI tool to create bare-bones Python projects, the way I like them.

It will:

- Create a project directory
- Initialize `git`
- Add a `.gitignore`
- Create a virtualenv
- Create a `requirements.txt` with the default requirements, or a comma-separate list specified with `--requirements`
 

## Installation

```bash
pip install mkprj
```

## Usage

```bash
usage: mkprj [-h] [--python PYTHON] [--overwrite] [--requirements REQUIREMENTS] project_path

positional arguments:
  project_path          Path to the project to create.

optional arguments:
  -h, --help            show this help message and exit
  --python PYTHON       Path to Python interpreter to use. Defaults to 'python3'.
  --overwrite           Overwrite existing project at specified directory.
  --requirements REQUIREMENTS
                        Comma-separated list of requirements to install.
                        
```

## Planned enhancements

- A `--docker` flag to create a `Dockerfile`, plus `build.sh` and `push.sh` executable bash scripts
- Better support for creating virtualenvs in a default location (instead of the project directory)
- creating a main.py and test directory

More to come.