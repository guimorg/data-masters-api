"""Configuring workers for ThreadPoolExecutor"""
import signal
import asyncio

from concurrent.futures import ProcessPoolExecutor

from api.config import WORKERS_OPTION as config_workers


def warm():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def clean():
    # Cleaning up models in memory of workers
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    global _score_model
    global _pre_process_model
    _score_model = None
    _pre_process_model = {}


async def init_workers(app):
    """
    Initializing ProcessPoolExecutor to execute
    sync functions as async.
    """
    n = int(config_workers("max_workers"))
    executor = ProcessPoolExecutor(max_workers=n)
    loop = asyncio.get_event_loop()
    run = loop.run_in_executor
    fs = [run(executor, warm) for i in range(0, n)]
    await asyncio.gather(*fs)

    async def close_executor(app):
        fs = [run(executor, clean) for i in range(0, n)]
        await asyncio.shield(asyncio.gather(*fs))
        executor.shutdown(wait=True)

    app.on_cleanup.append(close_executor)
    app['executor'] = executor
    return executor
