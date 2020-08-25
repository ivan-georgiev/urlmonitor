# pylint: disable=too-many-arguments

"""
Observer implemtation doing OS command
"""
from base.iobserver import IObserver

import subprocess
import logging
import os
import sys

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    datefmt='%H:%M:%S',
    stream=sys.stderr,
)
logger = logging.getLogger('osaction')


class OsAction(IObserver):
    """
    Class implementing observer executing os commands
    """

    # process execution timeout
    _TIMEOUT = 20

    def __init__(self, scope: set, name: str, cmd: tuple, useShell=False, waitToComplete=False):
        self._name = name
        self._cmd = cmd
        self._useShell = useShell
        self._waitToComplete = waitToComplete
        self._scope = scope

    def update(self, correlationId: str, msg: object) -> None:
        """
        Executes predefined OS command
        """
        if msg[0] not in self._scope:  # type: ignore
            return

        try:
            logger.info(f'{correlationId} - Execute {self._cmd}')
            proc = subprocess.Popen(self._cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=self._useShell, env=os.environ.copy())

            # if not set to wait - exit
            if not self._waitToComplete:
                return

            # get command output
            try:
                outs, errs = proc.communicate(timeout=OsAction._TIMEOUT)
            except Exception as e:
                proc.kill()
                outs, errs = proc.communicate()
                logger.error(f'{correlationId} - {str(e)} - {str(errs)}')
            logger.debug(f'{correlationId} - command output: {str(outs)}')

        except Exception as e:
            logger.error(f'{correlationId} - {str(e)}')

    @property
    def name(self) -> str:
        return self._name
