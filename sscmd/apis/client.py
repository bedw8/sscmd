from requests import Session
from pathlib import Path
from typing import Optional, Union
from sscmd.conf import Config

class Client():
    """Initializes the API client
    :param url: URL of the headquarters app
    :param api_user: API user name
    :param api_password: API user password
    :param token: Authorization token
    :param workspace: Name of the workspace. If `None`, "primary" will be assumed
    """

    
    
    def __init__(self, 
                 configFile: Union[str,Path] = Path('project.conf'),
                 url: Optional[str] = None,
                 api_user: Optional[str] = None,
                 api_password: Optional[str] = None,
                 token: Optional[str] = None,
                 workspace: str = "primary"
                ):

        
        args = locals()

        self.config = Config.load(configFile) 
        self.config = self.config if configFile else {}

        for section in ['credentials','general']:
            if section not in self.config:
                self.config[section] = {}

        # credentials
        for a in ['api_user','api_password','token']:
            if args[a] is not None:
                self.config['credentials'][a] = args[a]
            elif a not in self.config['credentials']:
                self.config['credentials'][a] = None
                
        # general
        for a in ['url','workspace']:
            if args[a] is not None:
                self.config['general'][a] = args[a]
            elif a not in self.config['general']:
                self.config['general'][a] = None
            
        self.session = Session()

        token = self.config['credentials']['token']
        api_user = self.config['credentials']['api_user']
        api_password = self.config['credentials']['api_password']
        
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        elif api_user and api_password:
            self.session.auth = (api_user, api_password)

        self.session.headers.update({"User-Agent": 'python'})
        self.baseurl = self.config['general']['url'].rstrip("/")
        self.workspace = self.config['general']['workspace']


