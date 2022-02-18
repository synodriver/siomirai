from typing import Callable
import asyncio


def timeout(time: float):
    def deco(func: Callable):
        async def inner(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), time)

        return inner

    return deco
