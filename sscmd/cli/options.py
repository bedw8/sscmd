from pathlib import Path
import typer

def OutputFileOption(content='la información',default=None) -> Path:
    help_ = 'Guarda '+content+' en la ruta indicada'  
    help_ = ' '.join(help_.split())
    return typer.Option(default,'--out','-o',help=help_,show_default=False)

def OutputFileArg(content='la información',default=None) -> Path:
    help_ = 'Guarda '+content+' en la ruta indicada'  
    help_ = ' '.join(help_.split())
    return typer.Argument(default,metavar='PATH',help=help_,show_default=False)

def ForceOverwriteOption(content=''):
    help_ = 'Sobrescribe el archivo '+content+' si ya existe'
    help_ = ' '.join(help_.split())
    return typer.Option(False,'--force','-f', help=help_.strip(),show_default=False)

def ReqArg(default,**kwargs):
    return typer.Argument(default,show_default=False)
