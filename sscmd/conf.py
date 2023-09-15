
from typing import Union
from pathlib import Path
import tomllib

class Config:
    @classmethod
    def load(cls, path: Union[str,Path]) -> None:
        return tomllib.load(Path(path).open('rb'))





