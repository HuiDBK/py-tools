import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from py_tools.decorators.base import run_on_executor
from loguru import logger

thread_executor = ThreadPoolExecutor(max_workers=3)


@run_on_executor(background=True)
async def async_func_bg_task():
    logger.debug("async_func_bg_task start")
    await asyncio.sleep(1)
    logger.debug("async_func_bg_task running")
    await asyncio.sleep(1)
    logger.debug("async_func_bg_task end")
    return "async_func_bg_task ret end"


@run_on_executor()
async def async_func():
    logger.debug("async_func start")
    await asyncio.sleep(1)
    logger.debug("async_func running")
    await asyncio.sleep(1)
    return "async_func ret end"


@run_on_executor(background=True, executor=thread_executor)
def sync_func_bg_task():
    logger.debug("sync_func_bg_task start")
    time.sleep(1)
    logger.debug("sync_func_bg_task running")
    time.sleep(1)
    logger.debug("sync_func_bg_task end")
    return "sync_func_bg_task end"


@run_on_executor()
def sync_func():
    logger.debug("sync_func start")
    time.sleep(1)
    logger.debug("sync_func running")
    time.sleep(1)
    return "sync_func ret end"


async def main():
    ret = await async_func()
    logger.debug(ret)

    async_bg_task = await async_func_bg_task()
    logger.debug(f"async bg task {async_bg_task}")
    logger.debug("async_func_bg_task 等待后台执行中")

    loop = asyncio.get_event_loop()
    for i in range(3):
        loop.create_task(async_func())

    ret = await sync_func()
    logger.debug(ret)

    sync_bg_task = sync_func_bg_task()
    logger.debug(f"sync bg task {sync_bg_task}")
    logger.debug("sync_func_bg_task 等待后台执行")

    await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
