#!/usr/bin/env python3

"""
mkprj is a tool to help create a new Python project, setting up all the boilerplate stuff, like:

* initializing git
* creating a .gitignore
* creating a virtualenv
* creating a requirements.txt


...and more.

"""

__version__ = (0, 1, 0)


import sys
import shutil
import logging
import argparse
import subprocess
import typing

from pathlib import Path


logging.basicConfig(level=logging.INFO, format='(mkprj) %(message)s')


DEFAULT_GITIGNORE_FILES = ['__pycache__', '.idea/', 'venv/']
DEFAULT_REQUIREMENTS = 'pytest'


def exit_with_message(message, exit_code=1):
    logging.error(message)
    sys.exit(exit_code)


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('--python', default='python3', help="Path to Python interpreter to use. Defaults to 'python3'.")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite existing project at specified directory.")
    parser.add_argument('--requirements', default=DEFAULT_REQUIREMENTS, help="Comma-separated list of requirements to install.")
    parser.add_argument('project_path', help='Path to the project to create.')

    return parser


def parse_arguments(args: typing.List[str]) -> argparse.Namespace:
    parser = get_argument_parser()

    args, remainder = parser.parse_known_args(args)

    if remainder:
        exit_with_message("Found unknown args: {}".format(remainder))
        parser.print_help()

    return args


def make_project_directory(project_path: Path, overwrite=False):
    if project_path.exists():
        if not overwrite:
            exit_with_message("Project directory already exists.")

        logging.info("Overwriting existing project.")
        shutil.rmtree(str(project_path))

    project_path.mkdir()


def create_gitignore(project_path: Path, files_to_ignore: typing.List[str]):
    gitignore_file = project_path / '.gitignore'
    with gitignore_file.open('w') as f:
        f.write('\n'.join(files_to_ignore))


def git_init(project_path: Path):
    proc = subprocess.run(['git', 'init'], cwd=project_path)
    proc.check_returncode()


def create_virtualenv(project_path: Path, which_python: str):
    project_name = project_path.stem
    proc = subprocess.run([which_python, '-m', 'venv', project_path / project_name])
    proc.check_returncode()


def create_requirements(project_path: Path, requirements: str=None):
    reqs_file = project_path / 'requirements.txt'
    if requirements:
        with reqs_file.open('w') as f:
            f.write('\n'.join(requirements.split(',')))
    else:
        reqs_file.touch()


def install_requirements(project_path: Path):
    reqs_file = project_path / 'requirements.txt'
    venv_path = (project_path / project_path.stem) / 'bin/python'
    proc = subprocess.run([venv_path, '-m', 'pip', 'install', '-r', reqs_file])
    proc.check_returncode()


def main():
    args = parse_arguments(sys.argv[1:])
    project_path = Path(args.project_path).absolute()

    logging.info("Creating a new project at {}".format(project_path))
    make_project_directory(project_path, args.overwrite)

    logging.info("Initializing git")
    git_init(project_path)

    logging.info("Creating gitignore")
    create_gitignore(project_path, DEFAULT_GITIGNORE_FILES)

    logging.info("Creating virtualenv")
    create_virtualenv(project_path, args.python)

    logging.info("Creating requirements file")
    create_requirements(project_path, args.requirements)

    logging.info("Installing requirements")
    install_requirements(project_path)


if __name__ == '__main__':
    main()
