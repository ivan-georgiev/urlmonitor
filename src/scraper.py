"""
Module implementig the URL watcher and the Subject role in Subject-Observer pattern
"""
from base.subject import Subject
from watcherconfig import WatcherConfig

import logging
import sys
import os
import asyncio
import aiohttp
from aiohttp import ClientSession
import uuid
import copy

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    datefmt='%H:%M:%S',
    stream=sys.stderr,
)
logger = logging.getLogger('scraper')


class Scraper(Subject):

    def __init__(self, urls):
        super().__init__()
        self._urls = urls

    async def _invokeWebRequest(self, url: str, session: ClientSession, requestParams: dict) -> aiohttp.ClientResponse:
        """request wrapper to execute web request.
        requestParams are passed to `session.request()`.
        """
        # deep copy to avoid modifying the dict
        newRequestParams = copy.deepcopy(requestParams)

        # add user-agent header if missing
        passedHeaders = newRequestParams.get('headers', dict())
        if not passedHeaders.get('user-agent'):
            passedHeaders['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
        newRequestParams['headers'] = passedHeaders

        # add default method HEAD if not set
        if not newRequestParams.get('method'):
            newRequestParams['method'] = 'HEAD'

        resp = await session.request(url=url, **newRequestParams)
        # Raise an aiohttp.ClientResponseError if the response status is 400 or higher.
        # resp.raise_for_status()
        return resp

    async def _checkUrl(self, url: WatcherConfig, session: ClientSession) -> str:
        """GET request wrapper to fetch page HTML.
        requestParams are passed to `session.request()`.
        """
        while True:
            error = None
            try:
                resp = await self._invokeWebRequest(url=url.url, session=session, requestParams=url.requestParams)
            except (
                aiohttp.ClientError,
                aiohttp.http_exceptions.HttpProcessingError,
            ) as e:
                logger.error(
                    f'aiohttp exception for {url.url} [{getattr(e, "status", None)}]: {getattr(e, "message", None)}'
                )
            except Exception as e:
                raise
            else:
                if resp.status not in url.responseCodesHealthy:
                    error = f'HTTP response code {resp.status} not in responseCodesHealthy'

                if error:
                    correlationId = uuid.uuid1()
                    logger.warning(
                        f'{url.url} is NOK. correlationId: {correlationId}. Error: {error}. Next check in {url.checkPeriodInSec} seconds'
                    )
                    # notify
                    self.notify(correlationId, (url.url, error))
                else:
                    logger.info(
                        f'{url.url} is OK[{resp.status}]. Next check in {url.checkPeriodInSec} seconds'
                    )

            await asyncio.sleep(url.checkPeriodInSec)

    async def run(self):
        """Crawl and check concurrently multiple `urls`."""
        async with ClientSession() as session:
            tasks = []
            for url in self._urls:
                tasks.append(
                    self._checkUrl(url=url, session=session)
                )
            res = await asyncio.gather(*tasks)
            print(res[0].status)
