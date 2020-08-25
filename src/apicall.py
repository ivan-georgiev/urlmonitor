"""
Module impementing api call in case of error
"""
from base.iobserver import IObserver

import requests
import logging
import os
import sys

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    datefmt='%H:%M:%S',
    stream=sys.stderr,
)
logger = logging.getLogger('apiaction')


class ApiCall(IObserver):
    """
    Class implementing api call in case of error
    """

    # api timeout
    _TIMEOUT = 20

    def __init__(self, scope: set, name: str):
        self._name = name
        self._scope = scope

    def update(self, correlationId: str, msg: object) -> None:
        """
        Executes predefined API call
        """
        if msg[0] not in self._scope:  # type: ignore
            return

        # example implementaton - can be changed with
        # send notification api - SendGrid, Slack, etc.
        # trigger repair endpoint

        try:
            endpoint = 'https://api.ipify.org?format=json'
            logger.info(f'{correlationId} - Call {endpoint}')
            resp = requests.get(endpoint, timeout=ApiCall._TIMEOUT)
            logger.debug(f'{correlationId} - Response {resp}')
        except Exception as e:
            logger.error(f'{correlationId} - {str(e)}')

    def name(self) -> str:
        return self._name
