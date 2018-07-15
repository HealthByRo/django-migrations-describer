# django-migrations-describer

## Instalation

Run:
```
PIPENV_VENV_IN_PROJECT=1 pipenv install --three --dev
PIPENV_VENV_IN_PROJECT=1 pipenv shell
```

## Usage
1. Update destination repository (master and release branch)
2. Run:
```
python describer.py --path=<path> --branch=<branch name>
```

## TODO:
 * table renamed
 * index added
 * index removed
 * data migration (print and allow user put comment or read doc from function)
 * check module if custom table is set
