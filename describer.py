import click
import git

SKIP_FILES = ["__init__.py", "__pycache__"]


@click.command()
@click.option("--path", prompt="Workspace path", help="Path to the workspace")
@click.option("--branch", prompt="Branch name", help="Branch name")
def main(path: str = "", branch: str = "") -> None:
    """Django Migrations Describer"""
    repo = git.Repo(path)

    current = repo.commit(branch)
    past = repo.commit("master")
    for index in past.diff(current).iter_change_type("A"):
        if "migrations" in index.b_path:
            click.secho(index.b_path)


if __name__ == "__main__":
    main()
