from typing import Optional, Union
from .baseapi import BaseApi


class AssignmentsApi(BaseApi):
    """ Set of functions to access and manipulate Assignments. """
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id: Optional[str] = None,
                 questionnaire_version: Optional[int] = None):
        """Get list of assignments
        :param questionnaire_id: Filter by specific questionnaire id
        :param questionnaire_version: Filter by specific version number
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
