print("Client side has been load")

import js
import pyodide
import asyncio
from functools import wraps

def client_side(f):
    @wraps(f)
    def inner(*args, **kwargs):
        return asyncio.ensure_future(f(*args, **kwargs))
    return inner