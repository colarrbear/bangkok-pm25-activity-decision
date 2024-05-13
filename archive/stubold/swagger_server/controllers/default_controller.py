import connexion
import six

from swagger_server.models.api import API  # noqa: E501
from swagger_server.models.locationto_decision import LocationtoDecision  # noqa: E501
from swagger_server.models.pmapi import PMAPI  # noqa: E501
from swagger_server import util


def controller_get_api():  # noqa: E501
    """Returns a list of API.

     # noqa: E501


    :rtype: List[API]
    """
    return 'do some magic!'


def controller_get_locationto_decision():  # noqa: E501
    """Returns a list of Decision.

     # noqa: E501


    :rtype: List[LocationtoDecision]
    """
    return 'do some magic!'


def controller_get_pm_api():  # noqa: E501
    """Returns a list of PM.

     # noqa: E501


    :rtype: List[PMAPI]
    """
    return 'do some magic!'
