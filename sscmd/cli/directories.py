##################################
# Función para fijar directorios #
##################################
import os
from pathlib import Path
from typing import Optional, List

def setup_directory(path,q_versions: Optional[List[str]] = None):
    """Crea la estructura de directorios para un projecto"""
     
    Path(path,'data','asignaciones').mkdir(parents=True,exist_ok=True) 
    Path(path,'data','equipo').mkdir(parents=True,exist_ok=True) 
    Path(path,'data','respaldo').mkdir(parents=True,exist_ok=True) 
    Path(path,'Reportes').mkdir(parents=True,exist_ok=True) 

    if q_versions:
        for version in q_versions:
            Path('data','paradata_v'+version).mkdir(parents=True,exist_ok=True) 
            Path('data','SurveySolutions_v'+version).mkdir(parents=True,exist_ok=True) 
