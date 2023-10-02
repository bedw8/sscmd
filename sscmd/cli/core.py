from typing import Optional, List
import configparser
import json
import typer
from pathlib import Path
from .options import ForceOverwriteOption
from .utils import check_config_exists, create_default_config
from . import assign, quest, directories
from ..apis.client import Client

app = typer.Typer(no_args_is_help=True,
                  context_settings={"allow_extra_args": True,
                                    "ignore_unknown_options": True,
                                    "help_option_names":['-h','--help']
                                    })

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__appname__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
        ctx: typer.Context,
        server_url: Optional[str] = typer.Option(
            None,
            '--url',
            '-u',
            help='URL del servidor'),
        workspace: Optional[str] = typer.Option(
            None,
            '--workspace',
            '-w',
            help='Especifica el workspace'),
        config_path: Optional[Path] = typer.Option(
            Path('project.conf'),
            '--config',
            '-c',
            help='Especifica archivo de configuración'
            ),
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Muestra la version de la aplicación",
            callback=_version_callback,
            is_eager=True)
        ) -> None:
    
    args = locals()

    if ctx.invoked_subcommand not in ['setup']:
        try:
            ctx.client = Client(config_path,workspace=workspace)
        except Exception as e:
            print(e)
    return

app.add_typer(quest.app, name='quest')
app.add_typer(assign.app, name='assign')

@app.command()
def setup(ctx: typer.Context, path: Path,
        versions: Optional[List[str]] =  typer.Option(None,help='Versiones de un cuestionario'),
        config_bool: Optional[bool] = typer.Option(True,'--no-config','-C', help='No crea el archivo de configuración de ejemplo'),
        force: Optional[bool] = ForceOverwriteOption('de configuración')
        ):
    '''Configura una carpeta para un nuevo proyecto'''
    directories.setup_directory(path) 
    if config_bool:
        create_default_config(ctx, path, force) 


