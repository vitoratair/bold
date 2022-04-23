import hashlib
import logging

from core import constants as core_c
from rest_framework.test import APITestCase

from omdb_adapter.connection_service import ConnectionService

logger = logging.getLogger('adapter_omdb')

class OmdbAdapterTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = {"token": "apikey=707b99bc"}
        cls.urls = {"movie": "http://www.omdbapi.com/?t=%s&%s", "season": "http://www.omdbapi.com/?i=%s&%s"}
        cls.hash = hashlib.new('sha256')
        cls.payload_hash = "bfd93f8069b57a9aefef7f38687bfa5d6d2984102dcb216675f0b18f125462b2"

    def test_invalid_key(self):
        """
            Must pass an invalid token to OMDB server.
            The response must be False
        """

        service = ConnectionService(auth={"token": "apikey=7ss07b99bc"}, urls=self.urls)
        api_response = service.get_movies(core_c.GOT)
        self.assertEqual(api_response, False)

    def test_sync_db_payload(self):
        """
            Must check if the response payload from OMDB server is correct
        """

        service = ConnectionService(auth=self.auth, urls=self.urls)
        api_response = service.get_movies(core_c.GOT)
        self.hash.update(str(api_response).encode())
        self.assertEqual(self.hash.hexdigest(), self.payload_hash)
