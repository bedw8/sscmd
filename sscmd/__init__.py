from .client import Client
from .questionnaires import QuestionnairesApi
from .export import ExportApi
from .assignments import AssignmentsApi

__appname__ = "sscmd"
__version__ = "0.1"


del client, questionnaires, export, assignments, baseapi, exceptions

__all__ = ["__version__", "ExportApi", "Client", "QuestionnairesApi","AssignmentsApi" ]
