import typer

def OutputFileOption(content='la información',default=None):
    help_ = 'Guarda '+content+' en el archivo indicado'  
    help_ = ' '.join(help_.split())
    return typer.Option(default,'--out','-o',help=help_)

def ForceOverwriteOption(content=''):
    help_ = 'Sobrescribe el archivo '+content+' si ya existe'
    help_ = ' '.join(help_.split())
    return typer.Option(False,'--force','-f', help=help_.strip())


