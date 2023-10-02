
from typing import Optional, List
from .baseapi import BaseApi
import pandas as pd

class QuestionnairesApi(BaseApi):
    """Functions to access information on Questionnaires. """

    _apiprefix = "/api/v1/questionnaires"

    def get_list(self, title: Optional[str] = None, questionnaire_id: Optional[str] = None,
                 version: Optional[int] = None):
        #if not fields:
        #    fields = [
        #        "id",
        #        "questionnaire_id",
        #        "version",
        #        "title",
        #        "variable",
        #    ]
        # we always have workspace parameter
        q_args = {
            "workspace": self.workspace
        }
        if questionnaire_id:
            q_args["id"] = questionnaire_id
        if version:
            q_args["version"] = version
        if title:
            q_args["title"] = title
        
        req = self._make_call('get', self.url,params=q_args)

        for q in req['Questionnaires']:
            yield q

