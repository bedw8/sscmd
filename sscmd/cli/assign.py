import typer
from typing import Optional
from pathlib import Path
from rich import print 
from rich_tools import df_to_table
import pandas as pd
from .utils import check_path_to_write
from .options import OutputFileOption, ForceOverwriteOption
from ..assignments import AssignmentsApi

app = typer.Typer()

@app.callback()
def main():
    '''Maneja las asignaciones'''
    pass
 
@app.command()
def get_list(ctx: typer.Context, 
        file: Path = OutputFileOption('la lista de asignaciones',...),
        force: Optional[bool] = ForceOverwriteOption(),
        questionnaire_id: Optional[str] = typer.Option(None,'--id',help='Identificador del cuestionario'),
        questionnaire_version: Optional[int] = typer.Option(None,'--version',help='Versión del cuestionario')
        ):
    '''Obtiene la liste de las asignaciones'''
    check_path_to_write(file,force) 

    api = AssignmentsApi(ctx.parent.parent.client)
    quests = list(api.get_list(questionnaire_id,questionnaire_version))
    df = pd.DataFrame(quests)
    df = df

    if not file:
        print(df_to_table(df))
    else:
        df.to_csv(file,index=False)
        print('Se escribío el archivo',file)

if __name__ == "__main__":
    app.run()
