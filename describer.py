import importlib.util
import os
import sys

import click

import git
from django.conf import settings
from django.db import migrations, models

SKIP_FILES = ["__init__.py", "__pycache__"]


def get_table_name(path: str, model: str):
    # TODO: check module if custom table
    module = path.split("/")[1]
    return "_".join([module, model]).lower()


@click.command()
@click.option("--path", prompt="Workspace path", help="Path to the workspace")
@click.option("--branch", prompt="Branch name", help="Branch name")
@click.option(
    "--venv", prompt="Project virtual env", help="Path to project virtual env"
)
@click.option("--ignore", help="Comma separated list of up to migrations to ignore")
def main(path: str = "", branch: str = "", venv: str = "", ignore: str = "") -> None:
    """Django Migrations Describer"""
    sys.path.append(path)
    sys.path.append(venv)

    ignores = {}
    if ignore:
        for i in ignore.split(","):
            i = i.split(".")
            ignores[i[0]] = int(i[1].split("_")[0]), i[1]

    print("i", ignores)

    repo = git.Repo(path)
    repo.remotes["origin"].fetch()

    current = repo.commit("origin/" + branch)
    past = repo.commit("origin/master")
    settings.configure()
    description = []
    for index in past.diff(current).iter_change_type("A"):
        if "migrations" in index.b_path:
            if "__init__.py" in index.b_path:
                continue

            migration_path = os.path.join(path, index.b_path)
            module_name, _, migration_name = index.b_path[:-3].split("/")[:3]
            if ignores.get(module_name):
                migration_no = int(migration_name.split("_")[0])
                if (
                    ignores[module_name][0] > migration_no
                    or ignores[module_name][1] == migration_name
                ):
                    continue
            spec = importlib.util.spec_from_file_location("Migration", migration_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            klass = mod.Migration
            for operation in klass.operations:
                if isinstance(operation, migrations.AddField):
                    table_name = get_table_name(index.b_path, operation.model_name)
                    field = operation.name
                    if isinstance(operation.field, models.fields.related.ForeignKey):
                        field += "_id"
                    elif isinstance(operation.field, models.ManyToManyField):
                        table_name = get_table_name(
                            index.b_path,
                            "_".join([operation.model_name, operation.name]),
                        )
                        description.append(f"Added table `{table_name}`")
                        continue
                    description.append(f"Added field `{field}` to table `{table_name}`")
                elif isinstance(operation, migrations.CreateModel):
                    table_name = get_table_name(index.b_path, operation.name)
                    description.append(f"Added table `{table_name}`")
                elif isinstance(operation, migrations.AlterField):
                    table_name = get_table_name(index.b_path, operation.model_name)
                    description.append(f"Updated field `{table_name}.{operation.name}`")
                elif isinstance(operation, migrations.RenameField):
                    table_name = get_table_name(index.b_path, operation.model_name)
                    description.append(
                        f"Renamed field `{table_name}.{operation.old_name}` to `{table_name}.{operation.new_name}`"
                    )
                elif isinstance(operation, migrations.DeleteModel):
                    table_name = get_table_name(index.b_path, operation.name)
                    description.append(f"Deleted table `{table_name}`")
                elif isinstance(operation, migrations.RunPython):
                    if not operation.code.__doc__:
                        raise Exception(
                            f"Missing migration description in {migration_path}"
                        )
                    description.append(
                        f"Data Migration: " + operation.code.__doc__.strip()
                    )
                elif isinstance(operation, migrations.AlterUniqueTogether):
                    table_name = get_table_name(index.b_path, operation.name)
                    for fields in operation.unique_together:
                        fields = ", ".join(fields)
                        description.append(
                            f"Added or updated Index for fields `{fields}` on table `{table_name}`"
                        )
                else:
                    with open(os.path.join(path, index.b_path)) as f_obj:
                        # click.echo(operation)

                        click.echo(index.b_path)
                        click.echo(f_obj.read())
                        description.append(
                            click.prompt(
                                "Operation not supported yet. ",
                                "Please read the above file content and describe the change",
                            )
                        )

    if description:
        click.echo("\n".join(description))


if __name__ == "__main__":
    main()
