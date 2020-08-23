#!/usr/bin/env python3

from scraper import Scraper
from watcherconfig import WatcherConfig
from osaction import OsAction
from apicall import ApiCall

import argparse
import os
import pathlib
import asyncio
import json
import sys


class Config():
    """
    Default config files names
    """
    WATCHER_URLS = 'conf-urls.json'
    OSACTION_URLS = 'conf-osa_urls.txt'
    APIACTION_URLS = 'conf-apia_urls.txt'


def filePath(path: str) -> str:
    """
    Argparse method. Validate if path is valid and return absolute path
    """
    if os.path.isfile(path):
        return os.path.abspath(path)
    else:
        raise argparse.ArgumentTypeError(f'"{path}" is not a file')


def main(args: argparse.Namespace):
    """
    Main method. Reads URL list and initializes scaper and observers
    """

    here = pathlib.Path(__file__).parent.parent

    urlsFile = args.urls if args.urls else here.joinpath(Config.WATCHER_URLS)
    osurlsFile = args.osurls if args.osurls else here.joinpath(
        Config.OSACTION_URLS)
    apiurlsFile = args.apiurls if args.apiurls else here.joinpath(
        Config.APIACTION_URLS)

    with open(urlsFile) as ufile:
        urls = json.load(ufile)

    # transform json to objects of type WatcherConfig
    urlsObjects = [WatcherConfig(url=url['url'],
                                 checkPeriodInSec=url['checkPeriodInSec'],
                                 requestParams=url.get('requestParams', {}),
                                 responseCodesHealthy=set(
                                     url['responseCodesHealthy']),
                                 responseBodyHealthyRegex=url.get(
                                     'responseBodyHealthyRegex'),
                                 responseHeadersHealthyRegex=url.get(
                                     'responseHeadersHealthyRegex')
                                 ) for url in urls]

    with open(osurlsFile) as ufile:
        # read all lines as set
        osurls = set(map(str.strip, ufile))

    with open(apiurlsFile) as ufile:
        # read all lines as set
        apiurls = set(map(str.strip, ufile))

    # init scraper for the URLs list
    scraper = Scraper(urlsObjects)

    # attach observers to receive notification on fail
    scraper.attach(OsAction(scope=osurls, name='Test-OSPing',
                            cmd=('ping', '127.0.0.1', '-n', '1'), waitToComplete=True))
    scraper.attach(ApiCall(scope=apiurls, name='Test-Sendemail'))

    # run scraper
    asyncio.run(scraper.run())


if __name__ == '__main__':
    #sys.argv = ["", "-c", "urls.json"]

    if sys.version_info < (3, 7):
        sys.exit(
            f'Python minumum version required is 3.7. Current version is {sys.version_info}')

    # parse arguments
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument('-urlc', '--urlconfig', dest='urls', metavar='path/to/config.json',
                        type=filePath, help='Path to urls to be watched.')
    parser.add_argument('-osurls', dest='osurls', metavar='path/to/osa_urls.txt',
                        type=filePath, help='Path to urls to execute OS command')
    parser.add_argument('-apiurls', dest='apiurls', metavar='path/to/apia_urls.txt',
                        type=filePath, help='Path to urls to execute API command')
    args = parser.parse_args()

    main(args)
