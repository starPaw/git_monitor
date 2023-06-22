import re
import aiohttp
import asyncio
from config import TOKEN
from db_connector import DBConnector


class GithubService:
    event_types = ['WatchEvent', 'PullRequestEvent', 'IssuesEvent']
    db = DBConnector()

    def __init__(self):
        self.etag = None
        self.fetch_task = None

    @staticmethod
    def parse_link_header(link_header):
        links = link_header.split(", ")
        urls = {re.findall('rel="(.*)"', link)[0]: re.findall("<(.*)>", link)[0] for link in links}
        return urls

    async def fetch_github_events(self):

        headers = {"accept": "application/vnd.github+json",
                   "Authorization": f"Bearer {TOKEN}"}
        while True:
            if self.etag:
                headers["If-None-Match"] = self.etag
            async with aiohttp.ClientSession(headers=headers) as session:
                url = 'https://api.github.com/events'
                while url:
                    async with session.get(url, params={"per_page": 100}) as resp:
                        poll_interval = int(resp.headers.get("X-Poll-Interval", "60"))
                        if resp.status == 304:
                            print("hi")
                            await asyncio.sleep(poll_interval)
                            continue
                        self.etag = resp.headers.get("ETag")
                        events = await resp.json()
                        for event in events:
                            if event['type'] not in self.event_types:
                                continue

                            new_event = self.db.add_event(event)
                            if not new_event:
                                break

                    if not new_event:
                        break
                    link_header = resp.headers.get('Link')
                    if link_header:
                        links = self.parse_link_header(link_header)
                        url = links.get("next")
                    else:
                        url = None
                    await asyncio.sleep(poll_interval)
            await asyncio.sleep(poll_interval)

    async def start(self):
        self.fetch_task = asyncio.create_task(self.fetch_github_events())

    async def stop(self):
        self.fetch_task.cancel()
        await self.fetch_task

