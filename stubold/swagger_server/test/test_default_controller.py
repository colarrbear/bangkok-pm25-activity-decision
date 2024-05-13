# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api import API  # noqa: E501
from swagger_server.models.locationto_decision import LocationtoDecision  # noqa: E501
from swagger_server.models.pmapi import PMAPI  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_get_api(self):
        """Test case for controller_get_api

        Returns a list of API.
        """
        response = self.client.open(
            '/PMDecision/API',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_locationto_decision(self):
        """Test case for controller_get_locationto_decision

        Returns a list of Decision.
        """
        response = self.client.open(
            '/PMDecision/LocationtoDecision',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_pm_api(self):
        """Test case for controller_get_pm_api

        Returns a list of PM.
        """
        response = self.client.open(
            '/PMDecision/PMAPI',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
