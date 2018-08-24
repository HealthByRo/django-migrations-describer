# django-migrations-describer

## Instalation

Run:
```
PIPENV_VENV_IN_PROJECT=1 pipenv install --three --dev
PIPENV_VENV_IN_PROJECT=1 pipenv shell
```

## Usage
1. Update destination repository (eg. release branch)
2. Run:
```
python describer.py --path=<path> --branch=<branch name>
```

## Optional parameters
* `--venv` - Path to project virtual env
* `--ignore` - Comma separated list of up to migrations to ignore
* `--branch` - Branch name to compare
* `--base-branch` - Base branch name to compare

## TODO:
 * index added
 * index removed
 * check module if custom table is set
 * add setup.py and release on PyPi
