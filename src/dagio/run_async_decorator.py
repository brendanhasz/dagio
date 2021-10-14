import asyncio
from functools import partial


def run_async(fn):
    """Runs a non-async function in a thread pool."""

    async def wrapped_fn(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))

    return wrapped_fn
