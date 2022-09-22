import time
import pytz
from typing import Optional, Union, Literal 

from .baseapi import BaseApi

class ExportApi(BaseApi):
    
    EXPORT_STATUS = Literal['Created', 'Running', 'Completed', 'Fail', 'Canceled']
    EXPORT_TYPE = Literal['Tabular', 'STATA', 'SPSS', 'Binary', 'DDI','Paradata']
    INTERVIEW_STATUS = Literal['All', 'SupervisorAssigned', 'InterviewerAssigned',\
        'Completed','RejectedBySupervisor', 'ApprovedBySupervisor', 'RejectedByHeadquarters',\
        'ApprovedByHeadquarters']

    _apiprefix: str = "/api/v2/export"

    def get_list(self,
                 questionnaire_identity: Optional[str] = None,
                 export_type: Optional[EXPORT_TYPE] = None,
        #         interview_status: Optional[INTERVIEW_STATUS] = None,
                 export_status: Optional[EXPORT_STATUS] = None,
                 has_file: Optional[bool] = None):
        """
        Get list of all previosly executed export jobs
        :param questionnaire_identity: Questionnaire and version
        :param export_type: Format of the export data
        :param export_status: Status of the export job
        :param has_file: Whether the job has export file to download
        """

        path = self.url
        params = {
            "exportType": export_type,
            "interviewStatus": interview_status,
            "questionnaireIdentity": questionnaire_identity,
            "exportStatus": export_status,
            "hasFile": has_file,
        }
        r = self._make_call('get', path, params=params)
        if r:
            for item in r:
                yield item


    def start(self, export_type: EXPORT_TYPE, q_id:str, from_: Optional[str] = None, to: Optional[str] = None, wait: bool = True, show_progress: bool = True):
        """Start new export job
        :param export_type
        :returns: request response
        """
        path = self.url
        
        data={
              "ExportType": export_type,
              "QuestionnaireId":q_id,
              "InterviewStatus": "All",
              "From": from_,
              "To": to,
              "AccessToken": None,
              "RefreshToken": None,
              "StorageType": None,
              "TranslationId": None,
              "IncludeMeta": True
            }

        export = self._make_call("post", path, json=data)

        if wait:
            export = self.get_info(export['JobId'])
            progress = 0
            status = None           

            if show_progress:
                print("Generando exportacion de " + str(export_type) + "...")

            while export['ExportStatus'] != "Completed":
                time.sleep(1)
                if show_progress:
                    #print(".", end="", flush=True)
                    print(str(progress)+"%", end=" ", flush=True)
                export = self.get_info(export['JobId'])
                progress = export['Progress']

            if show_progress:
                print('100%','Exportación compoletada de manera exitosa')

            if download == True:
                download_path = self._make_call('get', export['Links']['Download'], filepath='/tmp/')
                print('Descarga completada de manera exitosa')
            else:
                print('Falló la descarga')

            if export_type =="Paradata":
                extract_path
            

        return export


    def get_info(self,job_id: int):
        return self._make_call(method="get", path=f"{self.url}/{job_id}")

    def download(self,job_id: Optional[int], download_link: Optional[str]):
        if job_id:
            download_link = self.get_info(job_id)['Links']['Download']
    
