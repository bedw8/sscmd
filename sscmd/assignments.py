from typing import Optional, Union
from .baseapi import BaseApi


class AssignmentsApi(BaseApi):
    """ Set of functions to access and manipulate Assignments. """
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id: Optional[str] = None,
                 questionnaire_version: Optional[int] = None):
        """Obtiene una lista de las asignaciones

        Si no se entrega ID de cuestionario ni version, se obtendran las asignaciones de todos los cuestionarios disponibles en el workspace. Para identificar el ID y versión de un cuestionario usar `sscmd [-w workspace] quest list`  
        """
        path = self.url
        limit = 20
        offset = 1
        total_count = 21
        params = {
            'offset': offset,
            'limit': limit,
            'questionnaireId': None,
        }
        if questionnaire_id and questionnaire_version:
            params['questionnaireId'] = '{}${}'.format(questionnaire_id, questionnaire_version)

        while offset < total_count:
            params['offset'] = offset
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            offset += limit
            yield from r['Assignments']

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
