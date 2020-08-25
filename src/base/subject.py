"""
Module containing the Subject base class intended to be inherited
"""
from base.iobserver import IObserver
from uuid import UUID
import logging


class Subject():

    def __init__(self):
        self._observers = set()
        self._logger = logging.getLogger(__name__)

    def attach(self, obs: IObserver) -> None:
        """
        Attach observer to the set
        """
        self._observers.add(obs)

    def detach(self, obs: IObserver) -> None:
        """
        Dettach observer from the set
        """
        self._observers.remove(obs)

    def notify(self, correlationId: UUID, msg: object) -> None:
        """
        Execute each observer `notify` method
        """
        for obs in self._observers:
            # observer should not raise exceptions, but add protection logic
            try:
                obs.update(correlationId, msg)
            except Exception as e:
                self._logger.error(
                    f'Unable to notify observer {obs.name}. Error: {str(e)}')
