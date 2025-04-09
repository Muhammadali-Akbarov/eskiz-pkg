"""Client module for Eskiz.uz"""
from .sync import ClientSync # noqa

try:
    from .async_client import AsyncClient # noqa
    __all__ = ['ClientSync', 'AsyncClient']
except ImportError:
    # aiohttp might not be installed
    __all__ = ['ClientSync']
