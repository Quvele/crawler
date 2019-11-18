import asyncio
import logging
import io
import mimetypes
import os
import uuid
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Iterable, Optional

import aiohttp
import patoolib
import yarl
from lxml import html as lxml_html

from crawler import settings


logger = logging.getLogger(__name__)


class Crawler:

    site_url = settings.SITE_URL
    limit = settings.FILES_LIMIT
    files = set()
    archives_report = []

    def __init__(self) -> None:
        self.visited_urls = set()
        self.visited_urls.add(self.site_url)
        self.host = yarl.URL(self.site_url).host

    def start(self):
        logger.info('Start crawling site "%s"', self.site_url)

        self.executor = ThreadPoolExecutor()
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.fetch(self.site_url))
        except KeyboardInterrupt:
            logger.info('KeyboardInterrupt caught')
        except Exception:
            logger.error('Exception caught', exc_info=True)
        finally:
            loop.run_until_complete(asyncio.sleep(1))
            loop.close()
            self.executor.shutdown()

        self.write_to_file(self.files, 'downloaded_links')
        self.write_to_file(self.archives_report, 'archives_report')

    def write_to_file(self, lines: Iterable[str], name: str):
        if lines:
            guid = str(uuid.uuid4())[:8]
            filename = os.path.join(
                settings.BASE_DIR, f'{guid}_{name}.txt')
            with open(filename, 'x', encoding='utf-8') as f:
                f.writelines(lines)

    async def fetch(self, url: str, parent_url: Optional[str] = None):
        logger.info('URL : %s', url)

        if len(self.files) > self.limit:
            logger.info('Files limit is reached.')
            return

        if parent_url and self.host not in parent_url:
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                # check that response is file ready to download
                mtype, encoding = mimetypes.guess_type(url)
                if mtype or response.content_disposition:
                    self.files.add(url)
                    content = await response.read()
                    self.executor.submit(
                        self.download, url, mtype, response, content).result()
                    return

                html = await response.text()
                fs = [
                    asyncio.ensure_future(self.fetch(link, parent_url=url))
                    for link in self.get_links(html)
                ]
                await asyncio.gather(*fs)

    def download(
            self,
            url: str,
            mtype: str,
            response: 'ClientResponse',
            content: bytes,
    ) -> Optional[str]:
        """
        Download attachment if it is archive. Then do stats archives_report.
        """
        filename = None

        if mtype in settings.SUPPORTED_7ZIP_FORMATS:
            filename = os.path.join(
                settings.ARCHIVES_DIR,
                yarl.URL(url).parts[-1]
            )

        elif (response.content_disposition
              and response.content_type in settings.SUPPORTED_7ZIP_FORMATS):
            filename = os.path.join(
                settings.ARCHIVES_DIR,
                yarl.URL(url).parts[-1]
            )

        if filename:
            if not os.path.exists(filename):
                with open(filename, 'xb') as f:
                    f.write(content)

            report = self.unpack(filename)
            self.archives_report.extend(report)

            return filename

    def unpack(self, archive: str) -> Iterable[str]:
        """
        Extract files from archive and do stat archives_report.
        """
        report = []

        archive_name = os.path.basename(archive)

        logger.info('Unpacking archive "%s" ..', archive_name)

        archive_dir = archive_name.rsplit('.', maxsplit=2)[0]
        archive_path = os.path.join(settings.ARCHIVES_DIR, archive_dir)
        if not os.path.exists(archive_path):
            os.mkdir(archive_path)

        try:
            target = patoolib.extract_archive(
                archive,
                verbosity=0,
                outdir=os.path.join(settings.ARCHIVES_DIR, archive_dir)
            )
        except patoolib.util.PatoolError as e:
            logger.error('Cannot unpack archive "%s"', archive)
        else:
            for root, dirs, files in os.walk(target):
                for name in files:
                    size = os.path.getsize(os.path.join(root, name))
                    ftype = name.split('.')[-1]
                    row = f'{archive_name} - {name} - {ftype} - {size}\n'
                    report.append(row)

        return report

    def get_links(self, html: str) -> Iterable:
        """
        Gather links from document.
        """
        links = set()

        tree = lxml_html.parse(io.StringIO(html))
        for el in tree.iter():
            if el.tag == 'body':
                for element, attr, link, pos in el.iterlinks():
                    if (
                            attr == 'href'
                            and link not in self.visited_urls
                            and yarl.URL(link).is_absolute()
                    ):
                        links.add(link)

        return links
