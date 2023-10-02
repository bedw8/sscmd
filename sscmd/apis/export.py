from pathlib import Path
from typing import Optional, Union, Literal 
import time
import io
from zipfile import ZipFile
from datetime import datetime

from .baseapi import BaseApi

class ExportApi(BaseApi):
    
    EXPORT_STATUS = Literal['Created', 'Running', 'Completed', 'Fail', 'Canceled']
    EXPORT_TYPE = Literal['Tabular', 'STATA', 'SPSS', 'Binary', 'DDI','Paradata']
    INTERVIEW_STATUS = Literal['All', 'SupervisorAssigned', 'InterviewerAssigned',\
        'Completed','RejectedBySupervisor', 'ApprovedBySupervisor', 'RejectedByHeadquarters',\
        'ApprovedByHeadquarters']

    _apiprefix: str = "/api/v2/export"

    def get_list(self,
                 q_id: Optional[str] = None,
                 q_version: Optional[int] = None,
                 export_type: Optional[EXPORT_TYPE] = None,
                 interview_status: Optional[INTERVIEW_STATUS] = None,
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
            "exportStatus": export_status,
            "hasFile": has_file,
        }

        if not q_id:
            q_id = self._client.config['general']['q_id']
    
        if not q_version:
            q_version = self._client.config['general']['q_version']
        
        if q_id and q_version:
            params['questionnaireIdentity'] = '{}${}'.format(q_id, q_version)
        
        r = self._make_call('get', path, params=params)
        if r:
            for item in r:
                yield item


    def start(self, 
              export_type: EXPORT_TYPE, 
              q_id: Optional[str] = None,
              q_version: Optional[int] = None, 
              from_: Optional[str] = None, 
              to: Optional[str] = None, 
              wait: bool = True, 
              download=True, 
              outPath: Path = None, 
              show_progress: bool = True):
        """Start new export job
        :param export_type
        :returns: request response
        """
        path = self.url
        
        data={
              "ExportType": export_type,
              "InterviewStatus": "All",
              "From": from_,
              "To": to,
              "AccessToken": None,
              "RefreshToken": None,
              "StorageType": None,
              "TranslationId": None,
              "IncludeMeta": True
            }

        if not q_id:
            q_id = self._client.config['general']['q_id']
    
        if not q_version:
            q_version = self._client.config['general']['q_version']
        
        if q_id and q_version:
            data['QuestionnaireId'] = '{}${}'.format(q_id, q_version)
            
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
                    print(f"{progress}%", end="\r")
                export = self.get_info(export['JobId'])
                progress = export['Progress']

            if show_progress:
                print('100%','Exportación compoletada de manera exitosa')

            if download == True:
                if not outPath:
                    p = datetime.now().strftime('%Y%m%dT%H%M')
                    outPath = Path(p)

                if export_type =="Paradata":
                    outPath = outPath / f'paradata_v{q_version}'
                if export_type =="STATA":
                    outPath = outPath / f'SurveySolutions_v{q_version}'

                try:
                    outPath.mkdir(parents=True,exist_ok=True)
                except:
                    now = datetime.now()
                    nowStr = datetime.strftime(n,'%Y%m%d%H%M')
                    outPath = Path('export_'+nowStr)
                    outPath.mkdir(parents=True,exist_ok=True)

                self.download(export['JobId'], outPath)

        return export


    def get_info(self,job_id: int):
        return self._make_call(method="get", path=f"{self.url}/{job_id}")

    def download(self,job_id: int, outPath: Path):
        download_link = self.get_info(job_id)['Links']['Download']
        response = self._client.session.get(download_link)
        zfile = ZipFile(io.BytesIO(response.content))
        zfile.extractall(outPath)
        print('Descarga completada de manera exitosa')


    
