import asyncio
from config import Settings


class ConcurrencyLimiter:
    def __init__(self, max_concurrent: int = Settings().max_concurrency_limit):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute_tasks(self, tasks):
        semaphore = self.semaphore

        async def limited_task(task):
            async with semaphore:
                return await task

        limited_tasks = [limited_task(task) for task in tasks]
        return await asyncio.gather(*limited_tasks)
