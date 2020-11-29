import os
import signal

from functools import partial
from asyncio import get_event_loop, gather
from concurrent.futures import ThreadPoolExecutor


class ProcessHandler:
    def __init__(self):
        self.pool = ThreadPoolExecutor((os.cpu_count() or 1))
        self.loop = get_event_loop()

    @staticmethod
    async def get_executor(handlers):
        executor = await gather(*handlers, return_exceptions=True)
        return executor

    def start(self, handlers, cleanup_callback):
        for sig_name in {'SIGINT', 'SIGTERM'}:
            self.loop.add_signal_handler(
                getattr(signal, sig_name),
                partial(self.shutdown, sig_name, cleanup_callback)
            )
        self.loop.run_until_complete(self.get_executor(handlers))
        self.loop.run_forever()
        self.loop.stop()

    def shutdown(self, sig_name, cleanup_callback):
        print("Got signal %s. Exiting..." % sig_name)
        cleanup_callback()
        self.loop.stop()
