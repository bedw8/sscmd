import typer
import types
from typing import Optional
from pathlib import Path
from rich import print 
from rich_tools import df_to_table
import pandas as pd
from .utils import check_path_to_write, check_config_exists, docs_from
from .options import OutputFileOption, OutputFileArg, ForceOverwriteOption, ReqArg
from ..assignments import AssignmentsApi
from copy import deepcopy
from ast import literal_eval as le
from rich.progress import track

app = typer.Typer()

@app.callback()
def main(ctx: typer.Context):
    '''Maneja las asignaciones'''
    config_path = Path(ctx.parent.params['config_path'])
    check_config_exists(config_path) # Checks the config file exists

 

@app.command("list")
@docs_from(AssignmentsApi.get_list)
def get_list(ctx: typer.Context, 
        file: Path = OutputFileArg('la lista de asignaciones',...),
        force: Optional[bool] = ForceOverwriteOption(),
        questionnaire_id: Optional[str] = typer.Option(None,'--id','-q',help='Identificador del cuestionario',show_default=False),
        questionnaire_version: Optional[int] = typer.Option(None,'--version','-v',help='Versión del cuestionario',show_default=False),
        order: Optional[str] = typer.Option(None,'--sort','-s',help='Variable según la cual ordenar los resultados',show_default=False),
        id_range: Optional[str] = typer.Option(None,'--range','-r',help="Especifica el rango de Ids",show_default=False), 
        query: Optional[str] = typer.Option(None,'--query',help='Query de busqueda',show_default=False),
        folios: Optional[bool] = typer.Option(False,'--folios',help='Consultar folios las solicitudes (más lento)'),
        add_folios: Optional[Path] = typer.Option(None,'--folios-df',help='Añadar folios (merge) previamente obtenidos',show_default=False)
        ):
    check_path_to_write(file,force) 
    
    api_params = {key: ctx.params[key] for key in ctx.params if key not in ['file','force','folios','add_folios']}

    if id_range:
        api_params['id_range'] = le(api_params['id_range'])
    
    if not questionnaire_id:
        api_params['questionnaire_id'] = ctx.parent.parent.config['general']['q_id']
    
    if not questionnaire_version:
        api_params['questionnaire_version'] = ctx.parent.parent.config['general']['q_version']

    total = (api_params['id_range'][1] - api_params['id_range'][0])

    assigns = []
    api = AssignmentsApi(ctx.parent.parent.client)
    list_generator = api.get_list(**api_params)
    progress = track(list_generator,total=total) if id_range else list_generator  
    for a in progress:
        assigns.append(a)
    df = pd.DataFrame(assigns)
    df = df

    if add_folios:
        folios_df = pd.read_csv(add_folios)
        df = df.merge(folios_df,on='Id',how='left')
        print('Se añadieron folios')

    df.to_csv(file,index=False)
    print('Se escribío el archivo',file)


@app.command('details')
@docs_from(AssignmentsApi.get_id_details)
def get_id_details(ctx: typer.Context,
                   assign_id: int = ReqArg(...,metavar='ID', help='Id de la asignación')
	):

    api = AssignmentsApi(ctx.parent.parent.client)
    r = api.get_id_details(**ctx.params)
    print(r)


@app.command()
@docs_from(AssignmentsApi.set_responsible)
def set_responsible(ctx: typer.Context,
                    assign_id: int = ReqArg(...,metavar='ID',help = 'Id de la asignación'),
                    responsible: str = ReqArg(...,metavar='RESPONSABLE', help='Nombre del nuevo responsable')
	):
     
    api = AssignmentsApi(ctx.parent.parent.client)
    r = api.set_responsible(**ctx.params)
    print(r)

if __name__ == "__main__":
    app.run()
