# Notes on `uv`
<!-- TODO: write bash script to initialize `uv` project-->
`uv` is a virtual environment, dependency manager, and version manager for `python` projects.

## Installation

I installed it using 

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

which can be verified with 

```bash
uv --version
```

and be updated with

```bash
uv self update
```

## Setup

The list of installed python versions can be shown with

```bash
uv python list
```

and new ones installed with

```bash
uv python install 3.13
```

One of the convenient functions of uv is to transmit to other developers the exact version of python they need to use to run the project in a predictable manner.
When in the project directory, it suffices to do 

```bash
uv python pin 3.13.3
```

to fix that version to the project.
Henceforth, when the project is resumed elsewhere one needs only to execute

```bash
uv sync
```

or

```bash
uv run
```

to use the exact same python version and install it if necessary.

## Initialize project

To initialize a python development project run

```bash
uv init my-project
```

### `pyproject.toml`

Contains metadata about the project.
This file is used to specify dependencies, as well as details about the project such as its description or license.
It can be edited manually, or with commands like `uv add` and `uv remove` to manage your project from the terminal.
Details about the `pyproject.toml` file can be found in [https://packaging.python.org/en/latest/guides/writing-pyproject-toml/](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).

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

```bash
uv run main.py
```

## Update

Update project dependencies with

```bash
uv sync
```

and update lock file with

```bash
uv lock
```

## Managing dependencies

You can add dependencies to your `pyproject.toml` with the `uv add` command. 
This will also update the lockfile and project environment:

```bash
uv add requests
```

You can also specify version constraints or alternative sources:

```bash
# Specify a version constraint
uv add 'requests==2.31.0'
# Add a git dependency
uv add git+https://github.com/psf/requests
```

If you're migrating from a `requirements.txt` file, you can use `uv add` with the `-r` flag to add all dependencies from the file:

```bash
uv pip install -r requirements.txt
```

or

```bash
# Add all dependencies from `requirements.txt`.
uv add -r requirements.txt -c constraints.txt
```

To remove a package, you can use `uv remove`:

```bash
uv remove requests
```

To upgrade a package, run `uv lock` with the `--upgrade-package` flag:

```bash
uv lock --upgrade-package requests
```

The `--upgrade-package` flag will attempt to update the specified package to the latest compatible version, while keeping the rest of the lockfile intact.

To generate a requirements.txt from a UV lock file, use the following command:

```bash
uv export -o requirements.txt
```

### Development or produciton dependencies

Dependencies can be marked as for development using 

```bash
uv add --dev dependency
```

and only-production dependencies may be installed using

```bash
uv sync --no-dev --locked
```

Details at: [blog.pecar.me/uv-with-django](https://blog.pecar.me/uv-with-django)

## References

- [blog.stephane-robert.info/docs/developper/programmation/python/uv/](https://blog.stephane-robert.info/docs/developper/programmation/python/uv/)
- [docs.astral.sh/uv/guides/projects/#project-structure](https://docs.astral.sh/uv/guides/projects/#project-structure)
- [datacamp.com/tutorial/python-uv](https://www.datacamp.com/tutorial/python-uv)
- [realpython.com/python-uv/](https://realpython.com/python-uv/)
 [github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- [packaging.python.org/en/latest/guides/writing-pyproject-toml/](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [blog.pecar.me/uv-with-django](https://blog.pecar.me/uv-with-django)
