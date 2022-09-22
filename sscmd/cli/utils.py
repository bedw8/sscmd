import typer
from pathlib import Path
from configparser import ConfigParser

def check_path_to_write(file, force):
    if file:
        if file.is_dir():
            print('la ruta ingresada corresponde a un directorio')
            raise typer.Abort()
        
        if not force:
            if file.is_file():
                confirm = typer.confirm('El archivo ya existe. Desea sobrescribirlo?',abort=True)


def check_config_exists(config_path: Path):
    if not config_path.is_file():
        print('No existe el archivo de configuración. Cree uno o indíquelo con la opcion -c')
        raise typer.Abort()


def create_default_config(ctx: typer.Context, path: Path,force):
    configPath = Path(path,'project.conf')
    check_path_to_write(configPath,force)
    
    config = ctx.parent.config

    config.add_section('credentials')
    config.add_section('general')
    config.set('credentials','user','usuario')
    config.set('credentials','passwd','contraseña')
    config.set('general','url','https://...')

    configFile = open(configPath,'w')
    config.write(configFile)

