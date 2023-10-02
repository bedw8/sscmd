from typing import Optional, Union, Dict
from urllib.parse import unquote
from .client import Client
from .exceptions import NotFoundError, UnauthorizedError, ForbiddenError, NotAcceptableError
import re, os

class BaseApi():
    _apiprefix: str = '/'

    def __init__(self, client: Client,workspace: Optional[str] = None) -> None:
        self._client = client
        self.workspace = client.workspace if workspace is None else workspace

    @property
    def url(self) -> str:
        return (f"{self._client.baseurl}/{self.workspace}{self._apiprefix}" if self.workspace else f"{self._client.baseurl}{self._apiprefix}")

    def _make_call(self, method: str, path: str, filepath: Optional[str] = None, 
            use_login_session: bool = False, **kwargs) -> Union[Dict[str, dict], str, None]:

        if use_login_session:
            response = self._make_call_with_login(method=method, path=path, **kwargs)
        else:
            response = self._client.session.request(method=method, url=path, **kwargs)

        self._process_status_code(response)

        if 'Content-Type' in response.headers:
            if 'application/json' in response.headers['Content-Type']:
                return response.json()

            elif any(w in response.headers['Content-Type'] for w in ['application/zip', 'application/octet-stream']):
                return self._get_file_stream(filepath, response)
            else:
                return response.text

    @staticmethod
    def _process_status_code(response):
        code = response.status_code
        if code == 401:
            raise UnauthorizedError()
        elif code == 403:
            raise ForbiddenError()
        elif code == 404:
            raise NotFoundError(response.text)
        elif code in [400, 406]:
            print(response)
            raise NotAcceptableError(response.text)
        else:
            response.raise_for_status()

    @staticmethod
    def _get_file_stream(filepath, response) -> str:
        d = response.headers['content-disposition']
        fname = re.findall(
            r"filename\*=utf-8''(.+)", d, flags=re.IGNORECASE)

        if not fname:
            fname = re.findall(
                r"filename[ ]*=([^;]+)", d, flags=re.IGNORECASE)

        fname = fname[0].strip().strip('"')
        outfile = os.path.join(filepath, unquote(fname))

        with open(outfile, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return outfile
