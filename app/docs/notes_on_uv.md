# uv
`uv` is a virtual environment, dependency manager, and version manager for `python` projects.

## Installation
I installed it using 
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
which can be verified with 
```
uv --version
```
and be updated with
```
uv self update
```
## Setup
The list of installed python versions can be shown with
```
uv python list
```
and new ones installed with
```
uv python install 3.14
```
One of the convenient functions of uv is to transmit to other developers the exact version of python they need to use to run the project in a predictable manner.
When in the project directory, it suffices to do 
```
uv python pin 3.13
```
to fix that version to the project.
Henceforth, when the project is resumed elsewhere one needs only to execute
```
uv sync
```
or
```
uv run
```
to use the exact same python version and install it if necessary.
## Initialize project
To initialize a python development project run
```
uv init my-project
```
### `pyproject.toml`
Contains metadata about the project.
This file is used to specify dependencies, as well as details about the project such as its description or license.
It can be edited manually, or with commands like `uv add` and `uv remove` to manage your project from the terminal.
### `.python.version`
The `.python-version` file contains the project's default Python version. This file tells uv which Python version to use when creating the project's virtual environment.
### `.venv`
The `.venv` folder contains your project's virtual environment, a Python environment that is isolated from the rest of your system. This is where uv will install your project's dependencies.
### `uv.lock`
`uv.lock` is a cross-platform lockfile that contains exact information about your project's dependencies.
Unlike the `pyproject.toml` which is used to specify the broad requirements of your project, the lockfile contains the exact resolved versions that are installed in the project environment.
This file should be checked into version control, allowing for consistent and reproducible installations across machines.

uv.lock is a human-readable TOML file but is managed by uv and should not be edited manually.
## Run project
The `pyproject.toml`file describes the project and its dependencies.
To create its corresponding virtual environment and run the project in it we execute:
```
uv run main.py
```
## Update
Update project dependencies with
```
uv sync
```
and update lock file with
```
uv lock
```
## Managing dependencies
You can add dependencies to your `pyproject.toml` with the `uv add` command. 
This will also update the lockfile and project environment:
```
uv add requests
```
You can also specify version constraints or alternative sources:

```
# Specify a version constraint
uv add 'requests==2.31.0'
# Add a git dependency
uv add git+https://github.com/psf/requests
```
If you're migrating from a `requirements.txt` file, you can use `uv add` with the `-r` flag to add all dependencies from the file:

```
uv pip install -r requirements.txt
```
or 
```
# Add all dependencies from `requirements.txt`.
uv add -r requirements.txt -c constraints.txt
```
To remove a package, you can use `uv remove`:
```
uv remove requests
```
To upgrade a package, run `uv lock` with the `--upgrade-package` flag:
```
uv lock --upgrade-package requests
```
The `--upgrade-package` flag will attempt to update the specified package to the latest compatible version, while keeping the rest of the lockfile intact.

To generate a requirements.txt from a UV lock file, use the following command:
```
uv export -o requirements.txt
```
## References
[https://blog.stephane-robert.info/docs/developper/programmation/python/uv/](https://blog.stephane-robert.info/docs/developper/programmation/python/uv/)
[https://docs.astral.sh/uv/guides/projects/#project-structure](https://docs.astral.sh/uv/guides/projects/#project-structure)
[https://www.datacamp.com/tutorial/python-uv](https://www.datacamp.com/tutorial/python-uv)
[https://realpython.com/python-uv/](https://realpython.com/python-uv/)
[https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
