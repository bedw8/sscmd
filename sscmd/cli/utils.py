from typing import Optional
import typer
from pathlib import Path
import toml

def check_path_to_write(file: Optional[Path], force: Optional[bool]):
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
    
    config = {}

    config['credentials'] = {'api_user':'usuario','api_password':'contraseña'}
    config['general']  = {'url':'https://...','workspace':'primary'}

    configFile = open(configPath,'w')
    #config.write(configFile)
    toml.dump(config,configFile)


def docs_from(original):
	def wrapper(target):
		target.__doc__ = original.__doc__.splitlines()[0]
		return target
	return wrapper

