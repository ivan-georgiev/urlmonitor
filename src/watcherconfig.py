# pylint: disable=too-few-public-methods,too-many-arguments
"""
Module containing watcher configuration
"""


class WatcherConfig():
    """
    Struct defining watcher configuration
    """

    def __init__(self, url: str, checkPeriodInSec: int, requestParams: dict,
                 responseCodesHealthy: set, responseBodyHealthyRegex: str, responseHeadersHealthyRegex: dict):

        self.url = url
        self.checkPeriodInSec = checkPeriodInSec
        self.requestParams = requestParams
        self.responseCodesHealthy = responseCodesHealthy
        self.responseBodyHealthyRegex = responseBodyHealthyRegex
        self.responseHeadersHealthyRegex = responseHeadersHealthyRegex
