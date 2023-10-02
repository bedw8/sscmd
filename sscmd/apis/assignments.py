from pathlib import Path
from typing import Optional, Union, Tuple
from .baseapi import BaseApi
import pandas as pd


class AssignmentsApi(BaseApi):
    """ Set of functions to access and manipulate Assignments. """
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id: Optional[str] = None,
                 questionnaire_version: Optional[int] = None,
                 id_range: Optional[Tuple[int]] = None,
                 order: Optional[str] = None,
                 query: Optional[str] = None,
                 folios: Optional[bool] = None):
        """Obtiene una lista de las asignaciones

        Si no se entrega ID de cuestionario ni version, se obtendran las asignaciones de todos los cuestionarios disponibles en el workspace. Para identificar el ID y versión de un cuestionario usar `sscmd [-w workspace] quest list`  
        """
        path = self.url
        limit = 20
        offset = 0
        total_count = 21
        params = {
            'offset': offset,
            'limit': limit,
            'questionnaireId': None,
        }
        if not questionnaire_id:
            questionnaire_id = self._client.config['general']['q_id']
    
        if not questionnaire_version:
            questionnaire_version = self._client.config['general']['q_version']
        
        if questionnaire_id and questionnaire_version:
            params['questionnaireId'] = '{}${}'.format(questionnaire_id, questionnaire_version)        

        if query:
            params['searchBy'] = query

        if order:
            params['order'] = order

        if id_range:
            params['order'] = 'Id'

        while offset < total_count:
            params['offset'] = offset
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            offset += limit
            for assign in r['Assignments']:
                if not id_range:
                    if folios:
                        assign['Folio'] = self._get_folio(assign['Id'])
                    yield assign
                else:
                    if (assign['Id'] >= id_range[0] and assign['Id'] <= id_range[1]):
                        if folios:
                            assign['Folio'] = self._get_folio(assign['Id'])
                        yield assign
                    if assign['Id'] > id_range[1]:
                        offset = total_count


    def write_list(self,
                 out: Path,
                 add_folios: Optional[Path] = None,
                 progress: Optional[bool] = None,
                 **kwargs
                ):
        """Obtiene y escribe una lista de las asignaciones

        out: Path,
                 add_folios: Optional[Path] = None,
                 progress: Optional[bool] = None,
        """
    
        assigns = []
        list_generator = self.get_list(**kwargs)
        i=0
        for a in list_generator:
            if progress:
                print(i,end='\r')
                i+=1
            assigns.append(a)
            
        df = pd.DataFrame(assigns)
        df = df
    
        if add_folios:
            folios_df = pd.read_csv(add_folios)
            df = df.merge(folios_df,on='Id',how='left')
            print('Se añadieron folios')
    
        df.to_csv(out,index=False)
        print('Se escribío el archivo',out)


    def _get_folio(self,_id):
        details = self.get_id_details(_id)
        return details['Answers'][0]['Answer']['Value']

    def get_id_details(self, assign_id:int):
        """Entrega el detalle de una asignación"""
        path = f'{self.url}/{assign_id}'
        r = self._make_call('get',path)
        return r


    def set_responsible(self, assign_id: int, responsible: str):
        """Cambia el responsable de una asignacion"""
        path = f'{self.url}/{assign_id}/assign'
        params = {'Responsible': responsible}

        r = self._make_call('patch', path, json=params)
        return r
