import typer
from typing import Optional
from pathlib import Path
from rich import print 
from rich.prompt import Confirm
from rich_tools import df_to_table
import pandas as pd
from .utils import check_path_to_write
from .options import OutputFileOption, ForceOverwriteOption
from ..questionnaires import QuestionnairesApi

app = typer.Typer()

@app.callback()
def main():
    '''Maneja los cuestionarios'''
    pass
 
@app.command()
def get_list(ctx: typer.Context, 
        file: Optional[Path] = OutputFileOption('la lista de cuestionarios'),
        force: Optional[bool] = ForceOverwriteOption()
        ):
    '''Obtiene la lista de cuestionarios'''
    check_path_to_write(file,force) 

    qapi = QuestionnairesApi(ctx.parent.parent.client)
    quests = list(qapi.get_list())
    q_df = pd.DataFrame(quests).drop(['LastEntryDate','IsAudioRecordingEnabled','WebModeEnabled'],axis=1)
    q_df = q_df.sort_values(['Title','Version'])


    if not file:
        print(df_to_table(q_df))
    else:
        q_df.to_csv(file,index=False)
        print('Se escribío el archivo',file)

if __name__ == "__main__":
    app.run()
