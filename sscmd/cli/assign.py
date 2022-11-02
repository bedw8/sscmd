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
        questionnaire_id: Optional[str] = typer.Option(None,'--id',help='Identificador del cuestionario',show_default=False),
        questionnaire_version: Optional[int] = typer.Option(None,'--version',help='Versión del cuestionario',show_default=False),
        order: Optional[str] = typer.Option(None,'--order',help='Variable según la cual ordenar los resultados'),
        id_range: Optional[str] = typer.Option(None,'--range',help="Especifica el rango de Ids"), 
        query: Optional[str] = typer.Option(None,'--query',help='Query de busqueda',show_default=False),
        folios: Optional[bool] = typer.Option(False,'--folio',help='Incluir folios (más lento)')
        ):
    check_path_to_write(file,force) 
    
    api_params = {key: ctx.params[key] for key in ctx.params if key not in ['file','force']}

    if in_range:
        api_params['in_range'] = le(api_params['in_range'])
    
    api = AssignmentsApi(ctx.parent.parent.client)
    assigns = list(api.get_list(**api_params))
    df = pd.DataFrame(assigns)
    df = df

    if not file:
        print(df_to_table(df))
    else:
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
