from requests import Session
from typing import Optional

class Client():
    """Initializes the API client
    :param url: URL of the headquarters app
    :param api_user: API user name
    :param api_password: API user password
    :param token: Authorization token
    :param workspace: Name of the workspace. If `None`, "primary" will be assumed
    """

    def __init__(self, url: str,
                 api_user: Optional[str] = None,
                 api_password: Optional[str] = None,
                 token: Optional[str] = None,
                 workspace: str = "primary"):
        session = Session()

        if token:
            session.headers.update({"Authorization": f"Bearer {token}"})
        elif api_user and api_password:
            session.auth = (api_user, api_password)

        session.headers.update({"User-Agent": 'python'})
        self.baseurl = url.rstrip("/")
        self.session = session
        self.workspace = workspace


