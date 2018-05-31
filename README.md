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
python describer.py --path=<path> --branch==<branch name>
```

## TODO:
* auto update repository
* parse files
 * table added
 * table deleted
 * field added
 * field modified
 * index added
 * index removed
 * data migration (allow user put comment or read doc from function)
