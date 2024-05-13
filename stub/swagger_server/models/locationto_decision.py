# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class LocationtoDecision(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, ts: str=None, district: str=None, aqi: float=None, decision: str=None):  # noqa: E501
        """LocationtoDecision - a model defined in Swagger

        :param id: The id of this LocationtoDecision.  # noqa: E501
        :type id: int
        :param ts: The ts of this LocationtoDecision.  # noqa: E501
        :type ts: str
        :param district: The district of this LocationtoDecision.  # noqa: E501
        :type district: str
        :param aqi: The aqi of this LocationtoDecision.  # noqa: E501
        :type aqi: float
        :param decision: The decision of this LocationtoDecision.  # noqa: E501
        :type decision: str
        """
        self.swagger_types = {
            'id': int,
            'ts': str,
            'district': str,
            'aqi': float,
            'decision': str
        }

        self.attribute_map = {
            'id': 'id',
            'ts': 'ts',
            'district': 'district',
            'aqi': 'AQI',
            'decision': 'decision'
        }
        self._id = id
        self._ts = ts
        self._district = district
        self._aqi = aqi
        self._decision = decision

    @classmethod
    def from_dict(cls, dikt) -> 'LocationtoDecision':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The LocationtoDecision of this LocationtoDecision.  # noqa: E501
        :rtype: LocationtoDecision
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this LocationtoDecision.


        :return: The id of this LocationtoDecision.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this LocationtoDecision.


        :param id: The id of this LocationtoDecision.
        :type id: int
        """

        self._id = id

    @property
    def ts(self) -> str:
        """Gets the ts of this LocationtoDecision.


        :return: The ts of this LocationtoDecision.
        :rtype: str
        """
        return self._ts

    @ts.setter
    def ts(self, ts: str):
        """Sets the ts of this LocationtoDecision.


        :param ts: The ts of this LocationtoDecision.
        :type ts: str
        """

        self._ts = ts

    @property
    def district(self) -> str:
        """Gets the district of this LocationtoDecision.


        :return: The district of this LocationtoDecision.
        :rtype: str
        """
        return self._district

    @district.setter
    def district(self, district: str):
        """Sets the district of this LocationtoDecision.


        :param district: The district of this LocationtoDecision.
        :type district: str
        """

        self._district = district

    @property
    def aqi(self) -> float:
        """Gets the aqi of this LocationtoDecision.


        :return: The aqi of this LocationtoDecision.
        :rtype: float
        """
        return self._aqi

    @aqi.setter
    def aqi(self, aqi: float):
        """Sets the aqi of this LocationtoDecision.


        :param aqi: The aqi of this LocationtoDecision.
        :type aqi: float
        """

        self._aqi = aqi

    @property
    def decision(self) -> str:
        """Gets the decision of this LocationtoDecision.


        :return: The decision of this LocationtoDecision.
        :rtype: str
        """
        return self._decision

    @decision.setter
    def decision(self, decision: str):
        """Sets the decision of this LocationtoDecision.


        :param decision: The decision of this LocationtoDecision.
        :type decision: str
        """

        self._decision = decision
