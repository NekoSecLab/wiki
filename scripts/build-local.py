import mkdocs.utils
import os
import pathlib
import typer

app = typer.Typer()
root_docs_path = pathlib.Path("docs")
root_build_path = pathlib.Path("build")

@app.command()
def get_docs_paths():
    typer.echo("Getting docs to be built...", color=typer.colors.BLUE)
    doc_paths = [
        doc_path.absolute() for doc_path in root_docs_path.iterdir()
    ]
    return doc_paths

@app.command()
def build_one_doc(doc_path: pathlib.Path):
    typer.echo(f"Building doc: {doc_path}", color=typer.colors.BLUE)
    if not doc_path.exists():
        raise FileNotFoundError(f'''Doc path "{doc_path}" not existed!''')
    if not doc_path.is_dir():
        raise NotADirectoryError(f'''Doc path "{doc_path}" is not a directory!''')

    doc_config_path = doc_path / "mkdocs.yml"
    doc_config = mkdocs.utils.yaml_load(doc_config_path.read_text(encoding="utf-8"))

    doc_build_path = root_build_path / doc_path.name
    doc_build_path.mkdir()

@app.command()
def build():
    if os.path.exists(root_build_path):
        clean()
    os.mkdir(root_build_path)

    cwd = os.getcwd()
    doc_paths = get_docs_paths()
    if len(doc_paths) == 0:
        raise Error("No docs to be built!")

    for doc_path in doc_paths:
        build_one_doc(doc_path) 

@app.command()
def clean():
    typer.echo("Cleaning build caches...", color=typer.colors.BLUE)
    os.rmdir(root_build_path)

if __name__ == '__main__':
    app()
