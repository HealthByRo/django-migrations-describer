import importlib.util
import os

import click
import git
from django.conf import settings
from django.db import migrations, models

SKIP_FILES = ["__init__.py", "__pycache__"]


def get_table_name(path: str, model: str):
    # TODO: check module if custom table
    module = path.split("/")[1]
    return "__".join([module, model]).lower()


@click.command()
@click.option("--path", prompt="Workspace path", help="Path to the workspace")
@click.option("--branch", prompt="Branch name", help="Branch name")
def main(path: str = "", branch: str = "") -> None:
    """Django Migrations Describer"""
    repo = git.Repo(path)
    repo.remotes["origin"].fetch()

    current = repo.commit("origin/" + branch)
    past = repo.commit("origin/master")
    settings.configure()
    description = []
    for index in past.diff(current).iter_change_type("A"):
        if "migrations" in index.b_path:
            spec = importlib.util.spec_from_file_location(
                "Migration", os.path.join(path, index.b_path)
            )
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
