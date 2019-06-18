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
python describer.py --path=<path to project> --start-ref=<git ref>
```

## Parameters
* `--path` - Path to project
* `--start-ref` - Git ref (e.g. commit or tag) that we start the diff from
* `--end-ref` - Git ref (e.g. commit or tag) that we end the diff at, defaults to `master`
* `--venv` - Path to project's virtual env
* `--ignore` - Comma separated list of up to migrations to ignore

## TODO:
 * index added
 * index removed
 * check module if custom table is set
 * add setup.py and release on PyPi
